CXX := g++

CFLAGS := -std=c++14
CFLAGS += -g -O3
CFLAGS += -lm -lGL -lglut

build:
	mkdir -p build
	$(CXX) src/main.cpp -o build/main $(CFLAGS)

run: build
	./build/main

.PHONY: build run
