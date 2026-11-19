#include <stdio.h>
#include <stdlib.h>
#include "fopen_File.h"
#include "fclose_File.h"
#include "fread_File.h"

/* Data files are named "f-<id>" and are looked up in the directory given by the
 * FMS_DATA_DIR environment variable. The variable must hold an absolute path:
 * the simulator runs from a job-specific (possibly temporary) directory, so
 * relative paths are not reliable.
 *
 * If the file cannot be opened, an explicit message is printed and the file
 * handle is NULL: fread_File then returns 0 bytes and fclose_File does nothing,
 * so the model keeps running with an empty database instead of crashing. */
extern void fopen_File(swan_uint16 fname, access_File mode, t_File *f) {
    char m[2];
    switch (mode) {
        case Read:   m[0] = 'r'; break;
        case Write:  m[0] = 'w'; break;
        case Append: m[0] = 'a'; break;
        default:     m[0] = 'r'; break;
    }
    m[1] = '\0';

    *f = NULL;
    const char *dir = getenv("FMS_DATA_DIR");
    if (dir == NULL || dir[0] == '\0') {
        fprintf(stderr,
                "FMS: environment variable FMS_DATA_DIR is not set; cannot open f-%u.\n"
                "FMS: set it to the absolute path of the example 'data' folder, "
                "then restart Scade One (see README).\n",
                fname);
        fflush(stderr);
        return;
    }

    char path[1024];
    snprintf(path, sizeof(path), "%s/f-%u", dir, fname);
    *f = fopen(path, m);
    if (*f == NULL) {
        fprintf(stderr,
                "FMS: cannot open '%s'.\n"
                "FMS: check that FMS_DATA_DIR points to the example 'data' folder "
                "(see README).\n",
                path);
        fflush(stderr);
    }
}

extern void fclose_File(const t_File *f){
    if (*f != NULL) {
        fclose(*f);
    }
}

void swan_cp_t_File(t_File *dest, const t_File *src){
    *dest = *src;
}

extern void t_init_File(t_File *f){
    *f = NULL;
}

extern swan_bool swan_eq_t_File(const t_File *f1, const t_File *f2){
    return *f1 == *f2;
}

extern void fread_File(
  const t_File *f_in,
  t_File *f_out,
  array_u8_32768 * restrict buffer,
  swan_uint32 * restrict sz
  ){
    *f_out = *f_in;
    if (*f_in == NULL) {
        *sz = 0;
        return;
    }
    /* 32768 = File::BUFFER_SZ. Verified via codegen probe: this constant is inlined as a literal. */
    *sz = (swan_uint32)fread(buffer, sizeof(swan_uint8), 32768, *f_in);
}
