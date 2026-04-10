"""Small test script for low-pass filter."""

from pathlib import Path
import sys

harness_dir = Path.resolve(Path()) / "LowPassRC_Python"
sys.path.append(harness_dir)
from LowPassRC_Python import LowPassRC_LowPassRC  # noqa E402

lowpassfilter = LowPassRC_LowPassRC()
lowpassfilter.reset()
lowpassfilter.inputs.alpha = 0.11163521170465973

for i in range(0, 50):
    lowpassfilter.inputs.x = 0.0
    lowpassfilter.cycle()
    print(lowpassfilter.outputs.y)
for i in range(0, 50):
    lowpassfilter.inputs.x = 1.0
    lowpassfilter.cycle()
    print(lowpassfilter.outputs.y)
