#include <stdio.h>



#ifndef FILE_H_
#define FILE_H_

typedef FILE * t_File;

extern void t_init_File(t_File *swan_c1);
void swan_cp_t_File(t_File *dest, const t_File *src);
extern swan_bool swan_eq_t_File(const t_File *swan_c1, const t_File *swan_c2);

#endif /* FILE_H_ */