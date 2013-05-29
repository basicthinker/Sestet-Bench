#include "monitor.h"

#define NUM_CPU 4

int main(int argc, char *argv[]) {
  int i, j;
  FILE *outp;
  struct cpu_stat stat;
  uint32_t freqs[NUM_CPU];

  init_daemon(NULL);
  
  outp = fopen("write-energy.log", "w");
  if (!outp) exit(-EIO);

  cpu_util_init(&stat);
  for (i = 0; i < 10; ++i) {
    sleep(10);
    fprintf(outp, "%d - %f\n", i, cpu_util(&stat));
    if (cpu_freq(freqs, NUM_CPU) == NUM_CPU) {
      for (j = 0; j < NUM_CPU; ++j) {
        fprintf(outp, "\t%u", freqs[j]);
      }
      fprintf(outp, "\n");
    }
    fflush(outp);
  }
  fclose(outp);

  return 0;
}
