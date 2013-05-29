#include "monitor.h"

int main(int argc, char *argv[]) {
  int i;
  FILE *outp;
  struct cpu_stat stat;

  init_daemon(NULL);
  
  outp = fopen("write-energy.log", "w");
  if (!outp) exit(-EIO);

  cpu_util_init(&stat);
  for (i = 0; i < 10; ++i) {
    sleep(10);
    fprintf(outp, "%d - %f\n", i, cpu_util(&stat));
    fflush(outp);
  }
  fclose(outp);

  return 0;
}
