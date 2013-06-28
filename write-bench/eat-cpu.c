#include "monitor.h"

int main(int argc, char *argv[]) {
  int i = 654321;
  init_daemon(NULL);
  while (i > 0) {
    i = (i / 123) * 123 + (i % 123);
  }
  return 0;
}
