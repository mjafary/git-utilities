#!/bin/bash
#
# This script will guide the user through the process of rebasing their current repository
# (and branch if not on master). Should take the guess work out.
#

# Globals

# The following is false by default
REBASE_CURRENT_BRANCH=0

GIT_BASE_DIR=`/usr/bin/git rev-parse --show-toplevel`

# Function to print the headers
print_header () {
  printf "\033[34m################################################################################\033[1;32m\n\n${1}\n\n\033[31mEnter to proceed: \033[0m" 
  read  TEMP
  pushd . > /dev/null
}

# Clear screen prior to starting
clear

# Get the current branch
STARTING_BRANCH=`/usr/bin/git branch | /bin/grep '*' | /usr/bin/awk '{print $2}'`

# If we are not in the master branch, check that we should be rebasing
if [ "${STARTING_BRANCH}" != 'master' ]; then
  printf "\033[34m################################################################################\033[1;32m\n\nNot currently on master branch, do you want to rebase ${STARTING_BRANCH} as well?\n\n\033[31m[y/N]: \033[0m"
  read TEMP

  case "${TEMP}" in
    y|Y)
      # Set flag to true
      REBASE_CURRENT_BRANCH=1;;
    *)
      REBASE_CURRENT_BRANCH=0;;
  esac

  # Change to master
  pushd . > /dev/null
  cd "${GIT_BASE_DIR}"
  if [ "${STARTING_BRANCH}" != 'master' ]; then
    printf "\033[1;32m\n\nChanging to master branch\033[0m\n\n"
    /usr/bin/git checkout master
  fi
fi

# Get the rebase source, default is upstream
printf "\033[34m################################################################################\033[1;32m\n\nWhich repository is your rebase target? [u]pstream or [o]rigin\n\n\033[31m[U/o]: \033[0m"
read TEMP

case "${TEMP}" in
  o|O)
    # Set flag to true
    REBASE_TARGET='origin';;
  *)
    REBASE_TARGET='upstream';;
esac

# Fetch repo data
if [ "${REBASE_TARGET}" == 'upstream' ]; then 
  printf "\033[34m################################################################################\033[1;32m\n\nFetching Upstream repo data \033[0m\n\n"
  /usr/bin/git fetch --prune upstream
fi

printf "\033[34m################################################################################\033[1;32m\n\nFetching Origin repo data \033[0m\n\n"
/usr/bin/git fetch --prune origin

# Do the rebase
printf "\033[34m################################################################################\033[1;32m\n\nRebasing to ${REBASE_TARGET}\033[0m\n\n"
/usr/bin/git rebase "${REBASE_TARGET}"/master

# Push changes back to master
if [ "${REBASE_TARGET}" == 'upstream' ]; then 
  printf "\033[34m################################################################################\033[1;32m\n\nJust rebased against upstream.\n\nDo you want to push to your origin/master branch?\n\n\033[31m[Y/n]:\033[0m"

  read TEMP

  case "${TEMP}" in
    n|N)
      ;;
    *)
      # Push changes to origin
      /usr/bin/git push origin master;;
  esac
fi

# Change back to other branch
if [ "${STARTING_BRANCH}" != 'master' ]; then
  printf "\033[34m################################################################################\033[1;32m\n\nGoing back to ${STARTING_BRANCH}\033[0m\n\n"
  /usr/bin/git checkout "${STARTING_BRANCH}"
  popd > /dev/null
  if [ ${REBASE_CURRENT_BRANCH} -eq 1 ]; then
    /usr/bin/git rebase master
  fi
fi


