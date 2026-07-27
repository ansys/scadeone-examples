# RiceCookerPlantModel

This repository is organized into three components:

- `fmu-controller`: Controller FMU binary used by Simulink models
- `fmu-panel`: Graphical panel FMU binary used by a Simulink model
- `simulink`: Simulink model builders, co-simulation script, and MATLAB integration tests

## Repository layout

```text
fmu-controller/
  Controller_MainControl.fmu
  RiceCookerController/
    ... (Scade One controller model)

fmu-panel/
  RiceCookerPanel.fmu
  RiceCookerGraphicalPanels/
    ... (SCADE Rapid Prototyper panel models)
  tests/
    requirements.txt
    test_main_control.py
  build_fmu.bat

simulink/
  model/
    build_model.m
    build_model_with_panel.m
    build_plant_core.m
    rice_cooker_physics.m
    (RiceCookerPlant.slx)
    (RiceCookerWithPanel.slx)
  scripts/
    demo_cosim.m
  tests/
    test_cosim.m
  build_simulink.bat
  run_simulink_cosim.bat
  run_simulink_tests.bat
```

## Export Scade One controller model to FMU

### Generate code from Scade One controller model

First, generate the code from the Scade One controller model:

1. Open "RiceCookerController/RiceCookerController.sproj" in Scade One
2. Open the **Job Explorer** (Alt + Shift + J)
3. Select the code generation job **CodeGenerationController** from "RiceCookerController"
4. Click on **Start**

### Install Dependencies

Install dependencies (pyscadeone):

```bat
pip install ansys-scadeone-core
```

... or in a virtual environment:

```bat
cd fmu-controller
pip install uv
uv venv
uv pip install ansys-scadeone-core
```

### Export FMU from generated code

You can then export the FMU from the generated code using the following batch command:

```bat
cd fmu-controller
build_fmu.bat
```

... or if you are using `uv` for a virtual environment:

```bat  
cd fmu-controller
uv run cmd /c build_fmu.bat
```

## Export Graphical Panel to FMU

1. Open the panel "fmu-panel\RiceCookerGraphicalPanels\RiceCookerGraphicalPanels.etp"
2. Launch the code generation with **FMU** configuration

## Simulink import of FMU blocks

### Build Simulink models

```bat
cd simulink
build_simulink.bat
```

Expected outputs:

- `simulink/model/RiceCookerPlant.slx`
- `simulink/model/RiceCookerWithPanel.slx`

You can then run the Simulink models in MATLAB / Simulink.

### Run Simulink co-simulation demo

```bat
cd simulink
run_simulink_cosim.bat
```

This runs `scripts/demo_cosim.m` and writes:

- `simulink/cosim_result.png`

### Run MATLAB integration tests

```bat
cd simulink
run_simulink_tests.bat
```

### Notes

- Simulink FMU blocks use FMU file names only (for example `Controller_MainControl.fmu`).
- `addpath` is used to expose `fmu-controller` before FMU blocks are instantiated.
- Generated Simulink build folders (`slprj`) and archive artifacts are ignored in `.gitignore`.
