#include <stdio.h>

#include "monitor.h"

int main(int argc, char *argv[]) {
  int num_smpl, uslice;
  struct timeval tv;
  double time;
  struct cpu_stat cpu_s;
  double cpu_u;
  int len, i;

  time = get_time(&tv);

  if (argc != 2) {
    printf("Usage: %s SamplesPerSec\n", argv[0]);
    return -1;
  }

  num_smpl = atoi(argv[1]);
  uslice = 1000000 / num_smpl;

  cpu_util_init(&cpu_s);
  while (1) {
    usleep(uslice);
    cpu_u = cpu_util(&cpu_s);
    len = cpu_u / 0.02;
    printf("%.2f%%\t", cpu_u * 100);
    for (i = 0; i < len; ++i)
      putchar('+');
    for (i = 50 - len; i > 0; --i)
      putchar('-');
    printf("\t%.2f\n", get_time(&tv) - time);
  }

  return 0;
}

