#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/time.h>

#include "monitor.h"

#define NUM_CPU 2
#define TEST_NUM 10
#define SLEEP_TIME 10
#define WRITE_SIZE (1024 * 1024 * 4) //bytes

#define sec(tv) (tv->tv_sec + (double)tv->tv_usec / 1000 / 1000)

static inline double get_time(struct timeval *tv) {
  gettimeofday(tv, NULL);
  return sec(tv);
}

static inline void do_monit(struct cpu_stat *stat, double *util, uint32_t freqs[]) {
  int num = cpu_freq(freqs, NUM_CPU);
  while (num < NUM_CPU) freqs[num++] = 0;
  *util = cpu_util(stat);
}

int main(int argc, char *argv[]) {
  int i, j, fd;
  FILE *fp;
  char file_name[64];
  char *content;
  double tv_begin, wt_begin[TEST_NUM * 2], wt_end[TEST_NUM * 2];
  int ti = 0;
  struct timeval tv;
  struct cpu_stat stat;
  double utils[TEST_NUM * 4];
  uint32_t freqs[TEST_NUM * 4][NUM_CPU];

  init_daemon(NULL);
  wake_lock();

  content = malloc(WRITE_SIZE);
  tv_begin = get_time(&tv);

  sleep(SLEEP_TIME);
  cpu_util_init(&stat);

  for (i = 0; i < TEST_NUM; ++i) {
    sprintf(file_name, "rffs-test-energy.data-%d-m", i);
    
    fd = open(file_name, O_WRONLY | O_CREAT, 0666);
    if (fd < 0) exit(-1000);

    sleep(SLEEP_TIME);
    wt_begin[ti] = get_time(&tv) - tv_begin;
    do_monit(&stat, utils + ti * 2, freqs[ti * 2]);
    for (j = 0; j < 10; ++j) {
      write(fd, content, WRITE_SIZE);
      if (fsync(fd)) exit(-2000);
    }
    wt_end[ti] = get_time(&tv) - tv_begin;
    do_monit(&stat, utils + ti * 2 + 1, freqs[ti * 2 + 1]);
    ++ti;
    close(fd);

    sprintf(file_name, "rffs-test-energy.data-%d-s", i);
    
    fd = open(file_name, O_WRONLY | O_CREAT, 0666);
    if (fd < 0) exit(-3000);

    sleep(SLEEP_TIME);
    wt_begin[ti] = get_time(&tv) - tv_begin;
    do_monit(&stat, utils + ti * 2, freqs[ti * 2]);
    for (j = 0; j < 10; ++j) {
      write(fd, content, WRITE_SIZE);
    }
    if (fsync(fd)) exit(-4000);
    
    wt_end[ti] = get_time(&tv) - tv_begin;
    do_monit(&stat, utils + ti * 2 + 1, freqs[ti * 2 + 1]);
    ++ti;
    close(fd);
  }

  free(content);
  fp = fopen("write-energy.int", "w");
  for (i = 0; i < TEST_NUM * 2; ++i) {
    fprintf(fp, "%.5f\t%.5f\n", wt_begin[i], wt_end[i]);
  }
  fflush(fp);
  fd = fileno(fp);
  fsync(fd);
  fclose(fp);

  fp = fopen("write-energy.stat", "w");
  for (i = 0; i < TEST_NUM * 4; ++i) {
    fprintf(fp, "%f", utils[i]);
    for (j = 0; j < NUM_CPU; ++j) {
      fprintf(fp, "\t%u", freqs[i][j]);
    }
    fprintf(fp, "\n");
  }
  fflush(fp);
  fd = fileno(fp);
  fsync(fd);
  fclose(fp);

  wake_unlock();
  return 0;
}

