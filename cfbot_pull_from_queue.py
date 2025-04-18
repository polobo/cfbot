#!/usr/bin/env python3

import json
import subprocess
import sys

import cfbot_commitfest_rpc
import cfbot_patch
import cfbot_util

def run():
    patch = cfbot_commitfest_rpc.get_next_patch()
    print(json.dumps(patch._asdict(), indent=2))
    with cfbot_util.db() as conn:
        cfbot_patch.process_patch(conn, patch, force_success=True)
        conn.commit()

    subprocess.run(["psql", "-c", "table branch", "cfbot"])
    subprocess.run(["psql", "-c", "table work_queue", "cfbot"])

    return 0

if __name__ == "__main__":
    sys.exit(run())
