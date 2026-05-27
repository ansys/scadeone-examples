Requirements:
* Ansys Scade One 2026 R1 or later
* Python 3.10 or later
* Graphviz

Instructions:
1. Install dependencies with `pip install -r requirements.txt`.
2. Install [Graphviz](https://graphviz.org/) and ensure that Graphviz's `bin` directory is part of your `PATH` environment variable.
3. Run the script on your model of choice with `python instance_tree.py "C:\path\to\my\scade\one\project.sproj" "RootModule::RootOperator"`.
4. The script should generate a diagram image called `RootModule_RootOperator_graph.png`.
