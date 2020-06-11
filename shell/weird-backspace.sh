#!/usr/bin/env sh

while sleep 0.001; do
  printf '\b'
  case $A in
    "")
      A=0
      printf '|'
      ;;
    0) A=1; printf '/' ;;
    1) A=2; printf '-' ;;
    2) A=3; printf '\' ;;
    3) A=0; printf '·|' ;;
  esac
done
