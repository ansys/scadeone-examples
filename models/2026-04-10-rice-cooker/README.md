# Rice Cooker Model

## 1. Introduction

This project is a Scade One model of a rice cooker. It requires Scade One 2026 R1 or later.

The model combines:

- a controller that manages the cooking sequence,
- a physical plant model that approximates the bowl, water, rice, heating, evaporation, and swelling,
- utility modules for time handling, message formatting, and PI control,
- simulation harnesses to run the controller alone or coupled with the plant,
- graphical panels to interact with the system and visualize the plant state.

### Pre-requisites: generation of the graphical panels

Before opening the main project, you should:

- open the Rapid Prototyper graphical panels project at  [RiceCookerGraphicalPanels\RiceCookerGraphicalPanels.etp](RiceCookerGraphicalPanels\RiceCookerGraphicalPanels.etp),
- open each of the two graphical specifications inside: `RiceCookerPanel` and `VisualizationPanel`,
- for each specification, launch the `ScadeOneCoSimulation` job by clicking on the **Generate** button ![Button](generate_button.png).

This generates two Scade One wrapper projects that the main project depends on.

### High-level model structure

Once the graphical panels are generated, you may open the main Scade One project: [RiceCookerController/RiceCookerController.sproj](RiceCookerController/RiceCookerController.sproj).

At a high level, the model works as follows:

- the controller reads user inputs and plant feedback,
- it outputs a heater power command, a LED color, and a display message,
- the physical model converts heater power into temperature, water mass, and rice volume evolution,
- two graphical panels display the cooker state and provide interactive buttons,
- simulation harnesses connect both sides and the graphical panels together for batch simulation or interactive debug.

### Main modules and primary operators

| Module / file | Purpose | Main operator(s) |
| --- | --- | --- |
| `Controller.swan` | Rice cooker control logic | `MainControl` |
| `Clock-Ticks.swan` | Base simulation time source | `millis` |
| `Clock-Utils.swan` | Timing utilities | `TON`, `MsElapsed`, `DeltaSeconds` |
| `Utils-Msg.swan` | Display text formatting | `MillisecToHHMM` |
| `Utils-Msg.swani` | Message interface and constants | `MillisecToHHMM`, `SIZE_MSG`, `IDLE_MSG`, `SOAK_MSG`, `COOK_MSG` |
| `Utils-PIController.swan` | PI and saturation helpers | `PIAntiWindUp` |
| `PlantModel.swan` | Physical plant model | `PhysicalModel` |
| `Simulation.swant` | Simulation harnesses | `TestControllerWithPhysics` |
| `SimulationWithPanel.swant` | Interactive harnesses and debug integration | `harness_ControlPhysicsPanel` |
| `RiceCookerPanel/assets/RiceCookerPanel.swan` | Rice cooker control panel binding | `RiceCookerPanel` |
| `VisualizationPanel/assets/VisualizationPanel.swan` | Plant visualization panel binding | `VisualizationPanel` |

## 2. The Rice Cooker Controller

File: [RiceCookerController/assets/Controller.swan](RiceCookerController/assets/Controller.swan)

`MainControl` is the main controller model. It takes three button inputs:

- `btnStartStop`
- `btnDelay`
- `btnSetTime`

and produces:

- `heaterPowerPct`: heater command in percent,
- `colorLED`: panel LED state,
- `displayText`: message shown on the cooker display.

The controller also reads two sensors provided by the surrounding system:

- `tempPot`: pot temperature,
- `isLidOpen`: lid state.

### Main states

The top-level automaton in `MainControl` contains five user-visible phases:

| State | Role |
| --- | --- |
| `Idle` | Cooker is stopped. Heater is off and the display shows `IDLE`. |
| `SetDelay` | User cycles through preset delayed-start durations. The selected delay is displayed as `HH:MM`. |
| `DelayedCooking` | Countdown before cooking starts. LED is green and the remaining delay is displayed. |
| `Cooking` | Main cooking sequence. This is the core cooking automaton. |
| `KeepWarm` | After cooking completes and temperature falls to the keep-warm threshold, a PI controller maintains temperature around the keep-warm setpoint. |

### Cooking sub-phases

Inside `Cooking`, the controller uses a dedicated automaton with two layers.

First layer:

- `WaterAbsorption`: soaking phase regulated with a PI controller around `TEMP_SOAKING_C`. The controller waits until the soaking timer expires and the lid is closed.
- `CookingPhases`: thermal cooking sequence once soaking is finished.

Second layer inside `CookingPhases`:

| Sub-phase | Role |
| --- | --- |
| `PreCooking` | Full power heating at the beginning. |
| `EnzymaticActivation` | Reduced power plateau around the starch activation range. |
| `ReachingBoiling` | Full power ramp to boiling. |
| `Simmering` | Fixed reduced power while boiling continues. |
| `Resting` | Heater off, cooking marked complete. |

The transitions are temperature-driven:

- `PreCooking` -> `EnzymaticActivation` when `tempPot >= 60`
- `EnzymaticActivation` -> `ReachingBoiling` when `tempPot >= 80`
- `ReachingBoiling` -> `Simmering` when `tempPot >= 100`
- `Simmering` -> `Resting` when `tempPot >= TEMP_BOILING_THRESHOLD_C` continuously for 5 seconds

Then the top-level controller transitions from `Cooking` to `KeepWarm` when cooking is marked done and the pot temperature has cooled down to `TEMP_KEEP_WARM_C`.

### Controller constants

| Constant | Value | Meaning |
| --- | ---: | --- |
| `NB_PRESET_DELAYS` | 8 | Number of preset delayed-start durations |
| `PRESET_DELAYS_SEC` | `[1800, 2700, 3600, 7200, 10800, 18000, 25200, 32400]` | Delayed-start presets (in seconds) |
| `SOAKING_TIME_S` | 900 | Soaking duration (in seconds) |
| `TEMP_SOAKING_C` | 45 | Soaking temperature target (in Celsius) |
| `TEMP_BOILING_THRESHOLD_C` | 105 | Threshold used to validate sustained boiling (in Celsius) |
| `TEMP_KEEP_WARM_C` | 65 | Keep-warm temperature target (in Celsius) |
| `KP_SOAKING` | 0.038 | Proportional gain for soaking PI control |
| `KI_SOAKING` | 0.00002 | Integral gain for soaking PI control. |
| `KP_WARM` | 0.03 | Proportional gain for keep-warm PI control |
| `KI_WARM` | 0.00012 | Integral gain for keep-warm PI control |
| `MAX_POWER_WARMUP_PCT` | 50 | Warm-up power cap constant available in the controller model. |

## 3. The Utilities for the Rice Cooker

Files:

- [RiceCookerController/assets/Clock-Ticks.swan](RiceCookerController/assets/Clock-Ticks.swan)
- [RiceCookerController/assets/Clock-Utils.swan](RiceCookerController/assets/Clock-Utils.swan)
- [RiceCookerController/assets/Utils-Msg.swan](RiceCookerController/assets/Utils-Msg.swan)
- [RiceCookerController/assets/Utils-Msg.swani](RiceCookerController/assets/Utils-Msg.swani)
- [RiceCookerController/assets/Utils-PIController.swan](RiceCookerController/assets/Utils-PIController.swan)

### `Clock-Ticks.swan`

This module defines the base time source for the model.

- `millis()`: returns the number of milliseconds since start.
- `T_CYCLE`: base cycle duration in milliseconds.
- `ACCELERATION`: simulation acceleration factor.

The effective simulated time increment per cycle is:

$$
\Delta t_{cycle} = ACCELERATION \times T\_CYCLE
$$

This module can be replaced by a real-time clock source when deploying on hardware,
or by a different time source for faster or slower simulations.

### `Clock-Utils.swan`

This module provides reusable timing utilities.

- `TON(IN, PT, millis)`: standard on-delay timer. It becomes true when `IN` remains true for at least `PT` milliseconds.
- `MsElapsed(millis)`: elapsed milliseconds since a local reference point (when the scope of the operator instance is active).
- `DeltaSeconds(millis)`: elapsed time since previous cycle, converted to seconds.

### `Utils-Msg.swan` and `Utils-Msg.swani`

These files define the display formatting helpers and display messages.

- `MillisecToHHMM(ms)`: formats a duration in milliseconds as a `HH:MM` character array.
- `SIZE_MSG`: display message size.
- `IDLE_MSG`, `SOAK_MSG`, `COOK_MSG`: fixed display texts.

`MillisecToHHMM` uses `Int2Char` to convert a digit into an ASCII character.

`Int2Char` is intentionally not implemented directly in Swan. It relies on imported C code from `RiceCookerController/resources/int2char.h`, where the macro is:

```c
#define Int2Char_Utils_Msg(i) (char)(i + '0')
```

This is simply an ASCII conversion from a digit value to its character representation. The same behavior could be written in Scade One, but it would require an unnecessary switch/case structure for a very small operation.

### `Utils-PIController.swan`

This module contains the PI control building blocks used by the controller.

| Operator | Role |
| --- | --- |
| `PI` | Basic proportional-integral controller. |
| `PIAntiWindUp` | PI controller with output limiting and anti-windup behavior. This is the utility used in the main controller. |
| `Integral` | Plain numerical integrator based on elapsed time. |
| `SaturatedIntegral` | Integrator variant aware of saturation state. |
| `Limiter` | Clamps a value between lower and upper bounds and reports whether saturation occurred. |

## 4. The Plant Model

File: [RiceCookerController/assets/PlantModel.swan](RiceCookerController/assets/PlantModel.swan)

`PhysicalModel` is the plant model coupled to the controller during system simulation. It approximates the thermal behavior of the cooker and the progressive swelling of the rice.

Inputs:

- `tempExt`: ambient temperature,
- `powerPct`: heater command in percent,
- `volWaterInit`: initial water volume,
- `volRiceInit`: initial rice volume.

Outputs:

- `tempC`: pot temperature,
- `massWaterKg`: remaining free water mass,
- `massWaterPct`: remaining water percentage relative to initial water mass,
- `volRiceM3`: rice volume in cubic meters,
- `volRicePct`: rice volume relative to initial rice volume.

### Physical behavior modeled

The model distinguishes three main regimes:

- before boiling: temperature rises while rice absorbs water,
- during boiling: temperature is clamped to the boiling point while water evaporates and is still absorbed,
- after the free water is gone: only temperature evolves,
- throughout all phases: heat loss to the environment is applied.

### Power and heat-loss equations

The model first computes input power and thermal loss:

$$
P_{in} = \frac{powerPct}{100} \cdot FULL\_POWER\_COOKER\_W
$$

$$
P_{loss} = HEAT\_LOSS\_W\_PER\_K \cdot (T - T_{ext})
$$

### Temperature evolution outside boiling

When the cooker is not in the boiling regime, temperature evolves according to:

$$
\Delta T = \frac{(P_{in} - P_{loss}) \cdot \Delta t}{MASS\_BOWL\_KG \cdot C_{P,alu} + m_{rice} \cdot C_{P,dry\_rice} + m_{water,total} \cdot C_{P,water}}
$$

with:

$$
m_{water,total} = m_{water,free} + m_{water,absorbed}
$$

and the updated temperature:

$$
T_{next} = T + \Delta T
$$

### Boiling regime

When the previous temperature is at or above the boiling point and free water is still present, the model keeps temperature fixed at:

$$
T = T_{boiling} = 100^\circ C
$$

### Water absorption by the rice

The absorbed water mass increases with temperature and elapsed time:

$$
\Delta m_{w,absorbed} = 0.0001 \cdot \frac{T}{T_{boiling}} \cdot \Delta t
$$

The implemented model accumulates this absorbed mass and limits it to the configured maximum ratio relative to the dry rice mass:

$$
m_{w,absorbed} = \min \left(m_{w,absorbed}^{prev} + \Delta m_{w,absorbed},\; m_{rice} \cdot (MAX\_RATIO\_WATER\_ABSORB\_BY\_MASS - 1) \right)
$$

With the current constant value `MAX_RATIO_WATER_ABSORB_BY_MASS = 2`, this means the absorbed water mass can grow up to the dry rice mass.

### Water evaporation during boiling

During boiling, evaporated water is accumulated as:

$$
\Delta m_{w,evap} = \frac{(P_{in} - P_{loss}) \cdot \Delta t}{L}
$$

with:

- $L$ the latent heat of vaporization of water.
- $P_{in}$ and $P_{loss}$ computed as above, but with $T$ fixed to the boiling point.

and the updated total evaporated mass:

$$
m_{w,evap} = m_{w,evap}^{prev} + \Delta m_{w,evap}
$$

### Remaining free water

The remaining free water mass is then computed as:

$$
m_{water,free} = \max(0, m_{water,init} - m_{w,absorbed} - m_{w,evap})
$$

In the current model, the initial water input is provided through `volWaterInit` and used directly as the initial water mass scale.

### Rice volume evolution

The project also models rice swelling. This is handled by `VolumeRice`, which combines absorbed water and a temperature-dependent gelatinization phase factor.

This computation is only for visualization purposes (to see the rice volume evolution in a graphical panel) and is not fed back into the controller, which only sees the temperature and remaining free water mass.

The phase factor is:

| Temperature range | Equation |
| --- | --- |
| $T < TEMP\_GEL\_LOW\_C$ | $f_{phase} = S0\_BASELINE\_SWELLING$ |
| $TEMP\_GEL\_LOW\_C \le T < TEMP\_GEL\_HIGH\_C$ | $f_{phase} = S0\_BASELINE\_SWELLING + (1 - S0\_BASELINE\_SWELLING) \cdot clamp\left(\frac{T - TEMP\_GEL\_LOW\_C}{TEMP\_GEL\_HIGH\_C - TEMP\_GEL\_LOW\_C}, 0, 1\right)$ |
| $T \ge TEMP\_GEL\_HIGH\_C$ | $f_{phase} = 1$ |

The swelling ratio is driven by absorbed water and limited to the configured volumetric expansion:

$$
r_{abs} = clamp\left(\frac{m_{w,absorbed}}{m_{w,absorbed} + 0.5 \cdot \rho_{rice} \cdot V_{rice,init}}, 0, 1\right)
$$

$$
V_{rice} = V_{rice,init} \cdot \left(1 + (MAX\_RATIO\_WATER\_ABSORB\_BY\_VOL - 1) \cdot r_{abs} \cdot f_{phase}\right)
$$

This gives a progressive increase in rice volume, with a baseline swelling below gelatinization and full swelling once gelatinization is complete.

### Plant model operators

| Operator | Role |
| --- | --- |
| `PhysicalModel` | Main plant model coupling thermal and mass evolution. |
| `MassWaterAbsorbed` | Computes cumulative absorbed water mass. |
| `MassWaterEvap` | Computes cumulative evaporated water mass during boiling. |
| `ChangeTemp` | Computes temperature change outside the boiling plateau. |
| `VolumeRice` | Computes rice swelling volume from absorbed water and temperature phase. |
| `ComputeHeight` | Converts a volume into an approximate bowl height, used by the visualization panel. |

### Physical and rice characteristics constants

| Constant | Value | Meaning |
| --- | ---: | --- |
| `BOILING_POINT_C` | 100 | Boiling point used by the model. |
| `TEMP_GEL_LOW_C` | 60 | Lower bound of the gelatinization range. |
| `TEMP_GEL_HIGH_C` | 80 | Upper bound of the gelatinization range. |
| `HEAT_LOSS_W_PER_K` | 0.5 | Lumped thermal loss coefficient. |
| `LATENT_HEAT_VAPOR_J_PER_KG` | 2257000 | Latent heat of vaporization of water. |
| `C_P_ALU` | 900 | Specific heat capacity of aluminum. |
| `C_P_WATER` | 4184 | Specific heat capacity of water. |
| `C_P_DRY_RICE` | 1200 | Specific heat capacity of dry rice. |
| `DENSITY_RICE_KG_PER_M3` | 900 | Dry rice density. |
| `MAX_RATIO_WATER_ABSORB_BY_MASS` | 2 | Maximum final total mass ratio for hydrated rice relative to dry rice. |
| `MAX_RATIO_WATER_ABSORB_BY_VOL` | 3 | Maximum final volume ratio for swollen rice relative to initial volume. |
| `S0_BASELINE_SWELLING` | 0.35 | Baseline swelling factor before gelatinization. |

### Rice cooker constants

| Constant | Value | Meaning |
| --- | ---: | --- |
| `MASS_BOWL_KG` | 0.160 | Aluminum bowl mass. |
| `DIAMETER_BOWL_CM` | 12.5 | Bowl diameter used to derive displayed liquid/rice heights. |
| `FULL_POWER_COOKER_W` | 300 | Heater full power. |

## 5. How to Run Simulation

1. Change `ACCELERATION` in module `Clock::Ticks` to `5` so that 1 execution cycle corresponds to 1 simulated second.
2. Go to the Job Explorer.
3. Find `SimulationJobSystem` and click **Start**.
4. Once completed, click **Open Results**.
5. Drag and drop the flows you want to observe from the left sidebar into the main results view.

`SimulationJobSystem` is configured on harness `Simulation::TestControllerWithPhysics`, which couples the controller and the plant model.

## 6. The Graphical Panel

Rapid Prototyper Project: [RiceCookerGraphicalPanels\RiceCookerGraphicalPanels.etp](RiceCookerGraphicalPanels\RiceCookerGraphicalPanels.etp)

This project contains two graphical panels (rgfx files).

| Panel | Purpose |
| --- | --- |
| `RiceCookerPanel` | Interactive front panel of the rice cooker. It shows the text display, LED color, and provides the three user buttons. |
| `VisualizationPanel` | Plant visualization panel showing water percentage, water mass, water height, rice volume, rice height, temperature, and power. |

The corresponding built panels are accessible through wrapper operators in the projects generated by SCADE Rapid Prototyper:

- [RiceCookerPanel/assets/RiceCookerPanel.swan](RiceCookerPanel/assets/RiceCookerPanel.swan)
- [VisualizationPanel/assets/VisualizationPanel.swan](VisualizationPanel/assets/VisualizationPanel.swan)

## 7. How to Run Debug with Graphical Panel

1. Change `ACCELERATION` in module `Clock::Ticks` to a faster value, for example `50` (in which case, 1 cycle corresponds to 10 simulated seconds).
2. Go to `harness_ControlPhysicsPanel` in module `SimulationWithPanel`.
3. Start the debug session with **F5** or the debug button at the bottom right.
4. Click **Play** for live execution or **Step** with **F9** for step-by-step execution.
5. Use the buttons on the rice cooker panel to interact with the controller.

Note that the Test harness `harness_ControlPhysicsPanel` connects:

- the cooker panel `RiceCookerPanel` with interactive inputs,
- the main controller `Controller::MainControl`,
- the plant model `PlantModel::PhysicalModel`,
- the engineering panel `VisualizationPanel`,
- and the controller sensors `tempPot` and `isLidOpen`.

This harness is the most useful entry point for interactive end-to-end debugging of the controller together with the plant.

## 8. Any question?

Please reach out to the [SCADE support team](https://www.ansys.com/support) or your local Application Engineers
if you have any question about the model, or if you want to share feedback or suggestions for improvement.
