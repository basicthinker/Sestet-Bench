CC = arm-none-linux-gnueabi-gcc
CFLAGS += -Wall -static -march=armv7-a
 
all : cpu_trace ev_trace

cpu_trace : cpu_trace.c monitor.h
	$(CC) $(CFLAGS) -o cpu_trace.o $^

ev_trace : ev_trace.c monitor.h
	$(CC) $(CFLAGS) -o ev_trace.o $^

clean :
	rm cpu_trace.o ev_trace.o
