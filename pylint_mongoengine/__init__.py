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
import re

import astroid

from pylint.checkers.utils import safe_infer
from pylint.checkers.typecheck import TypeChecker
from pylint_plugin_utils import suppress_message


def _is_qs_manager(funcdef):
    """Checks if a function definition is a queryset manager created
    with the @queryset_manager decorator."""

    decors = getattr(funcdef, 'decorators', None)
    if decors:
        for dec in decors.get_children():
            try:
                if dec.name == 'queryset_manager':
                    return True
            except AttributeError:
                continue

    return False


def _is_call2manager(node):
    called = safe_infer(node.func)
    funcdef = getattr(called, '_proxied', None)
    return _is_qs_manager(funcdef)


def _is_manager_attribute(node):
    for attr in node.get_children():
        try:
            inferred = safe_infer(attr)
        except astroid.exceptions.InferenceError:
            continue

        funcdef = getattr(inferred, '_proxied', None)
        if _is_qs_manager(funcdef):
            return True

    return False


def add_transform(package_name):
    """From pylint-django"""

    def fake_module_builder():
        transforms_dir = os.path.join(os.path.dirname(__file__), 'transforms')
        fake_module_path = os.path.join(
            transforms_dir, '%s.py' % re.sub(r'\.', '_', package_name))

        with open(fake_module_path) as modulefile:
            fake_module = modulefile.read()

        return astroid.builder.AstroidBuilder(astroid.MANAGER).string_build(
            fake_module)

    astroid.register_module_extender(astroid.MANAGER, package_name,
                                     fake_module_builder)


def suppress_qs_decorator_messages(linter):
    suppress_message(linter, TypeChecker.visit_call, 'unexpected-keyword-arg',
                     _is_call2manager)
    suppress_message(linter, TypeChecker.visit_call, 'no-value-for-parameter',
                     _is_call2manager)
    suppress_message(linter, TypeChecker.visit_attribute, 'no-member',
                     _is_manager_attribute)


def register(linter):
    """
    Registering additional checkers.

    However, we will also use it to amend existing checker config.
    """

    add_transform('mongoengine')
    add_transform('mongomotor')
    suppress_qs_decorator_messages(linter)
