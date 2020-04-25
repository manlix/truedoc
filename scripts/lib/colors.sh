#!/usr/bin/env bash
# shellcheck disable=SC2034

# Colors for bash scripts (see: https://gist.github.com/elucify/c7ccfee9f13b42f11f81)

RED=$(echo -en '\033[00;31m')
declare -r RED

GREEN=$(echo -en '\033[00;32m')
readonly GREEN

YELLOW=$(echo -en '\033[00;33m')
readonly YELLOW

MAGENTA=$(echo -en '\033[00;35m')
readonly MAGENTA

RESTORE=$(echo -en '\033[0m')
readonly RESTORE
