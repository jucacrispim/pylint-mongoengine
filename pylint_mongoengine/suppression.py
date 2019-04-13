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

from pylint.checkers.typecheck import TypeChecker
from pylint.checkers.utils import safe_infer
from pylint_plugin_utils import suppress_message
from pylint_mongoengine.utils import (name_is_from_qs, is_field_method,
                                      node_is_embedded_doc,
                                      node_is_embedded_doc_attr)


def _is_custom_qs_manager(funcdef):
    """Checks if a function definition is a queryset manager created
    with the @queryset_manager decorator."""

    decors = getattr(funcdef, 'decorators', None)
    if decors:
        for dec in decors.get_children():
            try:
                if dec.name == 'queryset_manager':  # pragma no branch
                    return True
            except AttributeError:
                continue

    return False


def _is_call2custom_manager(node):
    """Checks if the call is being done to a custom queryset manager."""
    called = safe_infer(node.func)
    funcdef = getattr(called, '_proxied', None)
    return _is_custom_qs_manager(funcdef)


def _is_custom_manager_attribute(node):
    """Checks if the attribute is a valid attribute for a queryset manager.
    """

    attrname = node.attrname
    if not name_is_from_qs(attrname):
        return False

    for attr in node.get_children():
        inferred = safe_infer(attr)
        funcdef = getattr(inferred, '_proxied', None)
        if _is_custom_qs_manager(funcdef):
            return True

    return False


def _is_embedded_doc_attr(node):
    if node_is_embedded_doc(
            node.last_child()) and node_is_embedded_doc_attr(node):

        return True

    return False


def suppress_qs_decorator_messages(linter):
    suppress_message(linter, TypeChecker.visit_call, 'unexpected-keyword-arg',
                     _is_call2custom_manager)
    suppress_message(linter, TypeChecker.visit_call, 'no-value-for-parameter',
                     _is_call2custom_manager)
    suppress_message(linter, TypeChecker.visit_attribute, 'no-member',
                     _is_custom_manager_attribute)


def suppress_fields_attrs_messages(linter):
    suppress_message(linter, TypeChecker.visit_attribute, 'no-member',
                     is_field_method)
    suppress_message(linter, TypeChecker.visit_attribute, 'no-member',
                     _is_embedded_doc_attr)
