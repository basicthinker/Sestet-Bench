#include "monitor.h"

int main(int argc, char *argv[]) {
  int i;
  FILE *outp;
  struct cpu_stat stat;

  init_daemon(NULL);
  
  outp = fopen("write-energy.log", "w");
  if (!outp) exit(-EIO);

  for (i = 0; i < 100; ++i) {
    cpu_util_begin(&stat);
    sleep(10);
    fprintf(outp, "%d - %f\n", i, cpu_util_end(&stat));
    fflush(outp);
  }
  fclose(outp);

  return 0;
}
