## Requirements
* Ansys Scade One 2026 R1 or later
* Ansys SCADE Rapid Prototyper 2026 R1 or later

## Instructions
1. Open project `RapidPrototyperPanel/RapidPrototyperPanel.etp` in SCADE Rapid Prototyper.
2. Run build configuration `ScadeOneCosimulation` to (re)build `RapidPrototyperPanel/specification_ScadeOneCosimulation/*`.
4. Open project `ImageProcessingLogic/ImageProcessingLogic.sproj` in Scade One.
5. Run a debug session on test harness `TestConv2dRP::harness_Conv2D`.
6. Press the "Play" button in Scade One and interact with the graphical panel.
