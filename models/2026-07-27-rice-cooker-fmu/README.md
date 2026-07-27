# RiceCookerPlantModel

This repository is organized into three components:

- `fmu-plant`: Modelica plant source, FMU build scripts, and Python FMU tests
- `fmu-controller`: Controller and panel FMU binaries used by Simulink models
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

## fmu-plant

### Open in OpenModelica

1. Open OMEdit.
2. Open `fmu-plant/src/package.mo`.
3. Simulate `PlantModel.TestPhysicalModel` if needed.

### Build the plant FMU

Windows:

```bat
cd fmu-plant
build_fmu.bat
```

Linux or macOS:

```bash
cd fmu-plant
bash build_fmu.sh
```

Expected outputs:

- `fmu-plant/build/windows/PlantModel.PhysicalModel.fmu`
- `fmu-plant/build/linux/PlantModel.PhysicalModel.fmu`

### Run plant FMU tests

```bash
cd fmu-plant
pip install -r tests/requirements.txt
pytest tests/
```

## simulink

### Build Simulink models

```bat
cd simulink
build_simulink.bat
```

Expected outputs:

- `simulink/model/RiceCookerPlant.slx`
- `simulink/model/RiceCookerWithPanel.slx`

### Run co-simulation demo

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

## Notes

- Simulink FMU blocks use FMU file names only (for example `Controller_MainControl.fmu`).
- `addpath` is used to expose `fmu-controller` before FMU blocks are instantiated.
- Generated Simulink build folders (`slprj`) and archive artifacts are ignored in `.gitignore`.
