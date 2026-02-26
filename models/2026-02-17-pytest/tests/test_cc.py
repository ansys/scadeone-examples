"""
Unit tests for Controller.

* Name: TC_CC_N_001
* Objective: Verify the behavior of the Cruise Control.
* Strategy: Set the buttons to different values to turn the CC on or off.
* Expected results: The output cruiseState conforms to the expectations.
* Pass criteria: The output result is identical to the expected value.

* Name: TC_CC_I_002
* Objective: Verify the integration of the Cruise Control.
* Strategy: Set the buttons and pedals to different values to exercise
  each state of the CC.
* Expected results: The output cruiseState conforms to the expectations
  and the value of the throttle is always equal to the accelerator when
  the CC is not regulating.
* Pass criteria: The output result is identical to the expected value.
"""

from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .proxy.cc.cc import Controller_CC


class CC_STATE(Enum):
    """Cruise Control states."""
    OFF, INT, STDBY, ON = range(4)

    def __eq__(self, other):
        """Equality operator overload to compare with integer/enum values."""
        if isinstance(other, int):
            return self.value == other
        if isinstance(other, Enum):
            return self.value == other.value
        return NotImplemented


def test_controller_nominal(controller: "Controller_CC"):
    """Test the nominal behavior of the Cruise Control."""
    # TC_CC_N_001
    controller.reset()
    # set the initial values for the commands
    controller.inputs.on = False
    controller.inputs.off = False
    controller.inputs.resume_ = False
    controller.inputs.set = False
    controller.inputs.speed = 0.0
    controller.inputs.accel = 0.0
    controller.inputs.brake = 0.0
    controller.inputs.quickAccel = False
    controller.inputs.quickDecel = False

    # Test Reference: CC_TEST_CCB_01
    #
    # Test Case Objectives:
    #    verify the CC is OFF when on button was never activated.
    #
    # Covered Requirements: CC_HLR_CCB_01 CC_HLR_CSM_01
    #
    # Test Case Acceptance Criteria:
    #    cruiseState is OFF and throttleCmd = accel
    controller.inputs.speed = 100.0
    for controller.inputs.accel in [0.0, 50.0, 0.0]:
        for i in range(20):
            controller.cycle()
            assert controller.outputs.cruiseState == CC_STATE.OFF
            assert abs(controller.outputs.throttleCmd - controller.inputs.accel) < 5.0e-6

    # Test Reference: CC_TEST_CCB_02
    #
    # Test Case Objectives:
    #    verify the CC is ON as soon as on button is activated,
    #    remains in the state, and the target speed is set.
    #
    # Covered Requirements: CC_HLR_CCB_02 CC_HLR_CCB_04 CC_HLR_CSM_01
    #
    # Test Case Acceptance Criteria:
    #    cruiseState is not OFF and targetSpeed = speed
    controller.inputs.on = True
    controller.cycle()
    assert abs(controller.outputs.cruiseSpeed - controller.inputs.speed) < 5.0e-6
    assert controller.outputs.cruiseState == CC_STATE.ON
    assert abs(controller.outputs.throttleCmd) < 5.0e-6
    controller.inputs.on = False
    controller.inputs.speed = 50.0
    for i in range(10):
        controller.cycle()
        assert abs(controller.outputs.throttleCmd) > 5.0e-6
        assert controller.outputs.cruiseState == CC_STATE.ON

    # Test Reference: CC_TEST_CCB_03
    #
    # Test Case Objectives:
    #    check that cruiseState come back to OFF as soon as off button is activated
    #
    # Covered Requirements: CC_HLR_CCB_03 CC_HLR_CSM_01
    #
    # Test Case Acceptance Criteria:
    #    cruiseState is OFF and throttleCmd = accel
    controller.inputs.off = True
    controller.cycle()
    assert controller.outputs.cruiseState == CC_STATE.OFF
    assert abs(controller.outputs.throttleCmd - controller.inputs.accel) < 5.0e-6


def test_controller_integration(controller: "Controller_CC"):
    # TC_CC_I_002
    controller.reset()
    # set the initial values for the commands
    controller.inputs.on = False
    controller.inputs.off = False
    controller.inputs.resume_ = False
    controller.inputs.set = False
    controller.inputs.speed = 0.0
    controller.inputs.accel = 0.0
    controller.inputs.brake = 0.0
    controller.inputs.quickAccel = False
    controller.inputs.quickDecel = False

    # Test Reference: CC_TEST_INT_01
    #
    # Test Case Objectives:
    #    verify the CC is started in STDBY mode when activated
    #    while the driver accelerates.
    #
    # Test Case Acceptance Criteria:
    #    cruiseState is STDBY, throttleCmd = accel,
    #    and cruiseSpeed = speed
    controller.inputs.speed = 100.0
    controller.inputs.accel = 25.0
    controller.inputs.on = True
    controller.cycle()
    assert controller.outputs.cruiseState == CC_STATE.STDBY
    assert abs(controller.outputs.throttleCmd - controller.inputs.accel) < 5.0e-6
    assert abs(controller.outputs.cruiseSpeed - controller.inputs.speed) < 5.0e-6

    # Test Reference: CC_TEST_INT_02
    #
    # Test Case Objectives:
    #    verify the CC switches to INT mode when the driver brakes.
    #
    # Test Case Acceptance Criteria:
    #    cruiseState is INT and throttleCmd = accel,
    controller.inputs.speed = 50.0
    controller.inputs.brake = 12.3456
    controller.inputs.on = False
    controller.cycle()
    assert controller.outputs.cruiseState == CC_STATE.INT
    assert abs(controller.outputs.throttleCmd - controller.inputs.accel) < 5.0e-6

    # Test Reference: CC_TEST_INT_03
    #
    # Test Case Objectives:
    #    verify the CC switches to STDBY mode when resume is activated.
    #
    # Test Case Acceptance Criteria:
    #    cruiseState is STDBY and throttleCmd = accel,
    controller.inputs.brake = 0.0
    controller.inputs.resume_ = True
    controller.cycle()
    assert controller.outputs.cruiseState == CC_STATE.STDBY
    assert abs(controller.outputs.throttleCmd - controller.inputs.accel) < 5.0e-6

    # Test Reference: CC_TEST_INT_04
    #
    # Test Case Objectives:
    #    verify the CC switches to ON mode when the driver stops accelerating.
    #
    # Test Case Acceptance Criteria:
    #    cruiseState is ON and throttleCmd > 0.
    controller.inputs.accel = 0.0
    controller.inputs.resume_ = False
    controller.cycle()
    assert controller.outputs.cruiseState == CC_STATE.ON
    assert controller.outputs.throttleCmd > 0.0

    # Test Reference: CC_TEST_INT_05
    #
    # Test Case Objectives:
    #    verify the throttle command is null while regulating
    #    and the cruise speed is above the speed.
    #
    # Test Case Acceptance Criteria:
    #    cruiseState is ON and throttleCmd = 0.
    controller.inputs.accel = 0.0
    controller.inputs.speed = 143.21
    for i in range(20):
        controller.cycle()
        assert controller.outputs.throttleCmd == 0.0
        assert controller.outputs.cruiseState == CC_STATE.ON
