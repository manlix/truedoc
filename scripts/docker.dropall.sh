#!/usr/bin/env bash

# Stop all containers and drop all images in Docker

# shellcheck source=/dev/null
. "$(dirname "$0")/lib/common.sh"


function main() {

    caption "Stop all containers and drop all images in Docker"

    docker::installed || die "No Docker installed"

    docker::stop_all_containers
    docker::remove_all_containers
    docker::remove_all_images
}

main
