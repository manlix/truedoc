#!/usr/bin/env bash

# Run tests and save report as HTML to 'htmlcov' directory

# shellcheck source=/dev/null
. "$(dirname "$0")/lib/common.sh"

function main() {

  caption "Run tests and save report as HTML"

  pytest::installed || die "No pytest installed"

  cd "$(dirname "$0")/../" || die "Cannot open source dir"

  # Run tests and save report as HTML to 'htmlcov' directory
  pytest --cov-report html --cov=truedoc
}

main
