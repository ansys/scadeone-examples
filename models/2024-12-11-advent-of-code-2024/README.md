Requirements:
* Ansys Scade One 2025 R1 or later

Instructions:
1. Open project `AdventOfCode2024Day03/AdventOfCode2024Day03.sproj` in Scade One.
2. Run a debug session on sample test harnesses `Tests::Part1Sample` and `Tests::Part2Sample`.
3. To run the model on actual Advent of Code data, you must retrieve it from the website first, since Advent of Code inputs are personalized and copyrighted. To do this, please:
    - Go to https://adventofcode.com/2024/day/3
    - Authenticate through your preferred method
    - Download your personalized input and save it under `resources/input.txt`
    - Run Python script `resources/input_to_swan_consts.py`; it re-generates the Scade One model's `Input` module
    - Reload the project in the Scade One IDE
    - Run a debug session on test harnesses `Tests::Part1` and `Tests::Part2`