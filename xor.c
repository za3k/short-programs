// 'xor'
// by zachary vance, released into the public domain (see CC0 1.0 license)
// Given two streams (exactly) as filenames on the command line, print to stdout the 'xor' of the two files. Pads the shorter file with zeros, so the length of the output is always the length of the longer file
#include <stdio.h>
#include <unistd.h>
#include <string.h>

#define MAX_FILES 10
#define BUFFER 1024

int main(int argc, char *argv[]){
  FILE *fp[MAX_FILES];
  char inbytes[BUFFER], outbytes[BUFFER];
  int bytes_read, max_bytes_read;
  int files, files_done;
  int f,b;
  
  files = argc-1;
  if (files < 2) {
    printf("usage: xor FILE1 FILE2\n");
    return 2;
  } else if (files > MAX_FILES) {
    printf("Too many files. Please recompile with a faster number of files maximum\n");
    return 2;
  }
  
  for (f=0;f<files;f++){
    fp[f]=fopen(argv[f+1],"rb");
    if(fp[f] == NULL){
      printf("File %d not found: %s\n", f, argv[f+1]);
      return 1;
    }
  }

  while(1) {
    files_done=0;
    for(f=0;f<files;f++)
      if(feof(fp[f])) files_done++;
    if(files == files_done) break;

    memset(outbytes, 0, BUFFER);
    max_bytes_read=0;
    for(f=0;f<files;f++) {
      bytes_read = fread(&inbytes, 1, BUFFER, fp[f]);
      for(b=0;b<bytes_read;b++) outbytes[b] ^= inbytes[b];
      if(bytes_read > max_bytes_read) max_bytes_read=bytes_read;
    }

    write(1, outbytes, max_bytes_read);
  }

  for(f=0;f<files;f++) fclose(fp[f]);

  return 0;
}
