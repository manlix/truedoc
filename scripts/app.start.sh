#!/usr/bin/env bash

# Start truedoc-app with deps

# shellcheck source=/dev/null
. "$(dirname "$0")/lib/common.sh"

function get_mysql_ip() {

  docker container inspect truedoc_truedoc-mysql_1 -f '{{ .NetworkSettings.Networks.truedoc_default.IPAddress }}'
}

function mysql_is_healthy() {

  mysql_state="$(docker inspect --format='{{.State.Health.Status}}' truedoc_truedoc-mysql_1)"

  [ "${mysql_state}" == "healthy" ]
}

function mysql_is_reachable() {
  nc -z "${1}" 3306
}

function wait_for_mysql() {

  mysql_ip="$(get_mysql_ip)"

  while ! mysql_is_reachable "${mysql_ip}"; do
    sleep 1
  done

  while ! mysql_is_healthy; do
    sleep 3
  done
}

function run_containers() {

  # Builds, (re)create, starts, and attaches to containers for a service
  docker-compose up -d --remove-orphans || die "Failed start services by docker-compose"
}

function main() {

  caption "Start truedoc-app with deps"

  docker::installed || die "No Docker installed"
  docker_compose::installed || die "No docker-compose installed"

  cd "$(dirname "$0")/../" || die "Cannot open source dir"

  msg "Up containers..."
  run_containers

  prefix_msg "Wait to being MySQL started..."
  wait_for_mysql
  print_ok

  msg "Truedoc is ready to accept connections."
}

main
