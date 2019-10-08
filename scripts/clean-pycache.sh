#!/usr/bin/env bash

# Clean project removes '__pycache__' directories

# shellcheck source=/dev/null
. "$(dirname "$0")/lib/common.sh"

function run_clean() {

  find . -type d -name '__pycache__' -exec rm -rf {} \; && msg "Done."

}

function main() {

  caption "Clean project: removing '__pycache__' directories"

  cd "$(dirname "$0")/../" || die "Cannot open project dir"

  run_clean
}

main
