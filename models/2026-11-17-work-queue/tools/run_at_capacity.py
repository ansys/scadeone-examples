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

"""Run the work-queue checks at another queue capacity.

    python tools/run_at_capacity.py 10000

Copies assets/ to a temporary folder, sets `const N` in JobList.swani, then:
  1. runs every harness of Demo.swant with the Scade One simulator;
  2. generates C for WorkQueue::controller and View::panel;
  3. compiles it with the bundled GCC (-O0 -fstack-usage) and prints the
     persistent context sizes and the largest stack frame.
Nothing in the project is modified. Requires Scade One 2027 R1 (v271);
set SCADE_ONE_HOME to override the default install path.
"""

import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

HOME = Path(
    os.environ.get("SCADE_ONE_HOME", r"C:\Program Files\ANSYS Inc\v271\Scade One")
)
SIM = HOME / "tools" / "simulator" / "swan_sim.exe"
CG = HOME / "tools" / "swan_cg.exe"
GCC = HOME / "contrib" / "mingw64" / "bin" / "gcc.exe"
INCLUDE = HOME / "resources" / "include"
ASSETS = Path(__file__).resolve().parent.parent / "work-queue" / "assets"
MODEL = [
    "Job.swan",
    "Job.swani",
    "JobList.swan",
    "JobList.swani",
    "WorkQueue.swan",
    "View.swan",
]
ROOTS = {
    "controller": (
        ["WorkQueue::controller", "WorkQueue::scenario"],
        "controller_WorkQueue",
    ),
    "panel": (["View::panel"], "panel_View"),
}


def run(cmd, cwd):
    """Run `cmd` in `cwd` with the bundled GCC on the PATH."""
    env = dict(os.environ, PATH=str(GCC.parent) + os.pathsep + os.environ["PATH"])
    cmd = [str(c) for c in cmd]
    return subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True)


def main(capacity):
    """Run the checks at capacity `capacity`; return the exit code."""
    work = Path(tempfile.mkdtemp(prefix="wq%d_" % capacity))
    assets = work / "assets"
    shutil.copytree(ASSETS, assets)
    interface = assets / "JobList.swani"
    text = interface.read_text(encoding="utf-8")
    text, count = re.subn(
        r"const N: uint32 = \d+;", "const N: uint32 = %d;" % capacity, text
    )
    assert count == 1, "const N not found in JobList.swani"
    with interface.open("w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    files = [str(assets / f) for f in MODEL]
    ok = True

    tests = assets / "Demo.swant"
    harnesses = [
        "Demo::" + h
        for h in re.findall(r"^_harness (\w+)", tests.read_text(encoding="utf-8"), re.M)
    ]
    sim_dir = work / "sim"
    sim_dir.mkdir(parents=True)
    with (sim_dir / "config.json").open("w") as f:
        json.dump(
            {
                "model_files": files + [str(tests)],
                "test_harnesses": harnesses,
                "output_test_results_file": "out/testResults.json",
            },
            f,
        )
    result = run([SIM, "config.json"], sim_dir)
    print("N = %d" % capacity)
    for line in result.stdout.splitlines():
        if line.startswith("(") or "executed" in line:
            print("  " + line)
    ok &= (
        result.returncode == 0
        and " 0 failed" in result.stdout
        and " 0 error" in result.stdout
    )

    for name, (roots, header) in ROOTS.items():
        out = work / name
        out.mkdir(parents=True)
        config = out / "cg.json"
        with config.open("w") as f:
            json.dump(
                {
                    "files": files,
                    "roots": roots,
                    "target": "C",
                    "target_dir": str(out / "gen"),
                },
                f,
            )
        result = run([CG, config], out)
        if result.returncode != 0:
            print("  %s: code generation failed" % name)
            ok = False
            continue
        code = out / "gen" / "code"
        sources = [str(p) for p in code.iterdir() if p.suffix == ".c"]
        result = run(
            [GCC, "-std=c11", "-O0", "-fstack-usage", "-I", code, "-I", INCLUDE, "-c"]
            + sources,
            out,
        )
        probe = out / "size.c"
        probe.write_text(
            '#include <stdio.h>\n#include "%s.h"\nint main(void)'
            '{printf("%%zu", sizeof(outC_%s));return 0;}\n' % (header, header)
        )
        objects = [p.name for p in out.iterdir() if p.suffix == ".o"]
        result = run(
            [GCC, "-std=c11", "-I", code, "-I", INCLUDE, "size.c"]
            + objects
            + ["-o", "size.exe"],
            out,
        )
        size = run([out / "size.exe"], out).stdout
        frames = []
        for p in out.iterdir():
            if p.suffix == ".su":
                with p.open() as f:
                    for line in f:
                        function, bytes_, _ = line.rsplit("\t", 2)
                        frames.append((int(bytes_), function.rsplit(":", 1)[-1]))
        top = max(frames)
        print(
            "  %-10s context %8s bytes, largest frame %d bytes (%s), all frames %d bytes"
            % (name, size, top[0], top[1], sum(b for b, _ in frames))
        )
    shutil.rmtree(work, ignore_errors=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(int(sys.argv[1]) if len(sys.argv) > 1 else 10000))
