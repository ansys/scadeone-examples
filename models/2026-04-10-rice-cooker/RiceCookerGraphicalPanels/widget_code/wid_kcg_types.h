/* $********** SCADE Suite KCG 32-bit 6.6.4 (build i3) **********
** Command: kcg664.exe -target_dir ../Code/Generated -target C -name_length 128 -significance_length 127 -user_config imported_user_macros.h -root CheckButton,AlphaNumKeypad,NumKeypad,PushButton,ScrollList,Slider,TextEditBox,ToggleButton,MultilineEditBox,PopUpPanel,ScrollBar,NumericEditBox,RadioBox,PopUpMenu,ComboBox,VirtualKeyboard,Scale,PiecewiseTranslation,PiecewiseRotation,Curve,RollingDigits,Animations,GestureDrag,GestureFlick,GesturePinchExpandRotate,GesturePressHold,GestureTap,Joystick,Signals,InfiniteKnob,Knob,RotarySwitch,GraphTimed,Tree,MultiColumn,RampSignal ../Widgets/Suite/Common/Pointer.xscade ../Widgets/Suite/Common/Util.xscade ../Widgets/Suite/Common/Strings.xscade ../Widgets/Suite/Common/libwidgets.xscade ../Widgets/Suite/Common/Math.xscade ../Widgets/Suite/Common/Angles.xscade ../Widgets/Suite/CheckButton/CheckButton.xscade ../Widgets/Suite/AlphaNumKeypad/AlphaNumKeypad.xscade ../Widgets/Suite/Animations/Animations.xscade ../Widgets/Suite/GestureDrag/GestureDrag.xscade ../Widgets/Suite/GestureFlick/GestureFlick.xscade ../Widgets/Suite/GesturePinchExpandRotate/GesturePinchExpandRotate.xscade ../Widgets/Suite/GesturePressHold/GesturePressHold.xscade ../Widgets/Suite/GestureTap/GestureTap.xscade ../Widgets/Suite/InfiniteKnob/InfiniteKnob.xscade ../Widgets/Suite/Knob/Knob.xscade ../Widgets/Suite/Joystick/Joystick.xscade ../Widgets/Suite/NumKeypad/NumKeypad.xscade ../Widgets/Suite/PushButton/PushButton.xscade ../Widgets/Suite/ScrollList/ScrollList.xscade ../Widgets/Suite/Slider/Slider.xscade ../Widgets/Suite/TextEditBox/TextEditBox.xscade ../Widgets/Suite/ToggleButton/ToggleButton.xscade ../Widgets/Suite/MultilineEditBox/MultilineEditBox.xscade ../Widgets/Suite/Scale/Scale.xscade ../Widgets/Suite/PopUpPanel/PopUpPanel.xscade ../Widgets/Suite/ScrollBar/ScrollBar.xscade ../Widgets/Suite/NumericEditBox/NumericEditBox.xscade ../Widgets/Suite/RadioBox/RadioBox.xscade ../Widgets/Suite/PopUpMenu/PopUpMenu.xscade ../Widgets/Suite/ComboBox/ComboBox.xscade ../Widgets/Suite/VirtualKeyboard/VirtualKeyboard.xscade ../Widgets/Suite/PiecewiseRotation/PiecewiseRotation.xscade ../Widgets/Suite/PiecewiseTranslation/PiecewiseTranslation.xscade ../Widgets/Suite/RollingDigits/RollingDigits.xscade ../Widgets/Suite/Signals/Signals.xscade ../Widgets/Suite/Curve/Curve.xscade ../Widgets/Suite/GraphTimed/GraphTimed.xscade ../Widgets/Suite/RotarySwitch/RotarySwitch.xscade ../Widgets/Suite/Tree/Tree.xscade ../Widgets/Suite/MultiColumn/MultiColumn.xscade ../Widgets/Suite/RampSignal/RampSignal.xscade
** Generation date: 2025-09-23T22:03:49
*************************************************************$ */
#ifndef WID_KCG_TYPES_H_
#define WID_KCG_TYPES_H_

#ifndef KCG_NO_STDDEF_H
#include "stddef.h"
#endif /* KCG_NO_STDDEF_H */

#define KCG_MAPW_CPY

#include "imported_user_macros.h"

#ifndef kcg_char
#define kcg_char kcg_char
typedef char kcg_char;
#endif /* kcg_char */

#ifndef kcg_bool
#define kcg_bool kcg_bool
typedef unsigned char kcg_bool;
#endif /* kcg_bool */

#ifndef kcg_float32
#define kcg_float32 kcg_float32
typedef float kcg_float32;
#endif /* kcg_float32 */

#ifndef kcg_float64
#define kcg_float64 kcg_float64
typedef double kcg_float64;
#endif /* kcg_float64 */

#ifndef kcg_size
#define kcg_size kcg_size
typedef ptrdiff_t kcg_size;
#endif /* kcg_size */

#ifndef kcg_uint64
#define kcg_uint64 kcg_uint64
typedef unsigned long long kcg_uint64;
#endif /* kcg_uint64 */

#ifndef kcg_uint32
#define kcg_uint32 kcg_uint32
typedef unsigned long kcg_uint32;
#endif /* kcg_uint32 */

#ifndef kcg_uint16
#define kcg_uint16 kcg_uint16
typedef unsigned short kcg_uint16;
#endif /* kcg_uint16 */

#ifndef kcg_uint8
#define kcg_uint8 kcg_uint8
typedef unsigned char kcg_uint8;
#endif /* kcg_uint8 */

#ifndef kcg_int64
#define kcg_int64 kcg_int64
typedef signed long long kcg_int64;
#endif /* kcg_int64 */

#ifndef kcg_int32
#define kcg_int32 kcg_int32
typedef signed long kcg_int32;
#endif /* kcg_int32 */

#ifndef kcg_int16
#define kcg_int16 kcg_int16
typedef signed short kcg_int16;
#endif /* kcg_int16 */

#ifndef kcg_int8
#define kcg_int8 kcg_int8
typedef signed char kcg_int8;
#endif /* kcg_int8 */

#ifndef kcg_lit_float32
#define kcg_lit_float32(kcg_C1) ((kcg_float32) (kcg_C1))
#endif /* kcg_lit_float32 */

#ifndef kcg_lit_float64
#define kcg_lit_float64(kcg_C1) ((kcg_float64) (kcg_C1))
#endif /* kcg_lit_float64 */

#ifndef kcg_lit_size
#define kcg_lit_size(kcg_C1) ((kcg_size) (kcg_C1))
#endif /* kcg_lit_size */

#ifndef kcg_lit_uint64
#define kcg_lit_uint64(kcg_C1) ((kcg_uint64) (kcg_C1))
#endif /* kcg_lit_uint64 */

#ifndef kcg_lit_uint32
#define kcg_lit_uint32(kcg_C1) ((kcg_uint32) (kcg_C1))
#endif /* kcg_lit_uint32 */

#ifndef kcg_lit_uint16
#define kcg_lit_uint16(kcg_C1) ((kcg_uint16) (kcg_C1))
#endif /* kcg_lit_uint16 */

#ifndef kcg_lit_uint8
#define kcg_lit_uint8(kcg_C1) ((kcg_uint8) (kcg_C1))
#endif /* kcg_lit_uint8 */

#ifndef kcg_lit_int64
#define kcg_lit_int64(kcg_C1) ((kcg_int64) (kcg_C1))
#endif /* kcg_lit_int64 */

#ifndef kcg_lit_int32
#define kcg_lit_int32(kcg_C1) ((kcg_int32) (kcg_C1))
#endif /* kcg_lit_int32 */

#ifndef kcg_lit_int16
#define kcg_lit_int16(kcg_C1) ((kcg_int16) (kcg_C1))
#endif /* kcg_lit_int16 */

#ifndef kcg_lit_int8
#define kcg_lit_int8(kcg_C1) ((kcg_int8) (kcg_C1))
#endif /* kcg_lit_int8 */

#ifndef kcg_false
#define kcg_false ((kcg_bool) 0)
#endif /* kcg_false */

#ifndef kcg_true
#define kcg_true ((kcg_bool) 1)
#endif /* kcg_true */

#ifndef kcg_lsl_uint64
#define kcg_lsl_uint64(kcg_C1, kcg_C2)                                        \
  ((kcg_uint64) ((kcg_C1) << (kcg_C2)) & 0xffffffffffffffff)
#endif /* kcg_lsl_uint64 */

#ifndef kcg_lsl_uint32
#define kcg_lsl_uint32(kcg_C1, kcg_C2)                                        \
  ((kcg_uint32) ((kcg_C1) << (kcg_C2)) & 0xffffffff)
#endif /* kcg_lsl_uint32 */

#ifndef kcg_lsl_uint16
#define kcg_lsl_uint16(kcg_C1, kcg_C2)                                        \
  ((kcg_uint16) ((kcg_C1) << (kcg_C2)) & 0xffff)
#endif /* kcg_lsl_uint16 */

#ifndef kcg_lsl_uint8
#define kcg_lsl_uint8(kcg_C1, kcg_C2)                                         \
  ((kcg_uint8) ((kcg_C1) << (kcg_C2)) & 0xff)
#endif /* kcg_lsl_uint8 */

#ifndef kcg_lnot_uint64
#define kcg_lnot_uint64(kcg_C1) ((kcg_C1) ^ 0xffffffffffffffff)
#endif /* kcg_lnot_uint64 */

#ifndef kcg_lnot_uint32
#define kcg_lnot_uint32(kcg_C1) ((kcg_C1) ^ 0xffffffff)
#endif /* kcg_lnot_uint32 */

#ifndef kcg_lnot_uint16
#define kcg_lnot_uint16(kcg_C1) ((kcg_C1) ^ 0xffff)
#endif /* kcg_lnot_uint16 */

#ifndef kcg_lnot_uint8
#define kcg_lnot_uint8(kcg_C1) ((kcg_C1) ^ 0xff)
#endif /* kcg_lnot_uint8 */

#ifndef kcg_assign
#include "kcg_assign.h"
#endif /* kcg_assign */

#ifndef kcg_assign_struct
#define kcg_assign_struct kcg_assign
#endif /* kcg_assign_struct */

#ifndef kcg_assign_array
#define kcg_assign_array kcg_assign
#endif /* kcg_assign_array */

/* Strings::EndOfLineKind/ */
typedef enum kcg_tag_EndOfLineKind_Strings {
  CR_Strings,
  LF_Strings,
  CRLF_Strings
} EndOfLineKind_Strings;
/* Animations/SM1: */
typedef enum kcg_tag_x7_SSM_TR_SM1 {
  SSM_TR_no_trans_SM1,
  SSM_TR_Idle_Idle_1_Idle_SM1,
  SSM_TR_Idle_Run_2_Idle_SM1,
  SSM_TR_Idle_Run_3_Idle_SM1,
  SSM_TR_Run_Run_1_1_Run_SM1,
  SSM_TR_Run_Run_2_1_Run_SM1,
  SSM_TR_Run_Run_1_2_Run_SM1,
  SSM_TR_Run_Run_2_2_Run_SM1,
  SSM_TR_Run_Idle_3_Run_SM1
} x7_SSM_TR_SM1;
/* Animations/SM1: */
typedef enum kcg_tag_x6_SSM_ST_SM1 {
  SSM_st_Idle_SM1,
  SSM_st_Run_SM1
} x6_SSM_ST_SM1;
/* InfiniteKnob/IfBlock:then:SM1: */
typedef enum kcg_tag_SSM_TR_SM1_then_IfBlock {
  SSM_TR_no_trans_SM1_then_IfBlock,
  SSM_TR_StBy_rotate_1_StBy_SM1_then_IfBlock,
  SSM_TR_rotate_StBy_1_rotate_SM1_then_IfBlock
} SSM_TR_SM1_then_IfBlock;
/* InfiniteKnob/IfBlock:then:SM1: */
typedef enum kcg_tag_SSM_ST_SM1_then_IfBlock {
  SSM_st_StBy_SM1_then_IfBlock,
  SSM_st_rotate_SM1_then_IfBlock
} SSM_ST_SM1_then_IfBlock;
/* Knob/IfBlock:then:behavior: */
typedef enum kcg_tag_x5_SSM_TR_behavior_then_IfBlock {
  x12_SSM_TR_no_trans_behavior_then_IfBlock,
  SSM_TR_StBy_MouseDown_1_StBy_behavior_then_IfBlock,
  SSM_TR_MouseDown_StBy_1_MouseDown_behavior_then_IfBlock
} x5_SSM_TR_behavior_then_IfBlock;
/* Knob/IfBlock:then:behavior: */
typedef enum kcg_tag_x4_SSM_ST_behavior_then_IfBlock {
  SSM_st_StBy_behavior_then_IfBlock,
  SSM_st_MouseDown_behavior_then_IfBlock
} x4_SSM_ST_behavior_then_IfBlock;
/* Joystick/SM1: */
typedef enum kcg_tag_x3_SSM_TR_SM1 {
  x11_SSM_TR_no_trans_SM1,
  SSM_TR_Pressed_Idle_1_Pressed_SM1,
  SSM_TR_Idle_Pressed_1_Idle_SM1
} x3_SSM_TR_SM1;
/* Joystick/SM1: */
typedef enum kcg_tag_x2_SSM_ST_SM1 {
  SSM_st_Pressed_SM1,
  x8_SSM_st_Idle_SM1
} x2_SSM_ST_SM1;
/* Pointer::EditBoxCursorVisibility/EditBoxCursorVisibility_SM: */
typedef enum kcg_tag_SSM_TR_EditBoxCursorVisibility_SM {
  SSM_TR_no_trans_EditBoxCursorVisibility_SM,
  SSM_TR_CursorVisible_CursorHidden_1_CursorVisible_EditBoxCursorVisibility_SM,
  SSM_TR_CursorHidden_CursorVisible_1_CursorHidden_EditBoxCursorVisibility_SM
} SSM_TR_EditBoxCursorVisibility_SM;
/* Pointer::EditBoxCursorVisibility/EditBoxCursorVisibility_SM: */
typedef enum kcg_tag_SSM_ST_EditBoxCursorVisibility_SM {
  SSM_st_CursorVisible_EditBoxCursorVisibility_SM,
  SSM_st_CursorHidden_EditBoxCursorVisibility_SM
} SSM_ST_EditBoxCursorVisibility_SM;
/* TextEditBox/TextEditBox_SM: */
typedef enum kcg_tag_SSM_TR_TextEditBox_SM {
  SSM_TR_no_trans_TextEditBox_SM,
  SSM_TR_NoEdit_Edit_1_NoEdit_TextEditBox_SM,
  SSM_TR_Edit_NoEdit_1_Edit_TextEditBox_SM
} SSM_TR_TextEditBox_SM;
/* TextEditBox/TextEditBox_SM: */
typedef enum kcg_tag_SSM_ST_TextEditBox_SM {
  SSM_st_NoEdit_TextEditBox_SM,
  SSM_st_Edit_TextEditBox_SM
} SSM_ST_TextEditBox_SM;
/* MultilineEditBox/MultilineEditBox_SM: */
typedef enum kcg_tag_SSM_TR_MultilineEditBox_SM {
  SSM_TR_no_trans_MultilineEditBox_SM,
  SSM_TR_NoEdit_Edit_1_NoEdit_MultilineEditBox_SM,
  SSM_TR_Edit_NoEdit_1_Edit_MultilineEditBox_SM
} SSM_TR_MultilineEditBox_SM;
/* MultilineEditBox/MultilineEditBox_SM: */
typedef enum kcg_tag_SSM_ST_MultilineEditBox_SM {
  SSM_st_NoEdit_MultilineEditBox_SM,
  SSM_st_Edit_MultilineEditBox_SM
} SSM_ST_MultilineEditBox_SM;
/* NumericEditBox/NumericEditBox_SM: */
typedef enum kcg_tag_SSM_TR_NumericEditBox_SM {
  SSM_TR_no_trans_NumericEditBox_SM,
  SSM_TR_NoEdit_Edit_1_NoEdit_NumericEditBox_SM,
  SSM_TR_Edit_NoEdit_1_Edit_NumericEditBox_SM
} SSM_TR_NumericEditBox_SM;
/* NumericEditBox/NumericEditBox_SM: */
typedef enum kcg_tag_SSM_ST_NumericEditBox_SM {
  SSM_st_NoEdit_NumericEditBox_SM,
  SSM_st_Edit_NumericEditBox_SM
} SSM_ST_NumericEditBox_SM;
/* VirtualKeyboard/SM1: */
typedef enum kcg_tag_SSM_TR_SM1 {
  x9_SSM_TR_no_trans_SM1,
  SSM_TR_running_wait_ACK_1_running_SM1,
  SSM_TR_wait_ACK_running_1_wait_ACK_SM1
} SSM_TR_SM1;
/* VirtualKeyboard/SM1: */
typedef enum kcg_tag_SSM_ST_SM1 {
  SSM_st_running_SM1,
  SSM_st_wait_ACK_SM1
} SSM_ST_SM1;
/* RotarySwitch/IfBlock:then:behavior: */
typedef enum kcg_tag_SSM_TR_behavior_then_IfBlock {
  SSM_TR_no_trans_behavior_then_IfBlock,
  SSM_TR_Change_Magnet_1_Change_behavior_then_IfBlock,
  SSM_TR_StBy_Change_1_StBy_behavior_then_IfBlock,
  SSM_TR_Magnet_StBy_1_Magnet_behavior_then_IfBlock
} SSM_TR_behavior_then_IfBlock;
/* RotarySwitch/IfBlock:then:behavior: */
typedef enum kcg_tag_SSM_ST_behavior_then_IfBlock {
  SSM_st_Change_behavior_then_IfBlock,
  x10_SSM_st_StBy_behavior_then_IfBlock,
  SSM_st_Magnet_behavior_then_IfBlock
} SSM_ST_behavior_then_IfBlock;
typedef kcg_char array_char_254[254];

typedef kcg_char array_char_1[1];

typedef array_char_1 array_char_1_6[6];

typedef kcg_char array_char_255[255];

typedef array_char_255 array_char_255_30[30];

typedef array_char_255 array_char_255_16[16];

typedef array_char_255 array_char_255_32[32];

typedef array_char_255 array_char_255_128[128];

typedef array_char_255 array_char_255_33[33];

typedef array_char_255 array_char_255_9[9];

typedef kcg_bool array_bool_16[16];

typedef kcg_bool array_bool_8[8];

typedef array_bool_8 array_bool_8_32[32];

typedef array_bool_8 array_bool_8_128[128];

typedef kcg_bool array_bool_60[60];

typedef kcg_bool array_bool_30[30];

typedef kcg_bool array_bool_13[13];

typedef kcg_bool array_bool_9[9];

typedef kcg_bool array_bool_14[14];

typedef kcg_bool array_bool_128[128];

typedef kcg_bool array_bool_32[32];

typedef kcg_bool array_bool_120[120];

typedef kcg_bool array_bool_15[15];

typedef kcg_float32 array_float32_60[60];

typedef kcg_float32 array_float32_8[8];

typedef kcg_float32 array_float32_120[120];

typedef kcg_float32 array_float32_999[999];

typedef kcg_float32 array_float32_1000[1000];

typedef kcg_float32 array_float32_6[6];

typedef kcg_float32 array_float32_100[100];

typedef kcg_float32 array_float32_16[16];

typedef kcg_int32 array_int32_2[2];

typedef kcg_int32 array_int32_128[128];

typedef kcg_int32 array_int32_5[5];

typedef kcg_int32 array_int32_32[32];

typedef kcg_int32 array_int32_6[6];

#ifndef kcg_copy_array_bool_15
#define kcg_copy_array_bool_15(kcg_C1, kcg_C2)                                \
  (kcg_assign_array((kcg_C1), (kcg_C2), sizeof (array_bool_15)))
#endif /* kcg_copy_array_bool_15 */

#ifndef kcg_copy_array_float32_16
#define kcg_copy_array_float32_16(kcg_C1, kcg_C2)                             \
  (kcg_assign_array((kcg_C1), (kcg_C2), sizeof (array_float32_16)))
#endif /* kcg_copy_array_float32_16 */

#ifndef kcg_copy_array_bool_120
#define kcg_copy_array_bool_120(kcg_C1, kcg_C2)                               \
  (kcg_assign_array((kcg_C1), (kcg_C2), sizeof (array_bool_120)))
#endif /* kcg_copy_array_bool_120 */

#ifndef kcg_copy_array_bool_32
#define kcg_copy_array_bool_32(kcg_C1, kcg_C2)                                \
  (kcg_assign_array((kcg_C1), (kcg_C2), sizeof (array_bool_32)))
#endif /* kcg_copy_array_bool_32 */

#ifndef kcg_copy_array_char_255
#define kcg_copy_array_char_255(kcg_C1, kcg_C2)                               \
  (kcg_assign_array((kcg_C1), (kcg_C2), sizeof (array_char_255)))
#endif /* kcg_copy_array_char_255 */

#ifndef kcg_copy_array_char_1
#define kcg_copy_array_char_1(kcg_C1, kcg_C2)                                 \
  (kcg_assign_array((kcg_C1), (kcg_C2), sizeof (array_char_1)))
#endif /* kcg_copy_array_char_1 */

#ifndef kcg_copy_array_bool_128
#define kcg_copy_array_bool_128(kcg_C1, kcg_C2)                               \
  (kcg_assign_array((kcg_C1), (kcg_C2), sizeof (array_bool_128)))
#endif /* kcg_copy_array_bool_128 */

#ifndef kcg_copy_array_bool_14
#define kcg_copy_array_bool_14(kcg_C1, kcg_C2)                                \
  (kcg_assign_array((kcg_C1), (kcg_C2), sizeof (array_bool_14)))
#endif /* kcg_copy_array_bool_14 */

#ifndef kcg_copy_array_char_1_6
#define kcg_copy_array_char_1_6(kcg_C1, kcg_C2)                               \
  (kcg_assign_array((kcg_C1), (kcg_C2), sizeof (array_char_1_6)))
#endif /* kcg_copy_array_char_1_6 */

#ifndef kcg_copy_array_int32_6
#define kcg_copy_array_int32_6(kcg_C1, kcg_C2)                                \
  (kcg_assign_array((kcg_C1), (kcg_C2), sizeof (array_int32_6)))
#endif /* kcg_copy_array_int32_6 */

#ifndef kcg_copy_array_char_254
#define kcg_copy_array_char_254(kcg_C1, kcg_C2)                               \
  (kcg_assign_array((kcg_C1), (kcg_C2), sizeof (array_char_254)))
#endif /* kcg_copy_array_char_254 */

#ifndef kcg_copy_array_float32_100
#define kcg_copy_array_float32_100(kcg_C1, kcg_C2)                            \
  (kcg_assign_array((kcg_C1), (kcg_C2), sizeof (array_float32_100)))
#endif /* kcg_copy_array_float32_100 */

#ifndef kcg_copy_array_float32_6
#define kcg_copy_array_float32_6(kcg_C1, kcg_C2)                              \
  (kcg_assign_array((kcg_C1), (kcg_C2), sizeof (array_float32_6)))
#endif /* kcg_copy_array_float32_6 */

#ifndef kcg_copy_array_float32_1000
#define kcg_copy_array_float32_1000(kcg_C1, kcg_C2)                           \
  (kcg_assign_array((kcg_C1), (kcg_C2), sizeof (array_float32_1000)))
#endif /* kcg_copy_array_float32_1000 */

#ifndef kcg_copy_array_bool_8_128
#define kcg_copy_array_bool_8_128(kcg_C1, kcg_C2)                             \
  (kcg_assign_array((kcg_C1), (kcg_C2), sizeof (array_bool_8_128)))
#endif /* kcg_copy_array_bool_8_128 */

#ifndef kcg_copy_array_bool_9
#define kcg_copy_array_bool_9(kcg_C1, kcg_C2)                                 \
  (kcg_assign_array((kcg_C1), (kcg_C2), sizeof (array_bool_9)))
#endif /* kcg_copy_array_bool_9 */

#ifndef kcg_copy_array_float32_999
#define kcg_copy_array_float32_999(kcg_C1, kcg_C2)                            \
  (kcg_assign_array((kcg_C1), (kcg_C2), sizeof (array_float32_999)))
#endif /* kcg_copy_array_float32_999 */

#ifndef kcg_copy_array_bool_8_32
#define kcg_copy_array_bool_8_32(kcg_C1, kcg_C2)                              \
  (kcg_assign_array((kcg_C1), (kcg_C2), sizeof (array_bool_8_32)))
#endif /* kcg_copy_array_bool_8_32 */

#ifndef kcg_copy_array_bool_13
#define kcg_copy_array_bool_13(kcg_C1, kcg_C2)                                \
  (kcg_assign_array((kcg_C1), (kcg_C2), sizeof (array_bool_13)))
#endif /* kcg_copy_array_bool_13 */

#ifndef kcg_copy_array_int32_32
#define kcg_copy_array_int32_32(kcg_C1, kcg_C2)                               \
  (kcg_assign_array((kcg_C1), (kcg_C2), sizeof (array_int32_32)))
#endif /* kcg_copy_array_int32_32 */

#ifndef kcg_copy_array_float32_120
#define kcg_copy_array_float32_120(kcg_C1, kcg_C2)                            \
  (kcg_assign_array((kcg_C1), (kcg_C2), sizeof (array_float32_120)))
#endif /* kcg_copy_array_float32_120 */

#ifndef kcg_copy_array_bool_30
#define kcg_copy_array_bool_30(kcg_C1, kcg_C2)                                \
  (kcg_assign_array((kcg_C1), (kcg_C2), sizeof (array_bool_30)))
#endif /* kcg_copy_array_bool_30 */

#ifndef kcg_copy_array_char_255_9
#define kcg_copy_array_char_255_9(kcg_C1, kcg_C2)                             \
  (kcg_assign_array((kcg_C1), (kcg_C2), sizeof (array_char_255_9)))
#endif /* kcg_copy_array_char_255_9 */

#ifndef kcg_copy_array_bool_60
#define kcg_copy_array_bool_60(kcg_C1, kcg_C2)                                \
  (kcg_assign_array((kcg_C1), (kcg_C2), sizeof (array_bool_60)))
#endif /* kcg_copy_array_bool_60 */

#ifndef kcg_copy_array_bool_8
#define kcg_copy_array_bool_8(kcg_C1, kcg_C2)                                 \
  (kcg_assign_array((kcg_C1), (kcg_C2), sizeof (array_bool_8)))
#endif /* kcg_copy_array_bool_8 */

#ifndef kcg_copy_array_int32_5
#define kcg_copy_array_int32_5(kcg_C1, kcg_C2)                                \
  (kcg_assign_array((kcg_C1), (kcg_C2), sizeof (array_int32_5)))
#endif /* kcg_copy_array_int32_5 */

#ifndef kcg_copy_array_int32_128
#define kcg_copy_array_int32_128(kcg_C1, kcg_C2)                              \
  (kcg_assign_array((kcg_C1), (kcg_C2), sizeof (array_int32_128)))
#endif /* kcg_copy_array_int32_128 */

#ifndef kcg_copy_array_char_255_33
#define kcg_copy_array_char_255_33(kcg_C1, kcg_C2)                            \
  (kcg_assign_array((kcg_C1), (kcg_C2), sizeof (array_char_255_33)))
#endif /* kcg_copy_array_char_255_33 */

#ifndef kcg_copy_array_bool_16
#define kcg_copy_array_bool_16(kcg_C1, kcg_C2)                                \
  (kcg_assign_array((kcg_C1), (kcg_C2), sizeof (array_bool_16)))
#endif /* kcg_copy_array_bool_16 */

#ifndef kcg_copy_array_char_255_128
#define kcg_copy_array_char_255_128(kcg_C1, kcg_C2)                           \
  (kcg_assign_array((kcg_C1), (kcg_C2), sizeof (array_char_255_128)))
#endif /* kcg_copy_array_char_255_128 */

#ifndef kcg_copy_array_int32_2
#define kcg_copy_array_int32_2(kcg_C1, kcg_C2)                                \
  (kcg_assign_array((kcg_C1), (kcg_C2), sizeof (array_int32_2)))
#endif /* kcg_copy_array_int32_2 */

#ifndef kcg_copy_array_float32_8
#define kcg_copy_array_float32_8(kcg_C1, kcg_C2)                              \
  (kcg_assign_array((kcg_C1), (kcg_C2), sizeof (array_float32_8)))
#endif /* kcg_copy_array_float32_8 */

#ifndef kcg_copy_array_char_255_32
#define kcg_copy_array_char_255_32(kcg_C1, kcg_C2)                            \
  (kcg_assign_array((kcg_C1), (kcg_C2), sizeof (array_char_255_32)))
#endif /* kcg_copy_array_char_255_32 */

#ifndef kcg_copy_array_float32_60
#define kcg_copy_array_float32_60(kcg_C1, kcg_C2)                             \
  (kcg_assign_array((kcg_C1), (kcg_C2), sizeof (array_float32_60)))
#endif /* kcg_copy_array_float32_60 */

#ifndef kcg_copy_array_char_255_16
#define kcg_copy_array_char_255_16(kcg_C1, kcg_C2)                            \
  (kcg_assign_array((kcg_C1), (kcg_C2), sizeof (array_char_255_16)))
#endif /* kcg_copy_array_char_255_16 */

#ifndef kcg_copy_array_char_255_30
#define kcg_copy_array_char_255_30(kcg_C1, kcg_C2)                            \
  (kcg_assign_array((kcg_C1), (kcg_C2), sizeof (array_char_255_30)))
#endif /* kcg_copy_array_char_255_30 */

#ifdef kcg_use_array_bool_15
#ifndef kcg_comp_array_bool_15
extern kcg_bool kcg_comp_array_bool_15(
  array_bool_15 *kcg_c1,
  array_bool_15 *kcg_c2);
#endif /* kcg_comp_array_bool_15 */
#endif /* kcg_use_array_bool_15 */

#ifdef kcg_use_array_float32_16
#ifndef kcg_comp_array_float32_16
extern kcg_bool kcg_comp_array_float32_16(
  array_float32_16 *kcg_c1,
  array_float32_16 *kcg_c2);
#endif /* kcg_comp_array_float32_16 */
#endif /* kcg_use_array_float32_16 */

#ifdef kcg_use_array_bool_120
#ifndef kcg_comp_array_bool_120
extern kcg_bool kcg_comp_array_bool_120(
  array_bool_120 *kcg_c1,
  array_bool_120 *kcg_c2);
#endif /* kcg_comp_array_bool_120 */
#endif /* kcg_use_array_bool_120 */

#ifdef kcg_use_array_bool_32
#ifndef kcg_comp_array_bool_32
extern kcg_bool kcg_comp_array_bool_32(
  array_bool_32 *kcg_c1,
  array_bool_32 *kcg_c2);
#endif /* kcg_comp_array_bool_32 */
#endif /* kcg_use_array_bool_32 */

#ifdef kcg_use_array_char_255
#ifndef kcg_comp_array_char_255
extern kcg_bool kcg_comp_array_char_255(
  array_char_255 *kcg_c1,
  array_char_255 *kcg_c2);
#endif /* kcg_comp_array_char_255 */
#endif /* kcg_use_array_char_255 */

#ifdef kcg_use_array_char_1
#ifndef kcg_comp_array_char_1
extern kcg_bool kcg_comp_array_char_1(
  array_char_1 *kcg_c1,
  array_char_1 *kcg_c2);
#endif /* kcg_comp_array_char_1 */
#endif /* kcg_use_array_char_1 */

#ifdef kcg_use_array_bool_128
#ifndef kcg_comp_array_bool_128
extern kcg_bool kcg_comp_array_bool_128(
  array_bool_128 *kcg_c1,
  array_bool_128 *kcg_c2);
#endif /* kcg_comp_array_bool_128 */
#endif /* kcg_use_array_bool_128 */

#ifdef kcg_use_array_bool_14
#ifndef kcg_comp_array_bool_14
extern kcg_bool kcg_comp_array_bool_14(
  array_bool_14 *kcg_c1,
  array_bool_14 *kcg_c2);
#endif /* kcg_comp_array_bool_14 */
#endif /* kcg_use_array_bool_14 */

#ifdef kcg_use_array_char_1_6
#ifndef kcg_comp_array_char_1_6
extern kcg_bool kcg_comp_array_char_1_6(
  array_char_1_6 *kcg_c1,
  array_char_1_6 *kcg_c2);
#endif /* kcg_comp_array_char_1_6 */
#endif /* kcg_use_array_char_1_6 */

#ifdef kcg_use_array_int32_6
#ifndef kcg_comp_array_int32_6
extern kcg_bool kcg_comp_array_int32_6(
  array_int32_6 *kcg_c1,
  array_int32_6 *kcg_c2);
#endif /* kcg_comp_array_int32_6 */
#endif /* kcg_use_array_int32_6 */

#ifdef kcg_use_array_char_254
#ifndef kcg_comp_array_char_254
extern kcg_bool kcg_comp_array_char_254(
  array_char_254 *kcg_c1,
  array_char_254 *kcg_c2);
#endif /* kcg_comp_array_char_254 */
#endif /* kcg_use_array_char_254 */

#ifdef kcg_use_array_float32_100
#ifndef kcg_comp_array_float32_100
extern kcg_bool kcg_comp_array_float32_100(
  array_float32_100 *kcg_c1,
  array_float32_100 *kcg_c2);
#endif /* kcg_comp_array_float32_100 */
#endif /* kcg_use_array_float32_100 */

#ifdef kcg_use_array_float32_6
#ifndef kcg_comp_array_float32_6
extern kcg_bool kcg_comp_array_float32_6(
  array_float32_6 *kcg_c1,
  array_float32_6 *kcg_c2);
#endif /* kcg_comp_array_float32_6 */
#endif /* kcg_use_array_float32_6 */

#ifdef kcg_use_array_float32_1000
#ifndef kcg_comp_array_float32_1000
extern kcg_bool kcg_comp_array_float32_1000(
  array_float32_1000 *kcg_c1,
  array_float32_1000 *kcg_c2);
#endif /* kcg_comp_array_float32_1000 */
#endif /* kcg_use_array_float32_1000 */

#ifdef kcg_use_array_bool_8_128
#ifndef kcg_comp_array_bool_8_128
extern kcg_bool kcg_comp_array_bool_8_128(
  array_bool_8_128 *kcg_c1,
  array_bool_8_128 *kcg_c2);
#endif /* kcg_comp_array_bool_8_128 */
#endif /* kcg_use_array_bool_8_128 */

#ifdef kcg_use_array_bool_9
#ifndef kcg_comp_array_bool_9
extern kcg_bool kcg_comp_array_bool_9(
  array_bool_9 *kcg_c1,
  array_bool_9 *kcg_c2);
#endif /* kcg_comp_array_bool_9 */
#endif /* kcg_use_array_bool_9 */

#ifdef kcg_use_array_float32_999
#ifndef kcg_comp_array_float32_999
extern kcg_bool kcg_comp_array_float32_999(
  array_float32_999 *kcg_c1,
  array_float32_999 *kcg_c2);
#endif /* kcg_comp_array_float32_999 */
#endif /* kcg_use_array_float32_999 */

#ifdef kcg_use_array_bool_8_32
#ifndef kcg_comp_array_bool_8_32
extern kcg_bool kcg_comp_array_bool_8_32(
  array_bool_8_32 *kcg_c1,
  array_bool_8_32 *kcg_c2);
#endif /* kcg_comp_array_bool_8_32 */
#endif /* kcg_use_array_bool_8_32 */

#ifdef kcg_use_array_bool_13
#ifndef kcg_comp_array_bool_13
extern kcg_bool kcg_comp_array_bool_13(
  array_bool_13 *kcg_c1,
  array_bool_13 *kcg_c2);
#endif /* kcg_comp_array_bool_13 */
#endif /* kcg_use_array_bool_13 */

#ifdef kcg_use_array_int32_32
#ifndef kcg_comp_array_int32_32
extern kcg_bool kcg_comp_array_int32_32(
  array_int32_32 *kcg_c1,
  array_int32_32 *kcg_c2);
#endif /* kcg_comp_array_int32_32 */
#endif /* kcg_use_array_int32_32 */

#ifdef kcg_use_array_float32_120
#ifndef kcg_comp_array_float32_120
extern kcg_bool kcg_comp_array_float32_120(
  array_float32_120 *kcg_c1,
  array_float32_120 *kcg_c2);
#endif /* kcg_comp_array_float32_120 */
#endif /* kcg_use_array_float32_120 */

#ifdef kcg_use_array_bool_30
#ifndef kcg_comp_array_bool_30
extern kcg_bool kcg_comp_array_bool_30(
  array_bool_30 *kcg_c1,
  array_bool_30 *kcg_c2);
#endif /* kcg_comp_array_bool_30 */
#endif /* kcg_use_array_bool_30 */

#ifdef kcg_use_array_char_255_9
#ifndef kcg_comp_array_char_255_9
extern kcg_bool kcg_comp_array_char_255_9(
  array_char_255_9 *kcg_c1,
  array_char_255_9 *kcg_c2);
#endif /* kcg_comp_array_char_255_9 */
#endif /* kcg_use_array_char_255_9 */

#ifdef kcg_use_array_bool_60
#ifndef kcg_comp_array_bool_60
extern kcg_bool kcg_comp_array_bool_60(
  array_bool_60 *kcg_c1,
  array_bool_60 *kcg_c2);
#endif /* kcg_comp_array_bool_60 */
#endif /* kcg_use_array_bool_60 */

#ifdef kcg_use_array_bool_8
#ifndef kcg_comp_array_bool_8
extern kcg_bool kcg_comp_array_bool_8(
  array_bool_8 *kcg_c1,
  array_bool_8 *kcg_c2);
#endif /* kcg_comp_array_bool_8 */
#endif /* kcg_use_array_bool_8 */

#ifdef kcg_use_array_int32_5
#ifndef kcg_comp_array_int32_5
extern kcg_bool kcg_comp_array_int32_5(
  array_int32_5 *kcg_c1,
  array_int32_5 *kcg_c2);
#endif /* kcg_comp_array_int32_5 */
#endif /* kcg_use_array_int32_5 */

#ifdef kcg_use_array_int32_128
#ifndef kcg_comp_array_int32_128
extern kcg_bool kcg_comp_array_int32_128(
  array_int32_128 *kcg_c1,
  array_int32_128 *kcg_c2);
#endif /* kcg_comp_array_int32_128 */
#endif /* kcg_use_array_int32_128 */

#ifdef kcg_use_array_char_255_33
#ifndef kcg_comp_array_char_255_33
extern kcg_bool kcg_comp_array_char_255_33(
  array_char_255_33 *kcg_c1,
  array_char_255_33 *kcg_c2);
#endif /* kcg_comp_array_char_255_33 */
#endif /* kcg_use_array_char_255_33 */

#ifdef kcg_use_array_bool_16
#ifndef kcg_comp_array_bool_16
extern kcg_bool kcg_comp_array_bool_16(
  array_bool_16 *kcg_c1,
  array_bool_16 *kcg_c2);
#endif /* kcg_comp_array_bool_16 */
#endif /* kcg_use_array_bool_16 */

#ifdef kcg_use_array_char_255_128
#ifndef kcg_comp_array_char_255_128
extern kcg_bool kcg_comp_array_char_255_128(
  array_char_255_128 *kcg_c1,
  array_char_255_128 *kcg_c2);
#endif /* kcg_comp_array_char_255_128 */
#endif /* kcg_use_array_char_255_128 */

#ifdef kcg_use_array_int32_2
#ifndef kcg_comp_array_int32_2
extern kcg_bool kcg_comp_array_int32_2(
  array_int32_2 *kcg_c1,
  array_int32_2 *kcg_c2);
#endif /* kcg_comp_array_int32_2 */
#endif /* kcg_use_array_int32_2 */

#ifdef kcg_use_array_float32_8
#ifndef kcg_comp_array_float32_8
extern kcg_bool kcg_comp_array_float32_8(
  array_float32_8 *kcg_c1,
  array_float32_8 *kcg_c2);
#endif /* kcg_comp_array_float32_8 */
#endif /* kcg_use_array_float32_8 */

#ifdef kcg_use_array_char_255_32
#ifndef kcg_comp_array_char_255_32
extern kcg_bool kcg_comp_array_char_255_32(
  array_char_255_32 *kcg_c1,
  array_char_255_32 *kcg_c2);
#endif /* kcg_comp_array_char_255_32 */
#endif /* kcg_use_array_char_255_32 */

#ifdef kcg_use_array_float32_60
#ifndef kcg_comp_array_float32_60
extern kcg_bool kcg_comp_array_float32_60(
  array_float32_60 *kcg_c1,
  array_float32_60 *kcg_c2);
#endif /* kcg_comp_array_float32_60 */
#endif /* kcg_use_array_float32_60 */

#ifdef kcg_use_array_char_255_16
#ifndef kcg_comp_array_char_255_16
extern kcg_bool kcg_comp_array_char_255_16(
  array_char_255_16 *kcg_c1,
  array_char_255_16 *kcg_c2);
#endif /* kcg_comp_array_char_255_16 */
#endif /* kcg_use_array_char_255_16 */

#ifdef kcg_use_array_char_255_30
#ifndef kcg_comp_array_char_255_30
extern kcg_bool kcg_comp_array_char_255_30(
  array_char_255_30 *kcg_c1,
  array_char_255_30 *kcg_c2);
#endif /* kcg_comp_array_char_255_30 */
#endif /* kcg_use_array_char_255_30 */

#endif /* KCG_TYPES_H_ */
/* $********** SCADE Suite KCG 32-bit 6.6.4 (build i3) **********
** kcg_types.h
** Generation date: 2025-09-23T22:03:49
*************************************************************$ */

