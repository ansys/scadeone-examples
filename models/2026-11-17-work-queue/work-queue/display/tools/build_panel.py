# Copyright (C) 2025 - 2026 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Build the work-queue panel for Scade One co-simulation.

    python display/tools/build_panel.py [--mode synchronous|asynchronous] [--snapshot]

Steps (all command line, SCADE Display 2027 R1):
  1. run make_panel.py with SCADE Display's bundled Python (writes display/panel/);
  2. create display/panel/WorkQueuePanel.etp with `batch createProject` (default
     tables, bitmap fonts and fonts DLL), register the panel files, and point its
     "Scade One Co-simulation" configuration at the panel;
  3. `batch migrate` every graphics file (normalises the API output);
  4. `batch generate` the co-simulation project into display/WorkQueuePanel/
     (WorkQueuePanel.sproj, assets/WorkQueuePanel.swan, resources/*.spanel);
  5. optionally export a PNG snapshot of the panel (design-time values).

The generated .spanel is not committed; run this script to recreate it.
"""

import argparse
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

HOME = Path(
    os.environ.get(
        "SCADE_DISPLAY_HOME", r"C:\Program Files\ANSYS Inc\v271\SCADE Display"
    )
)
CONSOLE = str(HOME / "SCADE Display" / "bin" / "ScadeDisplayConsole.exe")
PYTHON = str(HOME / "contrib" / "Python312" / "python.exe")

DISPLAY = Path(__file__).resolve().parent.parent
PANEL_DIR = DISPLAY / "panel"
OUT_DIR = DISPLAY / "WorkQueuePanel"
NAME = "WorkQueuePanel"
CONF = "Scade One Co-simulation"
GRAPHICS = ["card.ogfx", "button.ogfx", "cell.ogfx", NAME + ".sgfx"]

MODEL_FOLDER = """		<Folder id="9010" extensions="asfx;pgfx;sgfx;ogfx" name="Model Files">
			<elements>
				<FileRef id="9011" persistAs="{name}.sgfx"/>
				<FileRef id="9012" persistAs="card.ogfx"/>
				<FileRef id="9013" persistAs="cell.ogfx"/>
				<FileRef id="9014" persistAs="button.ogfx"/>
			</elements>
		</Folder>
"""


def run(cmd, check=True):
    """Run `cmd`; exit with its output when it fails and `check` is set."""
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if check and proc.returncode != 0:
        sys.stdout.write(proc.stdout + proc.stderr)
        sys.exit("failed: %s" % " ".join(cmd[:3]))
    return proc


def set_conf_prop(project, name, value):
    """Set property `name` of the Scade One co-simulation configuration."""
    conf = re.search(
        r'<Configuration id="(\d+)" name="%s"/>' % re.escape(CONF), project
    ).group(1)
    pattern = re.compile(
        r'(<Prop id="\d+" name="%s">)\s*(?:<value>[^<]*</value>)?'
        r"(\s*<configuration>%s</configuration>)" % (re.escape(name), conf)
    )
    project, count = pattern.subn(
        lambda m: "%s\n\t\t\t<value>%s</value>%s" % (m.group(1), value, m.group(2)),
        project,
    )
    assert count == 1, (name, count)
    return project


def errors_of(proc):
    """Return the error and warning lines of a SCADE Display console run."""
    lines = (proc.stdout + proc.stderr).splitlines()
    return [
        line
        for line in lines
        if (line[:1] in "EW" and line[1:5].isdigit()) or line.startswith("ERROR")
    ]


def main():
    """Build the panel."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode", default="synchronous", choices=["synchronous", "asynchronous"]
    )
    parser.add_argument("--snapshot", action="store_true")
    args = parser.parse_args()

    run([PYTHON, str(DISPLAY / "tools" / "make_panel.py")])
    etp_path = PANEL_DIR / (NAME + ".etp")
    etp = str(etp_path)
    etp_path.unlink(missing_ok=True)
    run([CONSOLE, "batch", "createProject", etp, "-nature", "DISPLAY"])
    for g in GRAPHICS:
        run([CONSOLE, "batch", "migrate", str(PANEL_DIR / g), "-project", etp])
        for leftover in (g + ".bak", g + ".log"):
            (PANEL_DIR / leftover).unlink(missing_ok=True)
    # `migrate` rewrites the project file, so configure it afterwards.
    project = etp_path.read_text(encoding="utf-8")
    project = set_conf_prop(project, "@SDY:CONFSOURCE", NAME + ".sgfx")
    project = set_conf_prop(project, "@SDY:CONFPANELNAME", NAME)
    project = set_conf_prop(project, "@SDY:INTEGRATIONMODE", args.mode)
    if 'persistAs="%s.sgfx"' % NAME not in project:
        project = project.replace(
            "\t<roots>\n", "\t<roots>\n" + MODEL_FOLDER.format(name=NAME), 1
        )
    with etp_path.open("w", encoding="utf-8") as f:
        f.write(project)

    shutil.rmtree(OUT_DIR, ignore_errors=True)
    proc = run(
        [CONSOLE, "batch", "generate", etp, "-conf", CONF, "-outdir", str(OUT_DIR)],
        check=False,
    )
    for line in errors_of(proc):
        print(line)
    if proc.returncode != 0:
        sys.exit("panel generation failed")
    print("generated", OUT_DIR, "(%s)" % args.mode)

    if args.snapshot:
        shots = DISPLAY / "snapshots"
        shots.mkdir(parents=True, exist_ok=True)
        run(
            [
                CONSOLE,
                "batch",
                "exportSnapshots",
                etp,
                "-sources",
                NAME + ".sgfx",
                "-outdir",
                str(shots),
                "-format",
                "PNG",
            ]
        )
        print("snapshot in", shots)


if __name__ == "__main__":
    main()
