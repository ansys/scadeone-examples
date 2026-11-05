## Scade One and SCADE Display integration
This model is a companion to our [Technical Blog article](https://innovation.ansys.com/public/articles/topic/scade-one-and-scade-display-integration-on-a-hardware-target-expu/).

## Requirements
- Ansys Scade One 2026 R1
- Ansys SCADE Display 2026 R1
- Ansys SCADE Rapid Prototyper 2026 R1
- The sources for the OGLX middleware library

## Instructions - Co-simulation on Windows host
1. In **SCADE Display**, open project `.\scade-display\DemoPFD.etp`
    - Run job `ScadeOneCoSimulation`

2. In **SCADE Rapid Prototyper**, open project `.\scade-rapid-prototyper\ControlPanel.etp`
    - Run job `ScadeOneCoSimulation`

3. In **Scade One**, open project `.\scade-one\FlightControl\FlightControl.sproj`
    - Check that the "Workspace" diagram shows no error. If projects appear to be missing, steps #1 or #2 above may not have been completed.
    - Open operator `FlightControlSimulation::World`
    - Launch a debug session (via the button at the bottom-right of the diagram)
    - Adjust cycle time to 20ms with the clock icon in the top bar
    - Start running cycles by using the "Play" icon at the bottom right of the diagram
    - Play with the buttons in the "ControlPanel" graphical window, observe results on both graphical windows and on the Scade One diagram. A good start is to enable autopilot and set target speeds / altitude.

## Instructions - Itegration on Windows host
1. In **SCADE Display**, open project `.\scade-display\DemoPFD.etp`
    - Run job `Code Generation`

2. In **Scade One**, open project `.\scade-one\FlightControl\FlightControl.sproj`
    - *Note:* the "Workspace" diagram may show an error if you have never generated the Rapid Protoyper co-simulation project before. You can ignore this, as it is not needed for the standalone executable.
    - Run job `CodeGenerationJob0`
    - Copy all generated `.c`/`.h` files from `.\scade-one\FlightControl\jobs\codegen_6294cfd\out` to `.\integration\swan_cg\`. You will need to create the `swan_cg` beforehand.
    - If you have a copy of Microsoft Visual Studio 2022 installed:
        - Run script `.\integration\integration_host\cmake_msvc2022.bat`
        - Once build completes, run `.\integration\integration_host\msvc2022\Release\flightControlSystem.exe`
    - If you don't have Visual Studio installed:
        - Run script `.\integration\integration_host\cmake_ninja_gcc.bat`
        - Once build completes, run `.\integration\integration_host\ninja_gcc\flightControlSystem.exe`

## Instructions - Integration on i.MX8 target
1. In **SCADE Display**, open project `.\scade-display\DemoPFD.etp`
    - Run job `Code Generation`

2. In **Scade One**, open project `.\scade-one\FlightControl\FlightControl.sproj`
    - *Note:* the "Workspace" diagram may show an error if you have never generated the Rapid Protoyper co-simulation project before. You can ignore this, as it is not needed for the standalone executable.
    - Run job `CodeGenerationJob0`

3. Prepare the MicroSD card for your i.MX8 board
    - Download the official Debian image for the i.MX8MP: [`imx8mp-sdhc-debian-e4824cb.img.xz`](https://solid-run-images.sos-de-fra-1.exo.io/IMX8/imx8mp_build/lf-5.15.y/2025-09-30_e4824cb/imx8mp-sdhc-debian-e4824cb.img.xz)
    - Flash it to your SD card using Rufus or BalenaEtcher on Windows:
        - Select your SD card as the target device.
        - Select the downloaded .img.xz file.
        - Click Start and wait for the write to complete.
    - Insert the card into the CuBox-M and apply power. The default credentials are:
        - User: `root`
        - Password: `root`

4. Expand the filesystem
     - The flashed image only occupies approximately 1 GB of the card. Expand the partition and filesystem before installing any packages.

    ```bash
    # Free space for the package manager
    sudo apt clean

    # Install the partitioning tool
    sudo apt update
    sudo apt install parted -y

    # Resize partition 2 to fill the card
    sudo parted /dev/mmcblk1 resizepart 2 100%

    # Reboot so the kernel sees the updated partition table
    sudo reboot
    After the reboot, expand the filesystem to fill the enlarged partition:
    sudo resize2fs /dev/mmcblk1p2

    # Verify: the / mount point should reflect the full card size
    df -h
    Installing the XFCE Desktop Environment
    SCADE Display requires a graphical environment. We install XFCE with the LightDM login manager:
    sudo apt update
    sudo apt install apt-utils -y
    sudo apt install xfce4 xfce4-goodies lightdm firefox-esr -y

    # Set graphical login as the default boot target
    sudo systemctl set-default graphical.target
    ```

5. Configure the X11 Display Server
    - On the i.MX8MP, the default X11 auto-configuration often fails to initialize the framebuffer, producing a black screen or blinking cursor at boot. We fix this by forcing the fbdev driver. Install the required packages and fix directory permissions:

    ```bash
    sudo apt install xserver-xorg-video-fbdev -y
    sudo chown -R lightdm:lightdm /var/lib/lightdm
    sudo chmod 1777 /tmp
    ```

    - Create the X11 configuration file:

    ```bash
    sudo mkdir -p /etc/X11/xorg.conf.d/
    sudo nano /etc/X11/xorg.conf.d/99-fbdev.conf
    ```

    - Paste the following content and save (Ctrl+O, Enter, Ctrl+X):

    ```txt
    Section "Device"
        Identifier "i.MX Speedo"
        Driver "fbdev"
        Option "fbdev" "/dev/fb0"
    EndSection
    ```

    - Restart the display manager to apply the change:

    ```bash
    sudo systemctl restart lightdm
    ```

    - The CuBox-M now boots into the XFCE desktop.

6. Set up your development environment
    - Install the required OpenGL ES and EGL development headers:

    ```bash
    sudo apt install libegl1-mesa-dev libgles2-mesa-dev build-essential -y
    ```

    > Note on GPU drivers: The i.MX8MP Vivante GPU can operate either with the open-source Mesa software renderer (what `libegl1-mesa-dev` provides) or with NXP's proprietary Vivante driver stack available in NXP or SolidRun BSPs. The example project targets the Mesa stack, which is sufficient for development and demonstration.

  - There are two approaches for building the project.

**Option A (Recommended)** - Compile Natively on the CuBox-M

The CuBox-M's Cortex-A53 cores handle the small C project natively. The simplest workflow is to connect with VS Code Remote SSH:
- Install VS Code on Windows
- Install the Remote - SSH extension
- Connect to the CuBox-M using its IP address
- Open the project folder and compile directly on the board.

**Option B** - Cross-Compile from Windows

- For larger projects or CI integration, cross-compilation from Windows via WSL2 is more efficient.
- Install the ARM64 cross-compiler in your WSL terminal:

```bash
sudo apt update
sudo apt install build-essential gcc-aarch64-linux-gnu g++-aarch64-linux-gnu pkg-config
```

- Copy the board's headers and libraries to a local sysroot:

```bash
mkdir ~/cubox-sysroot
rsync -avz debian@IP_CUBOX:/usr/include ~/cubox-sysroot/
rsync -avz debian@IP_CUBOX:/usr/lib/aarch64-linux-gnu ~/cubox-sysroot/lib/
```

7. Build and run
    - Folder `integration_imx8/make/` contains a [ready-to-use Makefile](.\integration\integration_imx8\make\Makefile). It compiles every source tree in a single pass and links the result against the OGLX ES2 runtime library.
    - The OGLX ES2 library (`libOGLXES2`) is not part of the SCADE Display installation. Refer to the OGLX documentation for build instructions - CodeIntegration_SDY-OGLX-EPG-67.pdf - (or add its host path to LIBPATH) before building.
    - From a terminal on the CuBox-M (or from your WSL cross-compilation environment), run:

    ```bash
    cd integration_imx8/make
    make
    ```

    - On success, the `flightControlSystem` executable is produced in the `make/` directory.

    - Start the application from a terminal on the CuBox-M. If you are connecting over SSH, make sure to set the display variable so the application renders on the XFCE desktop:

    ```bash
    export DISPLAY=:0
    ./flightControlSystem
    ```

    - The DemoPFD window opens on the XFCE desktop. The flight-control Scade One model drives the display every cycle, and the SCADE Display OGLX backend renders the Primary Flight Display in real time on the Vivante GPU.
