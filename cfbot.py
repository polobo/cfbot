#!/usr/bin/env python3

import cfbot_cirrus

import cfbot_commitfest
import cfbot_commitfest_rpc
import cfbot_config
import cfbot_patch
import cfbot_util
import cfbot_web

import errno
import fcntl
import logging
import requests


def try_lock():
    """Make sure that only one copy runs."""
    fd = open(cfbot_config.LOCK_FILE, "w")
    try:
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        return fd
    except IOError as e:
        if e.errno != errno.EAGAIN:
            raise
        else:
            return None


def run():
    with cfbot_util.db() as conn:
        # pull in any build results that we are waiting for
        # XXX would need to aggregate the 'keep_polling' flag if we went
        # back to supporting multiple providers, or do something smarter,
        # but considering the plan to double-down on cirrus and switch to
        # webhooks, not bothering for now
        cfbot_cirrus.pull_build_results(conn)

        cursor = conn.cursor()
        cursor.execute("""SELECT COUNT(*)
                        FROM branch
                        WHERE status = 'testing'""")
        row = cursor.fetchone()

        if row and row[0] >= cfbot_config.CONCURRENT_BUILDS:
            cfbot_util.gc(conn)
            return
        else:
            patch = cfbot_commitfest_rpc.get_next_patch()
            cfbot_patch.process_patch(conn, patch)

if __name__ == "__main__":
    # don't run if we're already running
    lock_fd = try_lock()
    if lock_fd:
        try:
            run()
        except requests.exceptions.ReadTimeout:
            logging.error("Failed to process due to a timeout")
        except requests.exceptions.ConnectionError:
            logging.error("Failed to process due to a connection error")
        except requests.exceptions.HTTPError as e:
            logging.error("Failed to process due to an HTTP error: %s", e)
        lock_fd.close()
