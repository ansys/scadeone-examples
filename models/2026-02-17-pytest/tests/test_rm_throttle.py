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
# ruff: noqa: D101 D102 D103

"""
Unit tests for RegulationMgt.

* Name: TC_RM_N_02
* Objective: Verify the behavior of the throttle management,
  e.g. the behavior of the regulation using a PI integrator.
* Strategy: Set the target speed to values equal/above/below to the current
  speed, for different speed values.
* Expected results: The value of the output shall be null or regulated
  depending on the speed differences and the state of the regulation.

  The expected results are computed from the requirements in the test case itself.
* Pass criteria: The output result is identical to the expected value.
"""

from math import exp
from typing import TYPE_CHECKING, Optional

import matplotlib.pyplot as plt

if TYPE_CHECKING:
    from .proxy.mgt.mgt import RegulationMgt_CC

T_CYCLE = 0.1

# PID parameters value
KP = 8.113
KI = 0.5
THROTTLE_MIN = 0
THROTTLE_MAX = 100
SPEED_MIN = 30
SPEED_MAX = 50


class Car:
    def __init__(self, initial_vehicle_speed=0):
        self.last_vehicle_speed = initial_vehicle_speed

    def power_train(self, throttle: float):
        # car parameters
        iengine = 0.025
        tengine = -0.04
        torq_max = 400

        throttle_sat = min(max(throttle, 0.0), 100.0)
        engine_power = tengine * throttle_sat
        engine_torq = 1.0 - exp(engine_power)
        torq = (torq_max / iengine) * (engine_torq**2)
        return torq

    def vehicle_dynamic(self, torq, brake):
        # car parameters
        kbrake = 200
        mass = 1450
        vehicle_dynamic = 2.5

        if torq < 1:
            stop_brake = 150
        else:
            stop_brake = 0

        brake_torq = (
            stop_brake
            + kbrake * brake
            + +0.3 * (self.last_vehicle_speed**2)
            + 2.5 * self.last_vehicle_speed
        )
        if self.last_vehicle_speed < -0.1:
            brake_torq = -brake_torq
        elif self.last_vehicle_speed < 0.1:
            brake_torq = 0

        vehicle_speed = (
            self.last_vehicle_speed
            + ((torq - brake_torq) * vehicle_dynamic * T_CYCLE) / mass
        )
        return vehicle_speed

    def step(self, throttle, brake):
        self._torq = self.power_train(throttle)
        self.last_vehicle_speed = self.vehicle_dynamic(self._torq, brake)
        return self.last_vehicle_speed


class PI:
    """A simple PI regulator."""

    def __init__(self, kp=0.2, ki=0.0, output_min=None, output_max=None):
        self.Kp = kp
        self.Ki = ki
        self._integral = 0.0
        self.saturated = False
        self.min = output_min
        self.max = output_max

    def saturate(
        self, value: Optional[float], min_: Optional[float], max_: Optional[float]
    ):
        """Saturate value between min_ (if specified) or max_ (if specified).

        Returns a tuple of (saturated_value, is_saturated).
        """
        if value is None:
            return None, False
        elif min_ is not None and value < min_:
            return min_, True
        elif max_ is not None and value > max_:
            return max_, True
        return value, False

    def __call__(self, measure: float, setpoint: float):
        error = setpoint - measure
        self._proportional = self.Kp * error
        if not self.saturated:
            self._integral += self.Ki * error
        output = self._proportional + self._integral
        output, self.saturated = self.saturate(output, self.min, self.max)
        return output


def test_regulation_mgt_throttle(regulation_mgt: "RegulationMgt_CC"):
    """Test nominal behavior of the throttle management of the Cruise Control."""
    # TC_RM_N_02
    regulation_mgt.reset()

    # set the initial values for the commands to be in ON for regulation
    regulation_mgt.inputs.resume_ = False
    regulation_mgt.inputs.accel = 0
    regulation_mgt.inputs.brake = 0
    regulation_mgt.inputs.cruiseSpeed = 95

    # set initial car speed between SPEED_MIN and SPEED_MAX
    car_ref_speed = 71
    car_ref_throttle = 0
    car_test_speed = car_ref_speed

    # instantiate a PI regulator
    regulator_ref = PI(KP, KI, output_min=THROTTLE_MIN, output_max=THROTTLE_MAX)

    # instantiate 2 cars
    car_ref = Car(initial_vehicle_speed=car_ref_speed)
    car_test = Car(initial_vehicle_speed=car_ref_speed)

    # points lists for plotting
    t_data = [0.0]
    cruise_speed = [0.0]
    car_speed = [0.0]
    car_ref_throttle: float

    for cycle in range(200):
        if car_test_speed <= 95:
            print(f"Cycle #{cycle}: {car_test_speed=}")
        # reference system
        car_ref_throttle = regulator_ref(
            car_ref_speed, regulation_mgt.inputs.cruiseSpeed
        )
        car_ref_speed = car_ref.step(car_ref_throttle, regulation_mgt.inputs.brake)

        # system under test
        regulation_mgt.inputs.speed = car_test_speed
        regulation_mgt.cycle()
        car_test_speed = car_test.step(
            regulation_mgt.outputs.throttleCmd, regulation_mgt.inputs.brake
        )

        t_data.append(t_data[-1] + T_CYCLE)
        cruise_speed.append(regulation_mgt.inputs.cruiseSpeed)
        car_speed.append(car_test_speed)

        # check results
        assert abs(regulation_mgt.outputs.throttleCmd - car_ref_throttle) < 5.0e-3

    regulation_mgt.inputs.cruiseSpeed = 125
    for _ in range(100):
        # reference system
        car_ref_throttle = regulator_ref(
            car_ref_speed, regulation_mgt.inputs.cruiseSpeed
        )  # type: ignore
        car_ref_speed = car_ref.step(car_ref_throttle, regulation_mgt.inputs.brake)

        # system under test
        regulation_mgt.inputs.speed = car_test_speed
        regulation_mgt.cycle()
        car_test_speed = car_test.step(
            regulation_mgt.outputs.throttleCmd, regulation_mgt.inputs.brake
        )

        t_data.append(t_data[-1] + T_CYCLE)
        cruise_speed.append(regulation_mgt.inputs.cruiseSpeed)
        car_speed.append(car_test_speed)

        # check results
        assert abs(regulation_mgt.outputs.throttleCmd - car_ref_throttle) < 5.0e-3

    plt.plot(t_data, cruise_speed, t_data, car_speed)
    plt.legend(["cruise speed", "car speed"])
    plt.show()
