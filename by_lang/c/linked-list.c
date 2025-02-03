#include <stdio.h>
#include <stdlib.h>

/* A Linked List implementation in C. Only supports integers. */

struct LinkedList {
    struct LinkedList *prev;
    int content;
    struct LinkedList *next;
};
typedef struct LinkedList LinkedList;

int ll_len(LinkedList*);
void ll_alloc(LinkedList*, int);
LinkedList *ll_new(int);
void ll_free_last(LinkedList*);
LinkedList *ll_pop(LinkedList*);

int main() {
    LinkedList *ls;

    ls = ll_new(10);
    printf("LinkedList Length: %d\n", ll_len(ls));

    ll_alloc(ls, 20);
    printf("LinkedList Length: %d\n", ll_len(ls));

    ll_free_last(ls);
    printf("LinkedList Length: %d\n", ll_len(ls));
}

int ll_len(LinkedList *list) {
    LinkedList *current = list;
    int len = 1;
    for (;;) {
        if (current->next == NULL) {
            return len;
        } else {
            current = current->next;
            len++;
        }
    }
}

void ll_alloc(LinkedList *list, int content) {
    LinkedList *current = list;
    LinkedList *new = malloc(sizeof(LinkedList));
    if (!new) {
        fprintf(stderr, "could not allocate linked list\n");
        exit(1);
    }

    for (;;) {
        if (current->next == NULL) {
            new->content = content;
            current->next = new;
            new->prev = current;
            break;
        } else {
            current = current->next;
        }
    }
}

LinkedList *ll_new(int content) {
    LinkedList *new = malloc(sizeof(LinkedList));
    if (!new) {
        fprintf(stderr, "could not allocate linked list\n");
        exit(1);
    }

    new->content = content;
    return new;
}

void ll_free_last(LinkedList *list) {
    LinkedList *current = list;
    LinkedList *previous = NULL;

    for (;;) {
        if (current->next == NULL) {
            previous->next = NULL;
            free(current);
            break;
        } else {
            previous = current;
            current = current->next;
        }
    }
}

LinkedList *ll_pop(LinkedList *list) {
    LinkedList *current = list;

    for (;;) {
        if (current->next == NULL) {
            return current;
        } else {
            current = current->next;
        }
    }
}
