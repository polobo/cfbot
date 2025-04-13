#!/usr/bin/env python3

import json
import logging
import sys

import cfbot_commitfest
import cfbot_commitfest_rpc
import cfbot_util
import cfbot_patch

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
            #print(json.dumps(workflow[bucket], indent=2))
            cfbot_commitfest.record_submissions(conn, workflow[bucket]["submissions"])


        submission = cfbot_patch.choose_next_from_workflow(conn, workflow)
        print(json.dumps(submission, indent=2))
        # No actual, just see what would have happened
        patches = cfbot_commitfest_rpc.get_latest_attachments_for_submission(submission)
        print(json.dumps(patches, indent=2))

    return 0

if __name__ == "__main__":
    sys.exit(run())
