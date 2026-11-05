#include "swan_sensors.h"
#include "swan_consts.h"
#include "FlightcontrolSystem_FlightControlIntegration.h"
#include "DemoPFD_DemoPFD.h"


static sgl_type_statemachine glob_s_context;
outC_FlightcontrolSystem_FlightControlIntegration FlightcontrolSystem_FlightControlIntegration_context;

static GLenum glErrorStatus;    /* enum: OpenGL error index */
int g_latest_w = 0;
int g_latest_h = 0;
aol_typ_symbology_layer symbology_layer_ctx;

/*+ FUNCTIONS DESCRIPTION ----------------------------------------------
	NAME:           getW / getH / getRatioX / getRatioY / getSpecName
	DESCRIPTION:    Return respectively:
						- the width (in user units) of layers
						- the height (in user units) of layers
						- the X ratio of layers
						- the Y ratio of layers
						- the specification name
					as generated in the target_configuration.c file
---------------------------------------------------------------------+*/

int getW()
{
	return target_screen_width;
}

int getH()
{
	return target_screen_height;
}

float getRatioX()
{
	return (float)ratio_x;
}

float getRatioY()
{
	return (float)ratio_y;
}

const char* getSpecName()
{
	return "sampleScadeDisplayScadeOneIntegration";
}


/*+ FUNCTIONS DESCRIPTION ----------------------------------------------
	NAME:           getColorTable / getLineWidthTable / getLineStippleTable /
					getFontTable
	DESCRIPTION:    Return respectively:
						- the color table
						- the line width table
						- the line stipple table
						- the font table
					as generated from resource tables
---------------------------------------------------------------------+*/

void* getColorTable()
{
	return (void*)aol_color_table;
}

int getColorTableSize()
{
	return aol_color_table_size;
}

void* getLineWidthTable()
{
	return (void*)aol_line_width_table;
}

int getLineWidthTableSize()
{
	return aol_line_width_table_size;
}

void* getLineStippleTable()
{
	return (void*)aol_line_stipple_table;
}

int getLineStippleTableSize()
{
	return aol_line_stipple_table_size;
}

void* getFontTable(void)
{
	return (void*)(&aol_font_table);
}

int getTextureTableSize()
{
	return aol_texture_table_size;
}

// int getGradientTableSize()
// {
// 	return aol_gradient_table_size;
// }



/*+ FUNCTION DESCRIPTION ----------------------------------------------
	NAME:           oglx_init
	DESCRIPTION:    Complete initialization sequence for OGLX
---------------------------------------------------------------------+*/

void oglx_init()
{
	/* Initialize OGLX */
	static SGLbyte glob_tub_texture_buffer[4 * SGL_TEXTURE_MAX_WIDTH * SGL_TEXTURE_MAX_HEIGHT];
	sgl_texture_attrib* glob_texture_attrib = malloc(sizeof(sgl_texture_attrib) * getTextureTableSize());
	// sgl_gradient_attrib* glob_gradient_attrib = malloc(sizeof(sgl_gradient_attrib) * getGradientTableSize());
	static sgl_parameters lParameters;

	lParameters.ul_screen_width = getW();
	lParameters.ul_screen_height = getH();
	lParameters.pb_texture_buffer = glob_tub_texture_buffer;
	lParameters.ul_texture_max_width = SGL_TEXTURE_MAX_WIDTH;
	lParameters.ul_texture_max_height = SGL_TEXTURE_MAX_HEIGHT;
	lParameters.p_texture_attrib = glob_texture_attrib;
	lParameters.ul_number_of_textures = getTextureTableSize();
	lParameters.p_gradient_attrib = NULL;
	lParameters.ul_number_of_gradients = 0;

	sglInit(&glob_s_context, &lParameters);

	/* Load the color table */
	sglColorPointerf(getColorTable(), getColorTableSize());

	/* Set the OGLX line mode (RAW/SMOOTH) and load the corresponding line width table */
	sglSetRenderMode(SGL_RAW_OPENGL_LINES);
	/*sglSetRenderMode(SGL_SMOOTH_LINES);*/


	sglLineWidthPointerf(getLineWidthTable(), getLineWidthTableSize());

	/* Load the line stipple table */
	sglLineStipplePointer(getLineStippleTable(), getLineStippleTableSize());

	/* Load the fonts table */
	sgluLoadFonts(getFontTable());

	glShadeModel(GL_FLAT);

	sglViewport(0L, 0L, getW(), getH());
	sglOrtho(0, (float)(getW() * getRatioX() / 1.0F), 0, (float)(getH() * getRatioY() / 1.0F));

	/* Check if there is an OpenGL error after OGLX initialization */
	glErrorStatus = glGetError();
	if (glErrorStatus != GL_NO_ERROR) {
		printf("\nError %d raised during OGLX initialization\n\n", glErrorStatus);
	}

	g_latest_w = getW();
	g_latest_h = getH();
}

/*+ FUNCTION DESCRIPTION ----------------------------------------------
	NAME:           oglx_reset
	DESCRIPTION:    Resets the OGLX state
---------------------------------------------------------------------+*/

void oglx_reset()
{
	sglReset();
	sglViewport(0L, 0L, g_latest_w, g_latest_h);
	sglOrtho(0, (float)(getW() * getRatioX() / 1.0F), 0, (float)(getH() * getRatioY() / 1.0F));

	/* Check if there is an OpenGL error after OGLX reset */
	glErrorStatus = glGetError();
	if (glErrorStatus != GL_NO_ERROR) {
		printf("\nError %d raised during OGLX reset\n\n", glErrorStatus);
	}
}

/*+ FUNCTION DESCRIPTION ----------------------------------------------
	NAME:           DisplayOGLXErrors
	DESCRIPTION:   Displays OGLX errors to standard output
---------------------------------------------------------------------+*/
void DisplayOGLXErrors()
{
	static SGLuint32 loc_errors_number = 0;
	SGLuint32 loc_last_errors_number = 0;
	SGLuint32 loc_errors[SGL_ERROR_MAX][2];

	/*  OGLX interface sglGetErrors fills the input table with the 32 first errors since the start of the application or since last call to sgl ClearErrors */
	SGLbyte loc_b_status = sglGetErrors((SGLulong*)loc_errors, &loc_last_errors_number);

	if (loc_last_errors_number != loc_errors_number) {
		loc_errors_number = loc_last_errors_number;

		/* Fill the last error index only if there is at least one error */
		if (loc_b_status != SGL_NO_ERROR) {
			SGLulong i = 0;

			printf("**************************************************************\n");
			printf("\n\nNumber of OGLX stored errors: %d\n", (int)loc_errors_number);
			for (i = 0; i < loc_errors_number; i++) {
				/* Utilitary function oglxGetErrorDefinition provides additional informations on the detected errors */
				oglx_error_definition loc_error = oglxGetErrorDefinition(loc_errors[i][0]);
				printf("\nError number %d\n", (int)i + 1);
				/* Print outputs provided by sglGetErrors */
				printf("Error ID: %d, Parameter value: %d\n", (int)loc_errors[i][0], (int)loc_errors[i][1]);
				/* Print outputs provided by oglxReadErrors */
				printf("Error Name: %s\nRationale: %s\nParameter name: %s\nParameter value: %d\n",
					loc_error.s_error_name, loc_error.s_rationale, loc_error.s_parameter_name, (int)loc_errors[i][1]);
			}
		}
		else {
			printf("**************************************************************\n");
			printf("\n\nNo OGLX error.\n");
		}
	}
}

void init_scene()
{
	/* Initialize root module context */
	FlightcontrolSystem_init_FlightControlIntegration(&FlightcontrolSystem_FlightControlIntegration_context);
	aol_symbology_layer_init(&symbology_layer_ctx);
	aol_texture_table();
	// aol_gradient_table();
	// aol_static_sequences();
}

/* DemoPFD::DemoPFD */
void DemoPFD_DemoPFD(
  /* PN_PITCH_ANGLE */swan_float32 PN_PITCH_ANGLE,
  /* PN_ROLL_ANGLE */swan_float32 PN_ROLL_ANGLE,
  /* PN_ALTI */swan_float32 PN_ALTI,
  /* PN_AIRSPEED */swan_float32 PN_AIRSPEED,
  outC_DemoPFD_DemoPFD * restrict outC)
{
	aol_typ_symbology_layer displayContext;

    oglx_reset();
    /* BHVR_Pointer(&pointer_event); */

    /* Clear OpenGL colors, masks and buffers */
    glClearColor(0.f, 0.f, 0.f, 0.0f);
    glClear(GL_COLOR_BUFFER_BIT);

    /* Render the graphical scene */
    
	(void)outC;
	aol_symbology_layer_init(&displayContext);
	// aol_symbology_layer_S_valuedegf32(&displayContext, valuedegf32);
	aol_symbology_layer_S_PN_AIRSPEED(&displayContext, PN_AIRSPEED);
	aol_symbology_layer_S_PN_ALTI(&displayContext, PN_ALTI);
	aol_symbology_layer_S_PN_PITCH_ANGLE(&displayContext, PN_PITCH_ANGLE);
	aol_symbology_layer_S_PN_ROLL_ANGLE(&displayContext, PN_ROLL_ANGLE);
	aol_symbology_layer_draw(&displayContext, 0L);
	   
	
    /* Check if there is an OpenGL error after drawing of the scene */
    glErrorStatus = glGetError();
    if (glErrorStatus != GL_NO_ERROR) {
        printf("\nError %d raised during OGLX reset\n\n", glErrorStatus);
    }


    /* Swap OpenGL buffers at the end of scene rendering */
    glutSwapBuffers();


    /* Display OGLX Errors to standard output */
    DisplayOGLXErrors();

    /* To clear OGLX errors buffer, call sglClearErrors */
    /* sglClearErrors(); */
	
}

void DemoPFD_init_DemoPFD(
	outC_DemoPFD_DemoPFD* restrict outC)
{
	/* Initialize specification context */
	outC->_dummy = 0;
}


#ifndef SWAN_NO_EXTERN_CALL_TO_RESET
void DemoPFD_reset_DemoPFD(
	outC_DemoPFD_DemoPFD* restrict outC)
{
	/* Reset specification context */
	outC->_dummy = 0;
}
#endif /* SWAN_NO_EXTERN_CALL_TO_RESET */
