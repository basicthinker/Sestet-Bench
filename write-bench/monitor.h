#include <sys/param.h>
#include <unistd.h>
#include <stdint.h>
#include <stdlib.h>
#include <errno.h>
#include <stdio.h>

/*
 * Fork the current process to make daemon
 * @dir: new working directory. No change with `pwd` if it is NULL.
*/
static inline void init_daemon(const char *dir) {
  int pid;
  int i;
  if ((pid = fork())) {
    exit(0); // parent process
  } else if (pid < 0) {
    exit(-1);
  }

  // child process
  setsid();
  if ((pid = fork())) {
    exit(0); // session leader
  } else if (pid < 0) {
    exit(-1);
  }

  // daemon process
  for (i = 0; i < NOFILE; ++i) {
    close(i);
  }

  if (dir != NULL) {
    chdir(dir);
  }
}

struct cpu_stat {
  uint64_t user;
  uint64_t nice;
  uint64_t system;
  uint64_t idle;
  uint64_t iowait;
  uint64_t irq;
  uint64_t softirq; 
};

#define stat_sum(statp) \
    ((statp)->user + (statp)->nice + (statp)->system + (statp)->idle + \
    (statp)->iowait + (statp)->irq + (statp)->softirq)

static inline int cpu_util_begin(struct cpu_stat *stat) {
  FILE *fp;
  fp = fopen("/proc/stat", "r");
  if (!fp) return -EIO;

  fscanf(fp, "cpu %llu %llu %llu %llu %llu %llu %llu",
    &stat->user, &stat->nice, &stat->system, &stat->idle,
    &stat->iowait, &stat->irq, &stat->softirq);

  fclose(fp);
  return 0;
}

static inline double cpu_util_end(const struct cpu_stat *stat) {
  struct cpu_stat cur;
  double rate;
  FILE *fp = fopen("/proc/stat", "r");
  if (!fp) return 0;

  fscanf(fp, "cpu %llu %llu %llu %llu %llu %llu %llu",
    &cur.user, &cur.nice, &cur.system, &cur.idle,
    &cur.iowait, &cur.irq, &cur.softirq);

  fclose(fp);

  rate = (double)(cur.idle - stat->idle)/(stat_sum(&cur) - stat_sum(stat));
  return 1 - rate;
}

static int cpu_freq(void) {
  return 1000;
}

