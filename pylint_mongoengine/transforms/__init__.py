# -*- coding: utf-8 -*-
# Copyright 2018 Juca Crispim <juca@poraodojuca.net>

# This file is part of pylint_mongoengine.

# pylint_mongoengine is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# pylint_mongoengine is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with pylint_mongoengine. If not, see <http://www.gnu.org/licenses/>.

import os
import re

import astroid


def fake_module_builder(package_name):
    transforms_dir = os.path.join(os.path.dirname(__file__))
    fake_module_path = os.path.join(
        transforms_dir, '%s.py' % re.sub(r'\.', '_', package_name))

    with open(fake_module_path) as modulefile:
        fake_module = modulefile.read()

    return astroid.builder.AstroidBuilder(astroid.MANAGER).string_build(
        fake_module)


def add_transform(package_name):
    """Reads the classes from the input/ directory and extends the
    original ones in asteroid.

    :param package_name: The package beeing changed.
    """

    astroid.register_module_extender(astroid.MANAGER, package_name,
                                     lambda: fake_module_builder(package_name))
