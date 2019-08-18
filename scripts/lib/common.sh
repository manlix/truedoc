#!/usr/bin/env bash
# shellcheck disable=SC2034
# See official page about ignore errors: https://github.com/koalaman/shellcheck/wiki/Ignore

# Install latest 'shellcheck' before:
#  $ sudo snap install shellcheck
#  ...
#  $ command -v shellcheck
#  /snap/bin/shellcheck

##################################################################
#
# Example to use:
#
# manlix@lab:~$ . ./git/ansible/scripts/common.sh
# manlix@lab:~$ msg "Hello World =)"
# Hello World =)
#
##################################################################

set -o pipefail
set -o errexit # analog: set -e
set -o nounset # analog: set -u

############################################
#  COLORS
############################################

# shellcheck source=/dev/null
. "$(dirname "${BASH_SOURCE[0]}")/colors.sh"

############################################
#  FUNCTIONS
############################################

# shellcheck source=/dev/null
. "$(dirname "${BASH_SOURCE[0]}")/functions.sh"
