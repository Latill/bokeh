#-----------------------------------------------------------------------------
# Copyright (c) 2012 - 2024, Anaconda, Inc., and Bokeh Contributors.
# All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# Boilerplate
#-----------------------------------------------------------------------------
from __future__ import annotations # isort:skip

import pytest ; pytest

#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------

# Standard library imports
import re
from unittest import mock

# Module under test
import bokeh.util.version as buv # isort:skip

#-----------------------------------------------------------------------------
# Setup
#-----------------------------------------------------------------------------

VERSION_PAT = re.compile(r"^(\d+\.\d+\.\d+)$")

#-----------------------------------------------------------------------------
# General API
#-----------------------------------------------------------------------------

class Test_base_version:
    def test_returns_helper(self) -> None:
        with mock.patch('bokeh.util.version._base_version_helper') as helper:
            buv.base_version()
            assert helper.called


class Test_is_full_release:
    def test_actual(self) -> None:
        assert buv.is_full_release() == bool(VERSION_PAT.match(buv.__version__))

    def test_mock_full(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(buv, '__version__', "1.5.0")
        assert buv.is_full_release()

    @pytest.mark.parametrize('v', ("1.2.3.dev2", "1.4.5.rc3", "junk"))
    def test_mock_not_full(self, monkeypatch: pytest.MonkeyPatch, v: str) -> None:
        monkeypatch.setattr(buv, '__version__', v)
        assert not buv.is_full_release()

#-----------------------------------------------------------------------------
# Dev API
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# Private API
#-----------------------------------------------------------------------------


class Test__base_version_helper:
    def test_release_version_unchanged(self) -> None:
        assert buv._base_version_helper("0.2.3") == "0.2.3"
        assert buv._base_version_helper("1.2.3") == "1.2.3"

    def test_dev_version_stripped(self) -> None:
        assert buv._base_version_helper("0.2.3.dev2") == "0.2.3"
        assert buv._base_version_helper("1.2.3.dev10") == "1.2.3"

    def test_rc_version_stripped(self) -> None:
        assert buv._base_version_helper("0.2.3.rc2") == "0.2.3"
        assert buv._base_version_helper("1.2.3.rc10") == "1.2.3"

#-----------------------------------------------------------------------------
# Code
#-----------------------------------------------------------------------------
