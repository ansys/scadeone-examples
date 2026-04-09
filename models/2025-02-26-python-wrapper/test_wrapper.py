import sys, os

harness_dir = os.path.join(os.path.abspath(''), 'LowPassRC_Python')
sys.path.append(harness_dir)
from LowPassRC_Python import LowPassRC_LowPassRC

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
