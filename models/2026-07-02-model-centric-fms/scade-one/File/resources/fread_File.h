#ifndef FREAD_FILE_H
#define FREAD_FILE_H

#include "swan_types.h"

extern void fread_File(
  const t_File *f_in,
  t_File *f_out,
  array_u8_32768 * restrict buffer,
  swan_uint32 * restrict sz);

#endif /* FREAD_FILE_H */
