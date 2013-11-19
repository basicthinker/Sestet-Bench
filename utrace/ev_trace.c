#include <stdio.h>
#include "monitor.h"

int main(int argc, char *argv[]) {
  char *dev_name[] = { "/dev/input/event2" };
  struct pollfd ev_fd;
  struct input_event event;
  int ret;

  if (argc != 2) {
    printf("Usage: %s OutputFile\n", argv[0]);
    return -1;
  } else {
    freopen(argv[1], "w", stdout);
  }

  evdev_start_listen(dev_name, &ev_fd, 1);

  while ((ret = evdev_next_input(&ev_fd, 1, &event)) >= 0) {
    if (event.type == EV_SYN && event.code == SYN_REPORT) {
      printf("%.6f\n", tv_sec(&event.time));
      fflush(stdout);
    }
  }

  if (ret < 0) {
    fprintf(stderr, "[ev_trace] failed to fetch input event: %d\n", ret);
    return ret;
  } else return 0;
}

