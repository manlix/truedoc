#!/usr/bin/env bash

# Start truedoc-app with deps

# shellcheck source=/dev/null
. "$(dirname "$0")/lib/common.sh"

############################################
# Get MySQL container IP address
############################################

function get_mysql_ip() {

  sudo docker container inspect truedoc_truedoc-mysql_1 -f '{{ .NetworkSettings.Networks.truedoc_default.IPAddress }}'
}

############################################
# Check that MySQL server is reachable
############################################

function mysql_is_reachable() {
  nc -z "${1}" 3306
}

############################################
# Check that MySQL container is ready
############################################

function mysql_is_healthy() {

  mysql_state="$(docker inspect --format='{{.State.Health.Status}}' truedoc_truedoc-mysql_1)"

  [ "${mysql_state}" == "healthy" ]
}

############################################
# Wait to being MySQL started...
############################################

function wait_for_mysql() {

  mysql_ip="$(get_mysql_ip)"

  while ! mysql_is_reachable "${mysql_ip}"; do
    sleep 1
  done

  while ! mysql_is_healthy; do
    sleep 3
  done
}

############################################
# Run containers...
############################################

function run_containers() {

  # Builds, (re)create, starts, and attaches to containers for a service
  sudo docker-compose up -d --remove-orphans || die "Failed start services by docker-compose"
}

############################################
# Initialize DB: create tables, ...
############################################

function init_db() {
  docker-compose exec truedoc-app sh -c "cd truedoc/ && PYTHONPATH=.. alembic upgrade head && exit"
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

  msg "Initializing DB (if required)..."
  init_db

  msg "Truedoc is ready to accept connections."
}

main
