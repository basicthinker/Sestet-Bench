#include <stdio.h>
#include <stdlib.h>

#include <sys/time.h>

int main(int argc, char **argv) {
  int block_size, extra_size, block_num;
  int i;

  if (argc != 1 && argc != 4) {
    fprintf(stderr, "Usage:\n%s [block_size extra_size block_num]\n", argv[0]);
    return -1;
  }
  
  if (argc == 1) {
    block_size = 512 * 1024;
    extra_size = 4096;
    block_num = 100;
  } else {
    block_size = atoi(argv[1]);
    extra_size = atoi(argv[2]);
    block_num = atoi(argv[3]);
  }

  return 0;
}
