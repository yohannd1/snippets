CC         := cc
PRG        := main
SRC        := main.c
SOURCE_DIR := .
TARGET_DIR := .
IDIRS      :=
LIBS       :=
CFLAGS     :=

OBJ          := $(SRC:.c=.o)
SOURCE_FILES := $(patsubst %,$(SOURCE_DIR)/%,$(SRC))
TARGET_FILES := $(patsubst %,$(TARGET_DIR)/%,$(OBJ))
FLAGS        := $(LIBS) $(CFLAGS)

output: prepare $(TARGET_FILES) $(HEADERS)
	$(CC) $(TARGET_FILES) $(FLAGS) -o $(TARGET_DIR)/$(PRG)

%.o: %.c
	$(CC) -c $< -o $@ $(FLAGS)

prepare:
	mkdir -p $(TARGET_DIR)

clean:
	rm -f $(SOURCE_FILES)
	rm -f $(TARGET_FILES)

.PHONY: output prepare clean
