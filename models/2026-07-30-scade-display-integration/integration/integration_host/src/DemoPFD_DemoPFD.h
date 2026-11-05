#ifndef SWAN_DemoPFD_DemoPFD_H_
#define SWAN_DemoPFD_DemoPFD_H_

#include "swan_types.h"
#include "oglx.h"

#include "GL/glut.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "sdy_events.h"

/* Include utilitary function oglxReadErrors to have a readable output of errors */
#include "oglxReadErrors.h"
/* Generated .H files for resource tables and specification properties */
#include "target_configuration.h"
#include "aol_texture_table.h"
// #include "aol_gradient_table.h"
#include "aol_color_table.h"
#include "aol_line_width_table.h"
#include "aol_line_stipple_table.h"
#include "aol_font_table.h"

/* TODO GENERATED INCLUDES: include in this section generated .H and .P files for each layer */
#include "aol_symbology_layer.h"

/* #include "aol_static_sequences.h"*/
/* END GENERATED INCLUDES */

typedef struct Ctx_DemoPFD_DemoPFD {
	int _dummy;
} outC_DemoPFD_DemoPFD;

extern void oglx_init();
extern void oglx_reset();
extern void DisplayOGLXErrors();
/* Interface to specific part */


extern int getW();
extern int getH();
extern float getRatioX();
extern float getRatioY();
extern const char* getSpecName();
extern void* getColorTable();
extern int getColorTableSize();
extern void* getLineWidthTable();
extern int getLineWidthTableSize();
extern void* getLineStippleTable();
extern int getLineStippleTableSize();
extern void* getFontTable();
extern int getTextureTableSize();
// extern int getGradientTableSize();

extern void init_scene();
extern void context_init();
extern void draw_init();

/* DemoPFD::DemoPFD */
extern void DemoPFD_DemoPFD(
  /* PN_PITCH_ANGLE */swan_float32 PN_PITCH_ANGLE,
  /* PN_ROLL_ANGLE */swan_float32 PN_ROLL_ANGLE,
  /* PN_ALTI */swan_float32 PN_ALTI,
  /* PN_AIRSPEED */swan_float32 PN_AIRSPEED,
  outC_DemoPFD_DemoPFD * restrict outC);

#ifndef SWAN_NO_EXTERN_CALL_TO_RESET
extern void DemoPFD_reset_DemoPFD(
	outC_DemoPFD_DemoPFD* restrict outC);
#endif /* SWAN_NO_EXTERN_CALL_TO_RESET */

extern void DemoPFD_init_DemoPFD(
	outC_DemoPFD_DemoPFD* restrict outC);



#endif /* SWAN_DemoPFD_DemoPFD_H_ */

