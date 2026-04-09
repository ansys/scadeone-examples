# Using Python wrapper with Jupyter for frequency analysis

This example is adapted from the [blog published on Ansys Innovation Space](https://innovationspace.ansys.com/knowledge/forums/topic/jupyter-notebook-programming-with-the-scade-python-wrapper/).
It demonstrates how to use Python libraries (NumPy, SciPy) with a Jupyter notebook to perform time and frequency analysis
on a low-pass controller implemented in Swan.

## Requirements

- Scade One 2026 R1
- Jupyter notebook
- See requirements.txt for required Python libraries

## How to run
- Run the `gen_python_wapper.bat` script to generate the Python wrapper for the LowPassRc model
- Run `test_wrapper.py`, which demonstrates how to call the generated wrapper in a simple script
- Create a Python virtual environment and install all the packages specified in `requirements.txt`
- Open the `Blog_Notebook.ipynb` file in Jupyter notebook and execute all cells
