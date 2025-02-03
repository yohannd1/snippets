#!/usr/bin/env bash

## A collection of stack operations in bash.
## Felt lazy, might make this work with dash later.

stackAppend() {
  [ $# = 2 ] || exit 1
  printf "$1"
  grep -q ':$' <<<"$1" \
    || grep -q '^$' <<<"$1" \
    || printf ":"

  printf "$2"
}

stackPop() {
  [ $# = 1 ] || exit 1
  sed 's/:[^:]\+$//g' <<<"$1"
}

stackPush() {
  [ $# = 2 ] || exit 1
  local oldList="${!1}"
  local newList="$(stackAppend "$oldList" "$2")"
  eval "$1=${newList@Q}"
}
