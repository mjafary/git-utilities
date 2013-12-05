#!/bin/bash
#
# This script will reset the date and time of the most recent commit.
# This is useful if you have just squashed commits and want to make the 
# changes look like 'now' instead of the first one in the series.
#
# Use -i for interactive time entry
#

while getopts i option
do
  case "${option}"
  in
    i) read -p "Enter Time (hh:mm [dd Mmm]): " TIME;;
  esac
done

if [ "${TIME}" == '' ]; then
 TIME=`/bin/date "+%H:%M:%S %d %b"`
fi

GIT_COMMITTER_DATE=`/bin/date --utc --date="TZ=\"Australia/Adelaide\" ${TIME}"`; git commit --amend --date "$GIT_COMMITTER_DATE"
