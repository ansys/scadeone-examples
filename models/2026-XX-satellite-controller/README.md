# Satellite Control Simulation with Scade One Python Wrapper

This example is adapted from the [blog published on Ansys Innovation Space](https://innovationspace.ansys.com/knowledge/forums/forum/digital-engineering/embedded-software/).
It demonstrates how to use a Python Proxy generated from a Scade One model to perform discrete-time simulations of a satellite control system.

## Overview

The example covers the following steps:

1. Computation of the LQ controller in Python
2. Continuous-time simulation of the satellite system (plant + controller)
3. Generation of the Python Proxy from a Scade One project
4. Discretization of the satellite plant model
5. Discrete-time simulation of the satellite system (plant + imported Scade One controller)
6. Comparison between continuous-time and discrete-time results
7. Analysis of tracking errors

All steps are consolidated in the notebook: SatelliteExample.ipynb.

## Requirements

- Scade One 2026 R1
- Python 3.13 or later
- Jupyter notebook for simulation and visualization
- See requirements.txt for required Python libraries

## How to run
- Create a Python virtual environment and install all the packages specified in `requirements.txt`
- Open the `SatelliteExample.ipynb` file in Jupyter notebook and execute all cells
