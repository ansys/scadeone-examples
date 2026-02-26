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
# ruff: noqa: D100

from types import ModuleType
from typing import Any, TypeAlias

import pytest

from .build_proxy import ROOT_DIR, build_proxy

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
    """Return the class for operator `CC::Controller`."""
    return cc_build_proxy.Controller_CC()


@pytest.fixture(scope="function")
def regulation_mgt(mgt_build_proxy: ModuleType) -> Any:
    """Return the class for operator `CC::RegulationMgt`."""
    return mgt_build_proxy.RegulationMgt_CC()


@pytest.fixture(scope="function")
def cruise_speed_mgt(mgt_build_proxy: ModuleType) -> Any:
    """Return the class for operator `CC::CruiseSpeedMgt`."""
    return mgt_build_proxy.CruiseSpeedMgt_CC()
