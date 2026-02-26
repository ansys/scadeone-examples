# Copyright (C) 2025 - 2026 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# ruff: noqa: D101 D103

"""
Unit tests for RegulationMgt.

* Name: TC_RM_N_001
* Objective: Verify the nominal behavior of the regulation management function
  of the cruise control regarding the nominal conditions.
* Strategy: Set the target speed so that it is within the limit or not, together
  with different values of the accelerator.
* Expected results: The throttle is expected to be null when the accelerator
  is pressed and not null else.

  The state of the CC shall reflect that: either ON or STDBY.
* Pass criteria: The output result is identical to the expected value, with a precision of 5.10-6.

"""

from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .proxy.mgt.mgt import RegulationMgt_CC


class CC_STATE(Enum):  # noqa: N801
    """Possible states of the Cruise Control."""

    OFF, INT, STDBY, ON = range(4)

    def __eq__(self, other):
        """Equality operator overload to compare with integer/enum values."""
        if isinstance(other, int):
            return self.value == other
        if isinstance(other, Enum):
            return self.value == other.value
        return NotImplemented


def test_regulation_mgt_state(regulation_mgt: "RegulationMgt_CC"):
    """Test nominal behavior of the regulation management of the Cruise Control."""
    # TC_RM_N_001
    regulation_mgt.reset()
    inputs = regulation_mgt.inputs
    outputs = regulation_mgt.outputs
    # set the initial values for the commands
    inputs.speed = 0.0
    inputs.resume_ = False
    inputs.accel = 0.0
    inputs.brake = 0.0
    # set an arbitrary high target to ensure throttleCmd > 0 when the
    # regulation is active
    regulation_mgt.inputs.cruiseSpeed = 1000.0

    # Test Reference: RM_TEST_CCB_04
    #
    # Test Case Objectives:
    #    Verify the regulation is enabled when the nominal conditions are met.
    #
    # Covered Requirements: CC_HLR_CCB_01
    #
    # Test Case Acceptance Criteria:
    #    CruiseState is ON
    inputs.speed = 40.0
    regulation_mgt.cycle()
    assert outputs.cruiseState == CC_STATE.ON
    assert outputs.throttleCmd > 0.0

    # Test Reference: RM_TEST_CCB_051
    #
    # Test Case Objectives:
    #    Verify the regulation is disabled when the accelerator is pressed.
    #
    # Covered Requirements: CC_HLR_CCB_05 CC_HLR_PPD_02
    #
    # Test Case Acceptance Criteria:
    #    CruiseState is STDBY and throttleCmd = accel
    inputs.accel = 3.0
    regulation_mgt.cycle()
    assert outputs.cruiseState == CC_STATE.ON
    inputs.accel = 3.0001
    regulation_mgt.cycle()
    assert outputs.cruiseState == CC_STATE.STDBY
    assert abs(outputs.throttleCmd - inputs.accel) < 5.0e-6

    # Test Reference: RM_TEST_CCB_061
    #
    # Test Case Objectives:
    #    Verify the regulation is not reenabled while the
    #    accelerator is pressed.
    #
    # Covered Requirements: CC_HLR_CCB_06
    #
    # Test Case Acceptance Criteria
    #    CruiseState is STDBY and throttleCmd = accel
    for inputs.accel in [3.14159, 5.0, 15.0, 20.0]:
        regulation_mgt.cycle()
        assert outputs.cruiseState == CC_STATE.STDBY
        assert abs(outputs.throttleCmd - inputs.accel) < 5.0e-6

    # Test Reference: RM_TEST_CCB_062
    #
    # Test Case Objectives:
    #    Verify the regulation is reenabled when the accelerator is released.
    #
    # Covered Requirements: CC_HLR_CCB_06 CC_HLR_PPD_01
    #
    # Test Case Acceptance Criteria
    #    CruiseState is ON and throttleCmd > 0
    for inputs.accel in [3.0, 2.0, 0.0]:
        regulation_mgt.cycle()
        assert outputs.cruiseState == CC_STATE.ON
        assert outputs.throttleCmd > 0.0

    # Test Reference: RM_TEST_CCB_052
    #
    # Test Case Objectives:
    #    Verify the regulation is disabled when the speed is below the
    #    lower limit.
    #
    # Covered Requirements: CC_HLR_CCB_05
    #
    # Test Case Acceptance Criteria:
    #    CruiseState is STDBY and throttleCmd = accel
    inputs.speed = 29.999
    regulation_mgt.cycle()
    assert outputs.cruiseState == CC_STATE.STDBY
    assert abs(outputs.throttleCmd - inputs.accel) < 5.0e-6

    # Test Reference: RM_TEST_CCB_063
    #
    # Test Case Objectives:
    #    Verify the regulation is not reenabled while the
    #    speed is below the lower limit.
    #
    # Covered Requirements: CC_HLR_CCB_06
    #
    # Test Case Acceptance Criteria
    #    CruiseState is STDBY and throttleCmd = accel
    for inputs.speed in [15.0, 3.15159]:
        regulation_mgt.cycle()
        assert outputs.cruiseState == CC_STATE.STDBY
        assert abs(outputs.throttleCmd - inputs.accel) < 5.0e-6

    # Test Reference: RM_TEST_CCB_064
    #
    # Test Case Objectives:
    #    Verify the regulation is reenabled when the speed is in the limits.
    #
    # Covered Requirements: CC_HLR_CCB_06
    #
    # Test Case Acceptance Criteria
    #    CruiseState is ON and throttleCmd > 0
    for inputs.speed in [30.0, 120.0]:
        regulation_mgt.cycle()
        assert outputs.cruiseState == CC_STATE.ON
        assert outputs.throttleCmd > 0.0

    # Test Reference: RM_TEST_CCB_053
    #
    # Test Case Objectives:
    #    Verify the regulation is disabled when the speed is above the
    #    upper limit.
    #
    # Covered Requirements: CC_HLR_CCB_05
    #
    # Test Case Acceptance Criteria:
    #    CruiseState is STDBY and throttleCmd = accel
    inputs.speed = 160.00
    regulation_mgt.cycle()
    assert outputs.cruiseState == CC_STATE.STDBY
    assert abs(outputs.throttleCmd - inputs.accel) < 5.0e-6

    # Test Reference: RM_TEST_CCB_065
    #
    # Test Case Objectives:
    #    Verify the regulation is not reenabled while the
    #    speed is above the upper limit.
    #
    # Covered Requirements: CC_HLR_CCB_06
    #
    # Test Case Acceptance Criteria
    #    CruiseState is STDBY and throttleCmd = accel
    for inputs.speed in [150.0001, 999.0]:
        regulation_mgt.cycle()
        assert outputs.cruiseState == CC_STATE.STDBY
        assert abs(outputs.throttleCmd - inputs.accel) < 5.0e-6

    # Test Reference: RM_TEST_CCB_066
    #
    # Test Case Objectives:
    #    Verify the regulation is reenabled when the speed is in the limits.
    #
    # Covered Requirements: CC_HLR_CCB_06
    #
    # Test Case Acceptance Criteria
    #    CruiseState is ON and throttleCmd > 0
    for inputs.speed in [150.0, 75.0]:
        regulation_mgt.cycle()
        assert outputs.cruiseState == CC_STATE.ON
        assert outputs.throttleCmd > 0.0

    # Test Reference: RM_TEST_CCB_07
    #
    # Test Case Objectives:
    #    Verify the regulation is interrupted when the brake is pressed.
    #
    # Covered Requirements: CC_HLR_CCB_07 CC_HLR_PPD_02
    #
    # Test Case Acceptance Criteria:
    #    CruiseState is INT and throttleCmd = accel
    inputs.brake = 3.0
    regulation_mgt.cycle()
    assert outputs.cruiseState == CC_STATE.ON
    inputs.brake = 3.0001
    regulation_mgt.cycle()
    assert outputs.cruiseState == CC_STATE.INT
    assert abs(outputs.throttleCmd - inputs.accel) < 5.0e-6

    # Test Reference: RM_TEST_CCB_081
    #
    # Test Case Objectives:
    #    Verify the regulation is not resumed while the
    #    brake is pressed.
    #
    # Covered Requirements: CC_HLR_CCB_08 CC_HLR_PPD_02
    #
    # Test Case Acceptance Criteria
    #    CruiseState is INT and throttleCmd = accel
    inputs.resume_ = True
    for inputs.brake in [99.0, 3.0001]:
        regulation_mgt.cycle()
        assert outputs.cruiseState == CC_STATE.INT
        assert abs(outputs.throttleCmd - inputs.accel) < 5.0e-6

    # Test Reference: RM_TEST_CCB_082
    #
    # Test Case Objectives:
    #    Verify the regulation is resumed to ON while when
    #    resume is pressed.
    #
    # Covered Requirements: CC_HLR_CCB_08 CC_HLR_PPD_02
    #
    # Test Case Acceptance Criteria
    #    CruiseState is ON and throttleCmd > 0
    inputs.resume_ = False
    inputs.brake = 0.0
    regulation_mgt.cycle()
    assert outputs.cruiseState == CC_STATE.INT
    inputs.resume_ = True
    for inputs.brake in [3.0, 0.0]:
        regulation_mgt.cycle()
        assert outputs.cruiseState == CC_STATE.ON
        assert outputs.throttleCmd > 0.0

    # Test Reference: RM_TEST_CCB_083
    #
    # Test Case Objectives:
    #    Verify the regulation is resumed to STDBY while when
    #    resume is pressed.
    #
    # Covered Requirements: CC_HLR_CCB_08
    #
    # Test Case Acceptance Criteria
    #    CruiseState is ON and throttleCmd > 0
    inputs.resume_ = False
    inputs.brake = 50.0
    regulation_mgt.cycle()
    assert outputs.cruiseState == CC_STATE.INT
    inputs.speed = 20.0
    inputs.resume_ = True
    for inputs.brake in [3.0, 0.0]:
        regulation_mgt.cycle()
        assert outputs.cruiseState == CC_STATE.STDBY
        assert abs(outputs.throttleCmd - inputs.accel) < 5.0e-6
