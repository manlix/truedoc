#!/usr/bin/env bash

# Run tests

# shellcheck source=/dev/null
. "$(dirname "$0")/lib/common.sh"

function main() {

  caption "Run tests"

  pytest::installed || die "No pytest installed"

  cd "$(dirname "$0")/../" || die "Cannot open source dir"

  # Run tests
  pytest
}

main
