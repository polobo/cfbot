#!/usr/bin/env python3

import json
import sys

import cfbot_commitfest
import cfbot_commitfest_rpc
import cfbot_util

# Without actually performing any builds poll the Commitfest service
# for patches and apply the priority algorighm to sort them.
# This serves the purpose of testing the commitfest integration,
# especially in development with a local commitfrest server,
# and, against the live commitfest server, providing a quick
# way to review the priority algorithm.

def run():
    with cfbot_util.db() as conn:
        # get the current Commitfest ID
        workflow = cfbot_commitfest_rpc.get_commitfest_workflow()
        print(json.dumps(workflow["open"], indent=2))
        print(json.dumps(workflow["inprogress"], indent=2))
        print(json.dumps(workflow["parked"], indent=2))
        print(workflow["open"])
        print(workflow["inprogress"])
        print(workflow["parked"])
        #cfbot_commitfest.pull_submissions(conn, workflow["open"])
        #cfbot_commitfest.pull_submissions(conn, workflow["inprogress"])
        #cfbot_commitfest.pull_submissions(conn, workflow["parked"])

    return 0

if __name__ == "__main__":
    sys.exit(run())
