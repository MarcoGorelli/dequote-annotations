import os
import shutil
import sys

import pytest

from no_string_hints import main


def test_main(tmpdir):
    test_file = os.path.join('tests', 'data', 't.py')
    tmp_test_file = os.path.join(tmpdir, 't.py')
    shutil.copy(test_file, tmp_test_file)

    main((tmp_test_file,))

    with open(tmp_test_file) as fd:
        result = fd.read()

    with open(os.path.join('tests', 'data', 't_expected.py')) as fd:
        expected = fd.read()

    assert result == expected


@pytest.mark.skipif(
    sys.version_info.major != 3 or sys.version_info.minor != 8,
    reason='posonly args not available in Python3.7',
)
def test_posonly_kwonly(tmpdir):
    test_file = os.path.join('tests', 'data', 't_py38.py')
    tmp_test_file = os.path.join(tmpdir, 't.py')
    shutil.copy(test_file, tmp_test_file)

    main((tmp_test_file,))

    with open(tmp_test_file) as fd:
        result = fd.read()

    with open(os.path.join('tests', 'data', 't_py38_expected.py')) as fd:
        expected = fd.read()

    assert result == expected


def test_main_no_change(tmpdir):
    test_file = os.path.join('tests', 'data', 't_no_change.py')
    tmp_test_file = os.path.join(tmpdir, 't.py')
    shutil.copy(test_file, tmp_test_file)

    main((tmp_test_file,))

    with open(tmp_test_file) as fd:
        result = fd.read()

    with open(os.path.join('tests', 'data', 't_no_change.py')) as fd:
        expected = fd.read()

    assert result == expected
