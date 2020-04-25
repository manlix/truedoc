#!/usr/bin/env bash
#
# Common functions

# Print message to STDOUT
function msg() {

  echo "${GREEN}$*${RESTORE}"
}

# Print message to STDOUT with not new line
function prefix_msg() {

  echo -n "${MAGENTA}$*${RESTORE} "
}

# Print "OK" to STDOUT (useful for prefix_msg function)
function print_ok() {

  msg "OK"
}

# Print error message to STDERR and exit
function die() {

  echo >&2 "${RED}$*${RESTORE}"
  exit 1
}

# Print caption
function caption() {

  echo "${YELLOW}$*${RESTORE}"
}

# Program has been executed successfully
function exit::success() {

  msg "SUCCESS"
  exit 0
}

# Program has been executed failure
function exit::failure() {

  die "FAILURE"
}

############################################
# DOCKER package
############################################

# Is "docker" installed?

function docker::installed() {

  prefix_msg "Looking up [docker] executable..."
  # ATTENTION: avoid 'which' here. Because it failed by 'shellcheck'.
  command -v docker
}

function docker::stop_all_containers() {

  msg "Stopping all containers..."
  docker container ls --all --quiet | xargs -i docker container stop {}
}

function docker::remove_all_containers() {

  msg "Removing all containers..."
  docker container ls --all --quiet | xargs -i docker container rm {}
}

function docker::remove_all_images() {

  msg "Remove all images..."
  docker image ls --quiet | xargs -i docker image rm --force {}
}

############################################
# DOCKER-COMPOSE package
############################################

# Is "docker-compose" installed?

function docker_compose::installed() {

  prefix_msg "Looking up [docker-compose] executable..."
  # ATTENTION: avoid 'which' here. Because it failed by 'shellcheck'.
  command -v docker-compose
}

############################################
# PYTEST
############################################

# Is "pytest" installed?

function pytest::installed() {

  prefix_msg "Looking up [pytest] executable..."
  # ATTENTION: avoid 'which' here. Because it failed by 'shellcheck'.
  command -v pytest
}
