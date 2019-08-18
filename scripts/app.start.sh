#!/usr/bin/env bash

# Start truedoc-app with deps

# shellcheck source=/dev/null
. "$(dirname "$0")/lib/common.sh"

function get_mysql_ip() {

  mysql_ip=$(docker container inspect truedoc_truedoc-mysql_1 -f "{{ .NetworkSettings.Networks.truedoc_default.IPAddress }}")

}

function wait_for_mysql() {

  get_mysql_ip

  while [ "$(docker inspect --format='{{.State.Health.Status}}' truedoc_truedoc-mysql_1)" != "healthy" ] || ! nc -zv "${mysql_ip}" 3306; do
    msg "Wait for 3 seconds to being MySQL started..."
    sleep 3
  done

}

function main() {

  caption "Start truedoc-app with deps"

  docker::installed || die "No Docker installed"
  docker_compose::installed || die "No docker-compose installed"

  cd "$(dirname "$0")/../" || die "Cannot open source dir"
  docker-compose -f docker-compose.dev.yml up -d || die "Failed start by docker-compose"

  wait_for_mysql
}

main
