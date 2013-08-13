#include <stdio.h>

#include "monitor.h"

int main(int argc, char *argv[]) {
  int num_smpl, is_chart, uslice;
  struct timeval tv;
  double time;
  struct cpu_stat cpu_s;
  double cpu_u;
  int len, i;

  if (argc != 3) {
    printf("Usage: %s SamplesPerSec ToShowCharts\n", argv[0]);
    return -1;
  }

  num_smpl = atoi(argv[1]);
  is_chart = atoi(argv[2]);
  uslice = 1000000 / num_smpl;

  cpu_util_init(&cpu_s);
  while (1) {
    usleep(uslice);
    cpu_u = cpu_util(&cpu_s);
    len = cpu_u / 0.02;
    printf("%.6f\t%.2f%%\t", get_time(&tv), cpu_u * 100);
    if (is_chart) {
      for (i = 0; i < len; ++i)
        putchar('+');
      for (i = 50 - len; i > 0; --i)
        putchar('-');
    }
    putchar('\n');
  }

  return 0;
}

