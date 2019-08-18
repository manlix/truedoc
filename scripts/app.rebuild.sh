#!/usr/bin/env bash

# Rebuild truedoc-app with deps

# shellcheck source=/dev/null
. "$(dirname "$0")/lib/common.sh"


function main() {

    caption "Rebuild truedoc-app with deps"

    docker::installed || die "No Docker installed"
    docker_compose::installed || die "No docker-compose installed"

    cd "$(dirname "$0")/../" || die "Cannot open source dir"
    docker-compose -f docker-compose.dev.yml build --no-cache || die "Failed start by docker-compose"
}

main
