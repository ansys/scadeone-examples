#include "swan_types.h"
#include "stdlib.h"


/* Random integer */
swan_int32 random_c32_random(swan_int32 min, swan_int32 max) {
    return min + rand() % (max - min + 1);
}

swan_int64 random_c64_random(swan_int64 min, swan_int64 max) {
    return min + rand() % (max - min + 1);
}


/* Random occurrence of 'true' with a given probability (among 0-100) */
swan_bool random_true_random(swan_int32 probability) {
    return (swan_bool)(rand() * 100 <= RAND_MAX * probability);
}