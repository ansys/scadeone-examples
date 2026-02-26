import os
import sys
from importlib import import_module
from pathlib import Path
from types import ModuleType
from typing import Optional, Union

import pytest
from ansys.scadeone.core import ScadeOne
from ansys.scadeone.core.svc.wrapper import PythonWrapper

from environment import S_ONE_INSTALL_DIR  # type: ignore


PathType = Union[str, os.PathLike[str]]
TEST_DIR = Path(__file__).parent.parent
ROOT_DIR = TEST_DIR.parent


sys.path.insert(0, str(TEST_DIR))


def build_proxy(
    project_path: Path,
    job_name: str,
    wrapper_name: str,
    request: Optional[pytest.FixtureRequest] = None,
    out_dir: PathType = TEST_DIR / "proxy",
) -> ModuleType:
    """Build the proxy code for the given project / job and returned the proxy module."""
    out_dir = Path(out_dir)
    if request is None:
        skip_codegen = False
    else:
        skip_codegen = request.config.getoption("--no-codegen")

    print(f"Project path is {project_path}")
    assert project_path.is_file(), f"Project path {project_path} does not exist"
    app = ScadeOne(install_dir=S_ONE_INSTALL_DIR)
    prj = app.load_project(project_path)
    assert prj is not None, f"Failed to load project {project_path}"
    prj.load_jobs()

    job = prj.get_job(job_name)
    assert job is not None, f"Failed to get {job_name} job"
    if not skip_codegen:
        result = job.run()
        assert result.code == 0

        gen = PythonWrapper(
            project=prj, job=job_name, output=wrapper_name, target_dir=out_dir
        )
        gen.generate()

    dll = out_dir / wrapper_name / f"{wrapper_name}.dll"
    print(f"Expecting dll in {dll}")
    assert dll.exists(), f"Wrapper of {wrapper_name} not built correctly: missing {dll}"

    return import_module(f"proxy.{wrapper_name}.{wrapper_name}")
