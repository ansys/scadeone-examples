"""Script to generate sine wave test data files."""

import math

import ansys.scadeone.core.svc.simdata as sd


def generate_sin():
    """Generate sine wave input and expected output data files."""
    f = sd.create_file("../resources/TestSin.sd")
    x = f.add_element("x", sd.Float32)
    expf = sd.create_file("../resources/TestSinExpected.sd")
    v = expf.add_element("v", sd.Float32)

    xs = [i / 100 * math.pi * 2 for i in range(100)]  # inputs
    x.append_values(xs)
    vs = [math.sin(x) for x in xs]  # expected outputs
    v.append_values(vs)

    f.close()
    expf.close()


if __name__ == "__main__":
    generate_sin()
