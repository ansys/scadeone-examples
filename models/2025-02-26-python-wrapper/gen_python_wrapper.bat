set SCADE_ONE_PATH=C:\Program Files\ANSYS Inc\v261\Scade One

"%SCADE_ONE_PATH%\tools\job_launcher\scade_one_job_launcher.exe" -j CodeGen -p "LowPassRc/LowPassRc.sproj"
"%SCADE_ONE_PATH%\pytools\Scripts\pyscadeone.exe" pycodewrap "LowPassRc/LowPassRc.sproj" -j "CodeGen" -o "LowPassRC_Python" --install-dir "%SCADE_ONE_PATH%"
