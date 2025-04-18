#!/bin/sh
#
# This script applies patches inside a docker container.

set -e

TEMPLATE_DIR=patchburner_template
MOUNTED_DIR=patchburner_mock

usage() {
	echo "Usage: $1 init|create|apply|destroy"
	echo
	echo "init-template -- create 'patchburner_template'"
	echo
	echo "create -- create a new docker image with the cfbot-patchburner tag"
	echo "apply -- apply all the patches found in patchburner/work/patches'"
	echo "destroy -- destroy 'patchburner' if it exists"
	echo
	echo "template-repo-patch -- report path of template git repo"
	echo "burner-patch-path -- report path where patches should be placed"
	echo "burner-repo-path -- report path of burner git repo"
	exit 1
}

init_template() {
	# This is just a clean checkout of the git repo, which cfbot will keep
	# updated, and we'll copy whever we need a throw-away copy to apply patches
	# to.  This just avoids having to clone it every time, which would suck.
	# You should only need to init once.
    echo "init-template"
}

destroy_patchburner_if_exists() {
	echo "destory"
}

create_patchburner() {
	echo "create"
}

apply_patches_in_patchburner() {
	echo "apply"
}

case $1 in
init-template)
	init_template
	;;
create)
	create_patchburner
	;;
destroy)
	destroy_patchburner_if_exists
	;;
apply)
	apply_patches_in_patchburner
	;;
template-repo-path)
	echo $TEMPLATE_DIR/work/postgresql
	;;
burner-patch-path)
	echo $MOUNTED_DIR/work/patches
	;;
burner-repo-path)
	echo $MOUNTED_DIR/work/postgresql
	;;
*)
	usage
	;;
esac
