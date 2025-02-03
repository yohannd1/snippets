#!/usr/bin/env sh

i=0
interval=0.10
while true; do
  case "$i" in
    0) printf '|' ;;
    1) printf '/' ;;
    2) printf '-' ;;
    3) printf '\' ;;
  esac
  i=$(( ($i+1) % 4 ))
  printf '\b'

  sleep "$interval"
done
