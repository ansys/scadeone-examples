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
r"""

Tests for Controller::MainControl FMU (both Controller_MainControl.fmu and
ControllerWithSources.fmu).

Both FMUs are exercised identically via a parametrized fixture.  A test
failure in one but not the other pinpoints a build-time regression.

State machine under test (Controller.swan):
    Idle --btnStartStop--> Cooking/WaterAbsorption
         --btnDelay------> SetDelay
    SetDelay --btnStartStop--> DelayedCooking
             --btnDelay-------> Idle  (toggle back)
             --btnSetTime-----> advance preset index
    DelayedCooking --delay expires--> Cooking
    Cooking --btnStartStop--> Idle  (cancel)
            --isCooked & tempPot<=65--> KeepWarm
    KeepWarm --btnStartStop--> Idle

FMU timing:
    T_CYCLE = 200 ms, period = 0.2 s in tests => 200 ms simulated per doStep(0.2 s)
    SOAKING_TIME_S = 900 s
    Default delay preset 0 = 30*60 s
    DelayedCooking -> Cooking when: last'delay - timer <= SOAKING_TIME_S*1000

ColorLED enum (matches Swan type Controller::ColorLED):
    OFF=0, GREEN=1, RED=2, YELLOW=3

Display messages (Utils::Msg constants):
    IDLE_MSG = "IDLE\x00\x00"
    SOAK_MSG = "SOAK\x00\x00"
    COOK_MSG = "COOK\x00\x00"
"""  # noqa: D205

# ruff: noqa: D102 D103

from enum import IntEnum
from pathlib import Path
import shutil
import tempfile

from fmpy import extract, read_model_description
from fmpy.fmi2 import FMU2Slave
import pytest

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

FMU_DIR = Path(__file__).parent.parent

FMU_NAME = "Controller_MainControl.fmu"

# Each doStep in this test setup advances the controller clock by 200 ms.
STEP_SIZE_SEC = 0.2  # seconds
# Soaking phase: 15 min
SOAKING_STEPS = int(15 * 60 // STEP_SIZE_SEC)
# Default delay preset (30 min) transitions to Cooking after 15 min elapsed.
DELAY_TO_COOK_STEPS = int((30 * 60 - 15 * 60) // STEP_SIZE_SEC)


class ColorLED(IntEnum):
    """Matches Swan enum Controller::ColorLED."""

    OFF = 0
    GREEN = 1
    RED = 2
    YELLOW = 3


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


class _FMURunner:
    """Thin wrapper around FMU2Slave for step-by-step simulation."""

    def __init__(self, fmu_path: Path):
        self._md = read_model_description(str(fmu_path))
        self._vrs = {v.name: v.valueReference for v in self._md.modelVariables}
        self._tmpdir = tempfile.mkdtemp()
        extract(str(fmu_path), self._tmpdir)
        self._fmu = FMU2Slave(
            guid=self._md.guid,
            unzipDirectory=self._tmpdir,
            modelIdentifier=self._md.coSimulation.modelIdentifier,
            instanceName="test",
        )
        self._fmu.instantiate()
        self._fmu.setupExperiment(startTime=0.0)
        self._fmu.enterInitializationMode()
        self._fmu.exitInitializationMode()
        self._t = 0.0

    def step(
        self,
        *,
        btnStartStop: bool = False,
        btnDelay: bool = False,
        btnSetTime: bool = False,
        isLidOpen: bool = False,
        tempPot: float = 0.0,
    ) -> None:
        v = self._vrs
        self._fmu.setBoolean([v["btnStartStop"]], [btnStartStop])
        self._fmu.setBoolean([v["btnDelay"]], [btnDelay])
        self._fmu.setBoolean([v["btnSetTime"]], [btnSetTime])
        self._fmu.setBoolean([v["isLidOpen_Controller"]], [isLidOpen])
        self._fmu.setReal([v["tempPot_Controller"]], [tempPot])
        self._fmu.doStep(self._t, STEP_SIZE_SEC)
        self._t += STEP_SIZE_SEC

    @property
    def heater(self) -> float:
        return self._fmu.getReal([self._vrs["heaterPowerPct"]])[0]

    @property
    def color_led(self) -> int:
        return self._fmu.getInteger([self._vrs["colorLED"]])[0]

    @staticmethod
    def _decode_display(fmu: FMU2Slave, vrs: dict[str, int]) -> str:
        """Return display text as a decoded string (null bytes stripped)."""
        codes = [fmu.getInteger([vrs[f"displayText[{i}]"]])[0] for i in range(6)]
        return "".join(chr(c) for c in codes if c != 0)

    @property
    def display(self) -> str:
        return self._decode_display(self._fmu, self._vrs)

    def close(self) -> None:
        self._fmu.terminate()
        self._fmu.freeInstance()
        shutil.rmtree(self._tmpdir)


def _advance_until_cook(
    runner: _FMURunner, max_steps: int = SOAKING_STEPS + 10
) -> None:
    """Advance until the COOK phase becomes observable on outputs."""
    for _ in range(max_steps):
        runner.step(tempPot=0.0)
        if runner.display == "COOK":
            return


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestMainControlFMU:
    """Tests for Controller::MainControl FMU (both variants)."""

    @pytest.fixture
    def runner(self):
        """Parametrized fixture: runs test against FMU."""
        fmu_path = FMU_DIR / FMU_NAME
        r = _FMURunner(fmu_path)
        yield r
        r.close()

    def test_idle_state(self, runner: _FMURunner):
        """
        TC_RC_001 - Initial state is Idle.

        After one step with no inputs, the controller must report:
        * heaterPowerPct = 0
        * colorLED = OFF
        * displayText = "IDLE"
        """
        runner.step()

        assert runner.heater == pytest.approx(0.0)
        assert runner.color_led == ColorLED.OFF
        assert runner.display == "IDLE"

    def test_idle_to_cooking(self, runner: _FMURunner):
        """
        TC_RC_002 - btnStartStop transitions Idle -> Cooking (WaterAbsorption).

        Expected after pressing and releasing the button:
        * heaterPowerPct = 100  (full power during soaking)
        * colorLED = GREEN
        * displayText = "SOAK"
        """
        runner.step()  # settle in Idle
        runner.step(btnStartStop=True)  # press: transition latched
        runner.step()  # release: outputs updated

        assert runner.heater == pytest.approx(100.0)
        assert runner.color_led == ColorLED.GREEN
        assert runner.display == "SOAK"

    def test_cancel_cooking(self, runner: _FMURunner):
        """
        TC_RC_003 - btnStartStop during Cooking returns to Idle.

        Expected after pressing Start (enter Cooking) then pressing again:
        * heaterPowerPct = 0
        * colorLED = OFF
        * displayText = "IDLE"
        """
        runner.step()
        runner.step(btnStartStop=True)
        runner.step()  # now in Cooking

        assert runner.heater == pytest.approx(100.0)  # confirm we are in Cooking first

        runner.step(btnStartStop=True)  # cancel
        runner.step()  # outputs settle

        assert runner.heater == pytest.approx(0.0)
        assert runner.color_led == ColorLED.OFF
        assert runner.display == "IDLE"

    def test_set_delay_state(self, runner: _FMURunner):
        """
        TC_RC_004 - btnDelay from Idle enters SetDelay; btnDelay again returns to Idle.

        In SetDelay the display shows a HH:MM elapsed-time format.
        btnSetTime advances the internal preset index (not directly reflected in the
        display — the display tracks elapsed timer which starts at 0).
        A second btnDelay press toggles back to Idle.
        """
        runner.step()  # Idle
        runner.step(btnDelay=True)  # press Delay -> SetDelay
        runner.step()  # release

        msg = f"Expected HH:MM format in SetDelay, got {runner.display!r}"
        assert ":" in runner.display, msg
        assert runner.heater == pytest.approx(0.0), "Heater must be OFF in SetDelay"
        assert runner.color_led == ColorLED.OFF

        # btnSetTime advances internal preset; no direct display change (timer=0)
        runner.step(btnSetTime=True)
        runner.step()

        # Still in SetDelay — display still HH:MM format
        assert ":" in runner.display

        # btnDelay again returns to Idle
        runner.step(btnDelay=True)
        runner.step()

        assert runner.display == "IDLE"
        assert runner.color_led == ColorLED.OFF

    def test_delayed_cooking_to_cooking(self, runner: _FMURunner):
        """
        TC_RC_005 - SetDelay + btnStartStop eventually reaches Cooking.

        With 200 ms stepping, Start in SetDelay first enters DelayedCooking.
        After delay progression reaches the soaking threshold, outputs move to
        Cooking/WaterAbsorption. Validate resulting Cooking outputs.
        """
        runner.step()  # Idle
        runner.step(btnDelay=True)  # -> SetDelay
        runner.step()
        runner.step(btnStartStop=True)
        runner.step()  # enters DelayedCooking with 200 ms stepping

        for _ in range(DELAY_TO_COOK_STEPS + 10):
            runner.step(tempPot=0.0)
            if runner.heater == pytest.approx(100.0) and runner.display == "SOAK":
                break

        msg = "Heater must be ON in Cooking/WaterAbsorption"
        assert runner.heater == pytest.approx(100.0), msg
        assert runner.color_led == ColorLED.GREEN
        assert runner.display == "SOAK"

    def test_keepwarm_after_cooking(self, runner: _FMURunner):
        """
        TC_RC_006 - Full cooking cycle ends in KeepWarm state.

        Sequence:
        1. Start cooking (WaterAbsorption soaking phase, ~4 500 steps).
        2. Drive temperature through sub-states:
        tempPot >= 60  -> EnzymaticActivation (heater = 20)
        tempPot >= 80  -> ReachingBoiling     (heater = 100)
        tempPot >= 100 -> Simmering           (heater = 60)
        tempPot >= 105 (1 step TON) -> Resting (heater = 0, isCooked = true)
        3. Drop tempPot to 63 °C (<= 65 threshold) -> KeepWarm.

        Expected in KeepWarm:
        * colorLED = YELLOW
        * heaterPowerPct > 0  (PI controller actively keeping warm)
        * displayText shows HH:MM elapsed
        """
        runner.step()
        runner.step(btnStartStop=True)
        runner.step()
        runner.step()  # confirmed Cooking/WaterAbsorption

        # --- Soaking phase ---
        _advance_until_cook(runner)

        assert runner.display == "COOK", "Expected COOK after soaking phase"
        assert runner.color_led == ColorLED.RED

        # --- EnzymaticActivation ---
        runner.step(tempPot=62.0)
        runner.step(tempPot=62.0)
        assert runner.heater == pytest.approx(
            20.0
        ), "Expected heater=20 in EnzymaticActivation"

        # --- ReachingBoiling ---
        runner.step(tempPot=82.0)
        runner.step(tempPot=82.0)
        assert runner.heater == pytest.approx(
            100.0
        ), "Expected heater=100 in ReachingBoiling"

        # --- Simmering ---
        runner.step(tempPot=102.0)
        runner.step(tempPot=102.0)
        assert runner.heater == pytest.approx(60.0), "Expected heater=60 in Simmering"

        # --- Resting (isCooked=true) ---
        # Two settling steps are used to observe the Resting outputs.
        runner.step(tempPot=106.0)
        runner.step(tempPot=106.0)
        assert runner.heater == pytest.approx(0.0), "Expected heater=0 in Resting"
        assert runner.display == "COOK"

        # --- KeepWarm ---
        # Note: isCooked=true and tempPot <= 65
        runner.step(tempPot=63.0)
        runner.step(tempPot=63.0)

        assert runner.color_led == ColorLED.YELLOW, "Expected YELLOW LED in KeepWarm"
        assert runner.heater > 0.0, "PI controller must produce non-zero heater output"
        assert (
            ":" in runner.display
        ), f"Expected HH:MM display in KeepWarm, got {runner.display!r}"

    def test_keepwarm_to_idle(self, runner: _FMURunner):
        """
        TC_RC_007 - btnStartStop in KeepWarm returns to Idle.

        Expected after pressing Start in KeepWarm:
        * heaterPowerPct = 0
        * colorLED = OFF
        * displayText = "IDLE"
        """
        # Reach KeepWarm (abbreviated path using known step counts)
        runner.step()
        runner.step(btnStartStop=True)
        runner.step()
        runner.step()

        _advance_until_cook(runner)

        runner.step(tempPot=62.0)
        runner.step(tempPot=62.0)
        runner.step(tempPot=82.0)
        runner.step(tempPot=82.0)
        runner.step(tempPot=102.0)
        runner.step(tempPot=102.0)
        runner.step(tempPot=106.0)
        runner.step(tempPot=106.0)
        runner.step(tempPot=63.0)
        runner.step(tempPot=63.0)

        assert runner.color_led == ColorLED.YELLOW, "Must be in KeepWarm before cancel"

        runner.step(btnStartStop=True, tempPot=63.0)
        runner.step()

        assert runner.heater == pytest.approx(0.0)
        assert runner.color_led == ColorLED.OFF
        assert runner.display == "IDLE"
