from pathlib import Path

scade_one_install = r"C:\Program Files\ANSYS Inc\v252\Scade One"

S_ONE_INSTALL_DIR = Path(scade_one_install)
if not S_ONE_INSTALL_DIR.exists():
    raise FileNotFoundError(f"Scade One installation not found at {S_ONE_INSTALL_DIR}")
