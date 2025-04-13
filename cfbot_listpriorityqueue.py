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
        workflow = cfbot_commitfest_rpc.get_commitfest_workflow()
        for bucket in ["open", "inprogress", "parked"]:
            workflow[bucket]["submissions"] = cfbot_commitfest_rpc.retrieve_cf_submission_list(workflow[bucket]["id"])
            print(json.dumps(workflow[bucket], indent=2))
            cfbot_commitfest.record_submissions(conn, workflow[bucket]["submissions"])
    return 0

if __name__ == "__main__":
    sys.exit(run())
