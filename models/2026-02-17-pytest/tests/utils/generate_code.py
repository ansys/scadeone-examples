"""Generate code and Proxies for the tests"""
from build_proxy import ROOT_DIR, build_proxy  # type: ignore

project_path = ROOT_DIR / "CruiseControl" / "CruiseControl.sproj"
jobs = [("CCCodeGenerationJob", "cc"), ("MgtCodeGenerationJob", "mgt")]

for job_name, wrapper_name in jobs:
    print("=" * 20 + f" Generating code for job '{job_name}'" + "=" * 20)
    build_proxy(project_path, job_name, wrapper_name)
    print(f" => Generation done for {job_name}.\n")
