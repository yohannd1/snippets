#include <stdio.h>

/*
 * This is a test on C macros, using them to build functions. Quite a
 * weird experiment. I am scared.
 */
#define function(name, arglist, return_type, commands) \
    return_type name arglist { commands }

function(
        main, (), int,
        printf("Hello, World!\n");
        )
