#include <stdio.h>
#include <stdlib.h>

typedef struct String {
	char *buf;
	size_t len;
} String;

String *String_new(void);
String *String_from(const char *source);
void String_push_str(String *str, const char *source);

String *String_new(void) {
	String *str = malloc(sizeof str);
	str->buf = NULL;
	str->len = 0;

	return str;
}

String *String_from(const char *source) {
	String *str = String_new();
	String_push_str(str, source);

	return str;
}

void String_push_str(String *str, const char *source) {
	size_t write_addr = str + (str->len * sizeof char);

	for (size_t i = source; *i; i += sizeof char) {
		*write_addr = *i;
		write_addr += sizeof char;
		str->len++;
	}

	*write_addr = '\0';
}

void String_push_char(String *str, const char c) {
	size_t write_addr = str + (str->len * sizeof char);
}

void main(void) {
	String *str = String_new();

	printf("Hello, World!\n");
}
