/* $********** SCADE Suite KCG 32-bit 6.6.4 (build i3) **********
** Command: kcg664.exe -target_dir ../Code/Generated -target C -name_length 128 -significance_length 127 -user_config imported_user_macros.h -root CheckButton,AlphaNumKeypad,NumKeypad,PushButton,ScrollList,Slider,TextEditBox,ToggleButton,MultilineEditBox,PopUpPanel,ScrollBar,NumericEditBox,RadioBox,PopUpMenu,ComboBox,VirtualKeyboard,Scale,PiecewiseTranslation,PiecewiseRotation,Curve,RollingDigits,Animations,GestureDrag,GestureFlick,GesturePinchExpandRotate,GesturePressHold,GestureTap,Joystick,Signals,InfiniteKnob,Knob,RotarySwitch,GraphTimed,Tree,MultiColumn,RampSignal ../Widgets/Suite/Common/Pointer.xscade ../Widgets/Suite/Common/Util.xscade ../Widgets/Suite/Common/Strings.xscade ../Widgets/Suite/Common/libwidgets.xscade ../Widgets/Suite/Common/Math.xscade ../Widgets/Suite/Common/Angles.xscade ../Widgets/Suite/CheckButton/CheckButton.xscade ../Widgets/Suite/AlphaNumKeypad/AlphaNumKeypad.xscade ../Widgets/Suite/Animations/Animations.xscade ../Widgets/Suite/GestureDrag/GestureDrag.xscade ../Widgets/Suite/GestureFlick/GestureFlick.xscade ../Widgets/Suite/GesturePinchExpandRotate/GesturePinchExpandRotate.xscade ../Widgets/Suite/GesturePressHold/GesturePressHold.xscade ../Widgets/Suite/GestureTap/GestureTap.xscade ../Widgets/Suite/InfiniteKnob/InfiniteKnob.xscade ../Widgets/Suite/Knob/Knob.xscade ../Widgets/Suite/Joystick/Joystick.xscade ../Widgets/Suite/NumKeypad/NumKeypad.xscade ../Widgets/Suite/PushButton/PushButton.xscade ../Widgets/Suite/ScrollList/ScrollList.xscade ../Widgets/Suite/Slider/Slider.xscade ../Widgets/Suite/TextEditBox/TextEditBox.xscade ../Widgets/Suite/ToggleButton/ToggleButton.xscade ../Widgets/Suite/MultilineEditBox/MultilineEditBox.xscade ../Widgets/Suite/Scale/Scale.xscade ../Widgets/Suite/PopUpPanel/PopUpPanel.xscade ../Widgets/Suite/ScrollBar/ScrollBar.xscade ../Widgets/Suite/NumericEditBox/NumericEditBox.xscade ../Widgets/Suite/RadioBox/RadioBox.xscade ../Widgets/Suite/PopUpMenu/PopUpMenu.xscade ../Widgets/Suite/ComboBox/ComboBox.xscade ../Widgets/Suite/VirtualKeyboard/VirtualKeyboard.xscade ../Widgets/Suite/PiecewiseRotation/PiecewiseRotation.xscade ../Widgets/Suite/PiecewiseTranslation/PiecewiseTranslation.xscade ../Widgets/Suite/RollingDigits/RollingDigits.xscade ../Widgets/Suite/Signals/Signals.xscade ../Widgets/Suite/Curve/Curve.xscade ../Widgets/Suite/GraphTimed/GraphTimed.xscade ../Widgets/Suite/RotarySwitch/RotarySwitch.xscade ../Widgets/Suite/Tree/Tree.xscade ../Widgets/Suite/MultiColumn/MultiColumn.xscade ../Widgets/Suite/RampSignal/RampSignal.xscade
** Generation date: 2025-09-23T22:03:49
*************************************************************$ */
#ifndef KCG_PushButton_H_
#define KCG_PushButton_H_

#include "wid_kcg_types.h"

/* ========================  input structure  ====================== */
typedef struct {
  kcg_int32 /* EmitCondition/ */ EmitCondition;
  kcg_bool /* MouseInside/ */ MouseInside;
  kcg_bool /* MousePressed/ */ MousePressed;
  kcg_bool /* MouseReleased/ */ MouseReleased;
  kcg_bool /* KeyPressed/ */ KeyPressed;
  kcg_int32 /* KeyCode/ */ KeyCode;
  kcg_bool /* KeyReleased/ */ KeyReleased;
} inC_PushButton;

/* =====================  no output structure  ====================== */

/* ========================  context type  ========================= */
typedef struct {
  /* ---------------------------  outputs  --------------------------- */
  kcg_bool /* Selection/ */ Selection;
  kcg_bool /* ButtonPressed/ */ ButtonPressed;
  /* -----------------------  no local probes  ----------------------- */
  /* -----------------------  no local memory  ----------------------- */
  /* -------------------- no sub nodes' contexts  -------------------- */
  /* ----------------- no clocks of observable data ------------------ */
} outC_PushButton;

/* ===========  node initialization and cycle functions  =========== */
/* PushButton/ */
extern void PushButton(inC_PushButton *inC, outC_PushButton *outC);

#ifndef KCG_NO_EXTERN_CALL_TO_RESET
extern void PushButton_reset(outC_PushButton *outC);
#endif /* KCG_NO_EXTERN_CALL_TO_RESET */

#ifndef KCG_USER_DEFINED_INIT
extern void PushButton_init(outC_PushButton *outC);
#endif /* KCG_USER_DEFINED_INIT */



#endif /* KCG_PushButton_H_ */
/* $********** SCADE Suite KCG 32-bit 6.6.4 (build i3) **********
** PushButton.h
** Generation date: 2025-09-23T22:03:49
*************************************************************$ */

