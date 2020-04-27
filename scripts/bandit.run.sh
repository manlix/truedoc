#!/usr/bin/env bash

# Run secure static analyser

# shellcheck source=/dev/null
. "$(dirname "$0")/lib/common.sh"

function main() {

  caption "Run Bandit"

  bandit::installed || die "No bandit installed"

  cd "$(dirname "$0")/../" || die "Cannot open source dir"

  # Run
  bandit -r ./truedoc/
}

main
