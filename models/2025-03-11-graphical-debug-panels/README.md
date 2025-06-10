Requirements:
* Ansys Scade One 2025 R1 or later
* Ansys SCADE Rapid Prototyper 2025 R1 or later

Instructions:
1. Open project `ThermometerPanel/ThermometerPanel.etp` in SCADE Rapid Prototyper.
2. Launch generation configuration `ScadeOneCosimulationThermometerPanel`. This will generate a Scade One Co-Simulation project under `ThermometerPanel/ThermometerPanel_ScadeOneCosimulation/`.
3. Open project `Thermometer/Thermometer.sproj` in Scade One.
4. Launch a debug session from operator `TestModule::TH_ThermPanelToFahrenheit`.
