import mock
import sys
import pytest


class TestPythonVersion:
    def test_systemerror_python(self):
        with mock.patch.object(sys, 'version_info') as v_info:
            v_info.major = 2
            v_info.minor = 4
            v_info.micro = 10
            v_info = (v_info.major, v_info.minor, v_info.micro)
            sys.version_info = v_info
            with pytest.raises(ImportError) as e:
                import cloudpassage  # noqa: F401
            assert e
