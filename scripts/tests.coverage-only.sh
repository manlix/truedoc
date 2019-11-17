#!/usr/bin/env bash

# Run tests and show report

# shellcheck source=/dev/null
. "$(dirname "$0")/lib/common.sh"

function main() {

  caption "Run tests and show report"

  pytest::installed || die "No pytest installed"

  cd "$(dirname "$0")/../" || die "Cannot open source dir"

  # Run tests and show report
  pytest --cov=truedoc
}

main
