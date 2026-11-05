#include <stdio.h>
#ifdef _WIN32
#include <windows.h>
#else
#include <unistd.h>
#endif
/******************************************************************************
 **                           Includes
 *****************************************************************************/
#include "DemoPFD_DemoPFD.h"
#include "FlightcontrolSystem_FlightControlIntegration.h"

extern outC_FlightcontrolSystem_FlightControlIntegration FlightcontrolSystem_FlightControlIntegration_context;
/******************************************************************************
 **                           File variables
 *****************************************************************************/
static swan_float32 MCP_Speed = 0.0f;
static swan_float32 MCP_Altitude = 0.0f;
static swan_bool MCP_Autopilot = 0;
static swan_bool MCP_UnlockRoll = 1;
static swan_float32 Altitude = 660.0f;
static swan_float32 Speed = 50.0f;
static swan_float32 SDY_Baro_Scale = 0.0f;
static swan_bool JV_Alti_Alarm = 0;
static swan_bool JV_Speed_Alarm = 0;
static GLint timer_value = 20;  /* integer: Time (in ms) between two frames */
static GLint pause = 0;         /* boolean: Enable/disable refresh of drawings */
/******************************************************************************
 **                           GLUT callbacks
 *****************************************************************************/

/*+ FUNCTION DESCRIPTION ----------------------------------------------
    NAME:           timer_callback
    DESCRIPTION:    Evaluates the time (in ms) between 2 frames
---------------------------------------------------------------------+*/

static void timer_callback(int value)
{
    if (!pause)
        glutPostRedisplay();
    glutTimerFunc(timer_value > 0 ? timer_value : 1, timer_callback, value);
}
/*+ FUNCTION DESCRIPTION ----------------------------------------------
    NAME:           display_callback
    DESCRIPTION:    Renders each frame
---------------------------------------------------------------------+*/

void display_callback(void)
{
		FlightcontrolSystem_FlightControlIntegration(MCP_Speed, MCP_Altitude, MCP_Autopilot, MCP_UnlockRoll, Altitude, Speed, &SDY_Baro_Scale, &JV_Alti_Alarm, &JV_Speed_Alarm, &FlightcontrolSystem_FlightControlIntegration_context);
}

int main(int argc, char* argv[])
{

	/* Step 1: Initialize the GLUT library and negotiate a session with the
		 window system */
	glutInit(&argc, argv);

	/* Step 2: Set the initial display mode, which is used when creating
		 top-level windows, subwindows, and overlays to determine the
		 OpenGL display mode for the to-be-created window or overlay */
	glutInitDisplayMode(GLUT_ALPHA | GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH | GLUT_STENCIL);

	/* Step 3: Set the initial window size in pixels */
	glutInitWindowSize(getW(), getH());


	/* Step 4: Create a top-level window. The name will be provided to the window
	   system as the window's name. Implicitly, the current window is set
	   to the newly created window. Each created window has a unique associated
	   OpenGL context. State changes to a window's associated OpenGL context
	   can be done immediately after the window is created. */
	glutCreateWindow(getSpecName());


	/* Step 5: Initialize all OGLX states and variables */
	oglx_init();
    /* Step 6: Initialize the Scade One and/or Display application */
	init_scene();

    /* Step 7: Define the GLUT callbacks for display, window, keyboard,
       mouse, etc. management */
    glutDisplayFunc(display_callback);
    // glutReshapeFunc(reshape_callback);
    // glutKeyboardFunc(keyboard_callback);

    // glutMouseFunc(mouse);
    // glutPassiveMotionFunc(mousePassiveMotion);
    // glutMotionFunc(mouseMotion);

    timer_callback(0);

    /* Final Step: Enter the GLUT event processing loop. Once called, this
       routine will never return. It will call as necessary any callbacks
       that have been registered. */
    glutMainLoop();

	return 0;
}
