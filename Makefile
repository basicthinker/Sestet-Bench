CC = arm-none-linux-gnueabi-gcc
CFLAGS += -Wall -static -march=armv7-a
 
all : cpu_chart ev_trace

cpu_chart : cpu_chart.c monitor.h
	$(CC) $(CFLAGS) -o cpu_chart.o $^

ev_trace : ev_trace.c monitor.h
	$(CC) $(CFLAGS) -o ev_trace.o $^

clean :
	rm cpu_chart.o ev_trace.o
