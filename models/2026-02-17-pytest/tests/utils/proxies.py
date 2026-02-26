from types import ModuleType
from typing import Any, TypeAlias

import pytest

from .build_proxy import build_proxy, ROOT_DIR

OperatorProxy: TypeAlias = Any


# --- 👇Below are fixtures to be customized to match the project jobs and operators --- #

@pytest.fixture(scope="session")
def cc_build_proxy(request) -> ModuleType:
    """Build the proxy for job `CCCodeGenerationJob` and return the proxy module."""
    project_path = ROOT_DIR / "CruiseControl" / "CruiseControl.sproj"
    return build_proxy(project_path, "CCCodeGenerationJob", "cc", request=request)


@pytest.fixture(scope="session")
def mgt_build_proxy(request) -> ModuleType:
    """Build the proxy for job `MgtCodeGenerationJob` and return the proxy module."""
    project_path = ROOT_DIR / "CruiseControl" / "CruiseControl.sproj"
    return build_proxy(project_path, "MgtCodeGenerationJob", "mgt", request=request)


@pytest.fixture(scope="function")
def controller(cc_build_proxy: ModuleType) -> Any:
    """Return the class for operator `CC::Controller`"""
    return cc_build_proxy.Controller_CC()


@pytest.fixture(scope="function")
def regulation_mgt(mgt_build_proxy: ModuleType) -> Any:
    """Return the class for operator `CC::RegulationMgt`"""
    return mgt_build_proxy.RegulationMgt_CC()


@pytest.fixture(scope="function")
def cruise_speed_mgt(mgt_build_proxy: ModuleType) -> Any:
    """Return the class for operator `CC::CruiseSpeedMgt`"""
    return mgt_build_proxy.CruiseSpeedMgt_CC()
