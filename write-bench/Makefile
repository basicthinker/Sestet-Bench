CC = arm-none-linux-gnueabi-gcc
CFLAGS += -Wall -static -march=armv7-a
 
all : write-energy

write-energy : write-energy.c monitor.h
	$(CC) $(CFLAGS) -o write-energy.o $^

clean :
	rm write-energy.o
