#!/bin/sh

function append {
    [ $# = 2 ] || exit 1
    printf "${1}"
    grep -q ':$' <<<"${1}" ||
    grep -q '^$' <<<"${1}" ||
        printf ":"
    printf "${2}"
}

function pop {
    [ $# = 1 ] || exit 1
    sed 's/:[^:]\+$//g' <<<"${1}"
}

function list_push {
    [ $# = 2 ] || exit 1
    local old_list="${!1}"
    local new_list="$(append "${old_list}" "${2}")"
    eval "${1}=${new_list}"
}
