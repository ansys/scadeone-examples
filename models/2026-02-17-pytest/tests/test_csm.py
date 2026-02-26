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
# ruff: noqa: D103

"""
Unit tests for CruiseSpeedMgt.

* Procedure: TC_CSM_N_001
* Objective: Verify the nominal behavior of the cruise speed management
  function of the cruise control
* Strategy: Use different values for quickAccel, quickDecel and set and check
  the target speed.
* Expected results: The current speed is considered when set is true,
  else the target speed is updated accordingly to the commands quickAccel
  and quickDecel.
* Pass criteria: The output result is identical to the expected value,
  with a precision of 5.10-6.

* Procedure: TC_CSM_R_002
* Objective: Verify the robustness behavior of the cruise speed management
  function of the cruise control
* Strategy: Set the speed near to the lower and upper boundaries of the
  CC system and activate the buttons I/R/Set.
* Expected results: The target speed shall never get outside the specified
  boundaries.
* Pass criteria: The output result is identical to the expected value.
"""

from enum import Enum
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from .proxy.mgt.mgt import CruiseSpeedMgt_CC


class CC_BTN(Enum):  # noqa: N801
    """Cruise Control Actions."""

    NONE, SET, ACCELERATE, DECELERATE = range(4)

    def __eq__(self, other):
        """Equality operator overload to compare with integer/enum values."""
        if isinstance(other, int):
            return self.value == other
        if isinstance(other, Enum):
            return self.value == other.value
        return NotImplemented


def _set_action(cruise_speed_mgt: "CruiseSpeedMgt_CC", action: CC_BTN):
    """Set the action on the controller inputs."""
    # default
    cruise_speed_mgt.inputs.set = False
    cruise_speed_mgt.inputs.quickAccel = False
    cruise_speed_mgt.inputs.quickDecel = False
    if action == CC_BTN.SET:
        cruise_speed_mgt.inputs.set = True
    elif action == CC_BTN.ACCELERATE:
        cruise_speed_mgt.inputs.quickAccel = True
    elif action == CC_BTN.DECELERATE:
        cruise_speed_mgt.inputs.quickDecel = True


@pytest.mark.parametrize(
    "init, cycles, expected",
    [
        # TC_CSM_N_001
        # Test Reference: CSM_TEST_CSM_00
        #
        # Test Case Objectives:
        #    Verify the initial value of the cruise speed.
        #
        # Covered Requirements: CC_HLR_CSM_00 (derived requirement)
        #
        # Test Case Acceptance Criteria:
        #    cruiseSpeed = initial speed
        (34.12, [], 34.12),
        # Test Reference: CSM_TEST_CSM_06
        #
        # Test Case Objectives:
        #    Verify cruise speed is maintained when no button is pressed.
        #
        # Covered Requirements: CC_HLR_CSM_06
        #
        # Test Case Acceptance Criteria:
        #    cruiseSpeed = initial speed
        (34.12, [(56.78, CC_BTN.NONE)], 34.12),
        # Test Reference: CSM_TEST_CSM_02
        #
        # Test Case Objectives:
        #    Verify cruise speed is changed when the set button is activated.
        #
        # Covered Requirements: CC_HLR_CSM_02
        #
        # Test Case Acceptance Criteria:
        #    cruiseSpeed = new speed
        (34.12, [(56.78, CC_BTN.SET)], 56.78),
        # Test Reference: CSM_TEST_CSM_03
        #
        # Test Case Objectives:
        #    Verify cruise speed is incremented when the quick accel button
        #    is activated.
        #
        # Covered Requirements: CC_HLR_CSM_03
        #
        # Test Case Acceptance Criteria:
        #    cruiseSpeed = initial speed + SPEED_INC
        (75.31, [(0.0, CC_BTN.ACCELERATE)], 77.81),
        # Test Reference: CSM_TEST_CSM_04
        #
        # Test Case Objectives:
        #    Verify cruise speed is incremented when the quick decel button
        #    is activated.
        #
        # Covered Requirements: CC_HLR_CSM_04
        #
        # Test Case Acceptance Criteria:
        #    cruiseSpeed = initial speed - SPEED_INC
        (77.81, [(0.0, CC_BTN.DECELERATE)], 75.31),
        # TC_CSM_R_002
        # Test Reference: CSM_TEST_CSM_051
        #
        # Test Case Objectives:
        #    Verify cruise speed is in [30.0, 150.0] when the set button
        #    is activated.
        #
        # Covered Requirements: CC_HLR_CSM_02 CC_HLR_CSM_05
        #
        # Test Case Acceptance Criteria:
        #    cruiseSpeed = SPEED_MIN
        (12.34, [], 30.0),
        # Test Reference: CSM_TEST_CSM_052
        #
        # Test Case Objectives:
        #    Verify cruise speed is in [30.0, 150.0] when the set button
        #    is activated.
        #
        # Covered Requirements: CC_HLR_CSM_02 CC_HLR_CSM_05
        #
        # Test Case Acceptance Criteria:
        #    cruiseSpeed = SPEED_MAX
        (160, [], 150.0),
        # Test Reference: CSM_TEST_CSM_053
        #
        # Test Case Objectives:
        #    Verify cruise speed is in [30.0, 150.0] after the quick accel
        #    button has been activated too many times.
        #
        # Covered Requirements: CC_HLR_CSM_02 CC_HLR_CSM_05
        #
        # Test Case Acceptance Criteria:
        #    cruiseSpeed = SPEED_MAX
        (123.45, [(0.0, CC_BTN.ACCELERATE)] * 20, 150.0),
        # Test Reference: CSM_TEST_CSM_054
        #
        # Test Case Objectives:
        #    Verify cruise speed is in [30.0, 150.0] after the quick decel
        #    button has been activated too many times.
        #
        # Covered Requirements: CC_HLR_CSM_02 CC_HLR_CSM_05
        #
        # Test Case Acceptance Criteria:
        #    cruiseSpeed = SPEED_MIN
        (123.45, [(0.0, CC_BTN.DECELERATE)] * 50, 30.0),
    ],
)
def test_cruise_speed_mgt(
    cruise_speed_mgt: "CruiseSpeedMgt_CC",
    init: float,
    cycles: list[tuple[float, CC_BTN]],
    expected: float,
):
    cruise_speed_mgt.reset()
    # set the initial speed
    cruise_speed_mgt.inputs.speed = init
    _set_action(cruise_speed_mgt, CC_BTN.SET)
    cruise_speed_mgt.cycle()
    # perform the actions
    for speed, action in cycles:
        cruise_speed_mgt.inputs.speed = speed
        _set_action(cruise_speed_mgt, action)
        cruise_speed_mgt.cycle()
    assert abs(cruise_speed_mgt.outputs.cruiseSpeed - expected) < 5.0e-6
