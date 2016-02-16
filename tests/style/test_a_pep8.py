import os
import pep8
import re

integration_test_directory = os.path.abspath('./integration')
unit_test_directory = os.path.abspath('./unit')
code_directory = os.path.abspath('../cloudpassage/')


def pep8_examine(file_location):
    pep8style = pep8.StyleGuide(quiet=False)
    result = pep8style.check_files([file_location])
    return result.total_errors


def get_all_py_files(directory):
    pyfiles = []
    pattern = ".*py$"
    for f in os.listdir(directory):
        fullpath = os.path.join(directory, f)
        if (os.path.isfile(fullpath) and re.match(pattern, f)):
            pyfiles.extend([fullpath])
    return pyfiles


class TestPep8:
    def test_pep8(self):
        dirs_to_test = [integration_test_directory,
                        unit_test_directory,
                        code_directory]
        files_to_test = []
        for d in dirs_to_test:
            files_to_test.extend(get_all_py_files(d))
        for f in files_to_test:
            assert pep8_examine(f) == 0
