CC := gcc

run: main
	./main

main: main.c
	$(CC) -c main.c
	$(CC) main.o -o main -lSDL2 -lm -Wall
