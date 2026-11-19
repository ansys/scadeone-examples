#include "to_u32_Float32.h"
#include "of_u32_Float32.h"

extern swan_uint32 to_u32_Float32(swan_float32 f){
    union {swan_float32 f; swan_uint32 u;} x;
    x.f = f;
    return x.u;
}

extern swan_float32 of_u32_Float32(swan_uint32 u){
    union {swan_float32 f; swan_uint32 u;} x;
    x.u = u;
    return x.f;
}

