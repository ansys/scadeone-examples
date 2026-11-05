/*
 * Copyright (C) 2024  ANSYS, Inc. ALL RIGHTS RESERVED.
 * This source file may be used and distributed without restriction provided that this
 * copyright statement is not removed from the file and that any derivative work 
 * contains this copyright notice.
 * 
 * Warranty
 * ANSYS, Inc makes no warranty of any kind with regard to the use of this Software, 
 * either expressed or implied, including, but not limited to the fitness 
 * for a particular purpose.
 */

#include "math.h"

/** Math::Common */

/* Cbrt */
#define Cbrt32_Math_Common(In) ((swan_float32) cbrtf((swan_float32) In))
#define Cbrt64_Math_Common(In) ((swan_float64) cbrt((swan_float64) In))

/* Ceil */
#define Ceil32_Math_Common(In) ((swan_float32) ceilf((swan_float32) In))
#define Ceil64_Math_Common(In) ((swan_float64) ceil((swan_float64) In))

/* Exp */
#define Exp32_Math_Common(In) ((swan_float32) expf((swan_float32) In))
#define Exp64_Math_Common(In) ((swan_float64) exp((swan_float64) In))

/* Floor */
#define Floor32_Math_Common(In) ((swan_float32) floorf((swan_float32) In))
#define Floor64_Math_Common(In) ((swan_float64) floor((swan_float64) In))

/* Fmod */
#define Fmod32_Math_Common(In1, In2) ((swan_float32) fmodf((swan_float32) In1, (swan_float32) In2))
#define Fmod64_Math_Common(In1, In2) ((swan_float64) fmod((swan_float64) In1, (swan_float64) In2))

/* Log10 */
#define Log1032_Math_Common(In) ((swan_float32) log10f((swan_float32) In))
#define Log1064_Math_Common(In) ((swan_float64) log10((swan_float64) In))

/* Log2 */
#define Log232_Math_Common(In) ((swan_float32) log2f((swan_float32) In))
#define Log264_Math_Common(In) ((swan_float64) log2((swan_float64) In))

/* Log */
#define Log32_Math_Common(In) ((swan_float32) logf((swan_float32) In))
#define Log64_Math_Common(In) ((swan_float64) log((swan_float64) In))

/* Pow */
#define Pow32_Math_Common(In1, In2) ((swan_float32) powf((swan_float32) In1, (swan_float32) In2))
#define Pow64_Math_Common(In1, In2) ((swan_float64) pow((swan_float64) In1, (swan_float64) In2))

/* Sqrt */
#define Sqrt32_Math_Common(In) ((swan_float32) sqrtf((swan_float32) In))
#define Sqrt64_Math_Common(In) ((swan_float64) sqrt((swan_float64) In))

/* Trunc */
#define Trunc32_Math_Common(In) ((swan_float32) truncf((swan_float32) In))
#define Trunc64_Math_Common(In) ((swan_float64) trunc((swan_float64) In))


/** Math::Trigo::StdC */
/* ArcCosine */
#define ArcCosine32_Math_Trigo_StdC(In) ((swan_float32) acosf((swan_float32) In))
#define ArcCosine64_Math_Trigo_StdC(In) ((swan_float64) acos((swan_float64) In))

/* ArcSine */
#define ArcSine32_Math_Trigo_StdC(In) ((swan_float32) asinf((swan_float32) In))
#define ArcSine64_Math_Trigo_StdC(In) ((swan_float64) asin((swan_float64) In))

/* ArcTan2 */
#define ArcTan232_Math_Trigo_StdC(In1, In2) ((swan_float32) atan2f((swan_float32) In1, (swan_float32) In2))
#define ArcTan264_Math_Trigo_StdC(In1, In2) ((swan_float64) atan2((swan_float64) In1, (swan_float64) In2))

/* ArcTan */
#define ArcTan32_Math_Trigo_StdC(In) ((swan_float32) atanf((swan_float32) In))
#define ArcTan64_Math_Trigo_StdC(In) ((swan_float64) atan((swan_float64) In))

/* Cosine */
#define Cosine32_Math_Trigo_StdC(In) ((swan_float32) cosf((swan_float32) In))
#define Cosine64_Math_Trigo_StdC(In) ((swan_float64) cos((swan_float64) In))

/* Sine */
#define Sine32_Math_Trigo_StdC(In) ((swan_float32) sinf((swan_float32) In))
#define Sine64_Math_Trigo_StdC(In) ((swan_float64) sin((swan_float64) In))

/* Tan */
#define Tan32_Math_Trigo_StdC(In) ((swan_float32) tanf((swan_float32) In))
#define Tan64_Math_Trigo_StdC(In) ((swan_float64) tan((swan_float64) In))
