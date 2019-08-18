#!/usr/bin/env bash

# Build truedoc-app Docker image

# shellcheck source=/dev/null
. "$(dirname "$0")/lib/common.sh"

function main() {

  caption "Build truedoc-app Docker image"

  docker::installed || die "No Docker installed"

  cd "$(dirname "$0")/../" || die "Cannot open source dir"
  docker build --tag truedoc-app --no-cache -f ./Dockerfile.dev . || die "Failed build Docker image"
}

main
