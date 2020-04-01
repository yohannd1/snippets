#!/usr/bin/env bash

append() {
  [ $# = 2 ] || exit 1
  printf "$1"
  grep -q ':$' <<<"$1" \
    || grep -q '^$' <<<"$1" \
    || printf ":"

  printf "$2"
}

pop() {
  [ $# = 1 ] || exit 1
  sed 's/:[^:]\+$//g' <<<"$1"
}

listPush() {
  [ $# = 2 ] || exit 1
  local oldList="${!1}"
  local newList="$(append "$oldList" "$2")"
  eval "$1=${newList@Q}"
}

listPush a 1
listPush a 1
