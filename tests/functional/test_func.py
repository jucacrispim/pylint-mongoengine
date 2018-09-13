# -*- coding: utf-8 -*-

# from pylint-django

import os
import sys

import pytest

from pylint.test import test_functional


class PylintMongoEngineLintModuleTest(test_functional.LintModuleTest):
    """
        Only used so that we can load this plugin into the linter!
    """
    def __init__(self, test_file):
        super().__init__(test_file)
        self._linter.load_plugin_modules(['pylint_mongoengine'])


def get_tests(input_dir='input', sort=False):
    def _file_name(test):
        return test.base

    HERE = os.path.dirname(os.path.abspath(__file__))
    input_dir = os.path.join(HERE, input_dir)

    suite = []
    for fname in os.listdir(input_dir):
        if fname != '__init__.py' and fname.endswith('.py'):
            suite.append(test_functional.FunctionalTestFile(input_dir, fname))

    return suite


TESTS = get_tests()
TESTS_NAMES = [t.base for t in TESTS]


@pytest.mark.parametrize("test_file", TESTS, ids=TESTS_NAMES)
def test_everything(test_file):
    # copied from pylint.tests.test_functional.test_functional
    LintTest = PylintMongoEngineLintModuleTest(test_file)
    LintTest.setUp()
    LintTest._runTest()


if __name__ == '__main__':
    sys.exit(pytest.main(sys.argv))
