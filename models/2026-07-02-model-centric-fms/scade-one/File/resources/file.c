#include <stdlib.h>
#include "fopen_File.h"
#include "fclose_File.h"
#include "fread_File.h"




extern void fopen_File(swan_uint16 fname, access_File mode, t_File *f) {
    char m[2];
    switch (mode) {
        case Read:   m[0] = 'r'; break;
        case Write:  m[0] = 'w'; break;
        case Append: m[0] = 'a'; break;
    }
    m[1] = '\0';

    /* Data files are named "f-<id>" and looked up in the directory given by the
     * FMS_DATA_DIR environment variable (current directory if unset). */
    const char *dir = getenv("FMS_DATA_DIR");
    char path[512];
    if (dir == NULL || dir[0] == '\0') {
        dir = ".";
    }
    snprintf(path, sizeof(path), "%s/f-%u", dir, fname);

    /* Scoping decision: NULL return from fopen (file not found) is not handled.
     * The model assumes the file exists at the expected path. */
    *f = fopen(path, m);
}

extern void fclose_File(const t_File *f){
    fclose(*f);
}

void swan_cp_t_File(t_File *dest, const t_File *src){
    *dest = *src;
}

extern void t_init_File(t_File *f){
    // Nothing to do to init a file
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
        /* 32768 = File::BUFFER_SZ. Verified via codegen probe: this constant is inlined as a literal. */
    *sz = fread(buffer, sizeof(swan_uint8), 32768, *f_in);
    *f_out = *f_in;
}
