# -*- coding: utf-8 -*-
# Copyright 2018 Juca Crispim <juca@poraodojuca.net>

# This file is part of pylint-mongoengine.

# pylint-mongoengine is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# pylint-mongoengine is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with pylint-mongoengine. If not, see <http://www.gnu.org/licenses/>.

import os
import sys
import pytest

from pylint.test import test_functional
# # because there's no __init__ file in pylint/test/
# sys.path.append(os.path.join(os.path.dirname(pylint.__file__), 'test'))
# import test_functional  # noqa: E402

# # alter sys.path again because the tests now live as a subdirectory
# # of pylint_django
# sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
# so we can find migrations
sys.path.append(os.path.join(os.path.dirname(__file__), 'input'))


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
