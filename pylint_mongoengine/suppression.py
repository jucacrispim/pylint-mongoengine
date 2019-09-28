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

from astroid.exceptions import InferenceError
from pylint.checkers.typecheck import TypeChecker, IterableChecker
from pylint.checkers.utils import safe_infer
from pylint_plugin_utils import suppress_message
from pylint_mongoengine.utils import (name_is_from_qs, is_field_method,
                                      node_is_embedded_doc,
                                      node_is_embedded_doc_attr,
                                      node_is_complex_field,
                                      node_is_document,
                                      name_is_from_model,
                                      node_is_default_qs,
                                      name_is_doc_callable)


def _is_custom_qs_manager(funcdef):
    """Checks if a function definition is a queryset manager created
    with the @queryset_manager decorator."""

    decors = getattr(funcdef, 'decorators', None)
    if decors:
        for dec in decors.get_children():
            attrname = 'name' if hasattr(dec, 'name') else 'attrname'
            qs_name = 'queryset_manager'
            try:
                if getattr(dec, attrname) == qs_name:  # pragma no branch
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


def _is_complex_field_for(node):
    attr = list(node.get_children())[1]
    r = node_is_complex_field(attr)
    return r


def _is_complex_field_compare(node):
    r = False
    _, right = node.ops[0]
    r = node_is_complex_field(right)
    return r


def _is_complex_field_subscript(node):
    attr = node.value
    r = node_is_complex_field(attr)
    return r


def _is_document_field(node):
    """Checks if a node is a valid document field."""
    try:
        inf = next(node.get_children()).inferred()[0]
    except InferenceError:
        return False
    return node_is_document(inf) and name_is_from_model(node.attrname)


def _is_doc_call(node):
    """Checks if node is a valid callable for a document.
    """
    call_node = next(node.get_children())
    call_name = getattr(call_node, 'attrname', None) or getattr(
        call_node, 'name', None)
    if not call_name:
        return False
    # if is a doc call this is a doc
    maybe_doc = node.last_child().last_child()
    if not maybe_doc:
        return False
    try:
        doc_node = maybe_doc.inferred()[0]
    except InferenceError:
        return False

    return node_is_document(doc_node) and name_is_doc_callable(call_name)


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


def suppress_fields_messages(linter):
    suppress_message(linter, IterableChecker.visit_for,
                     'not-an-iterable', _is_complex_field_for)

    suppress_message(linter, TypeChecker.visit_compare,
                     'unsupported-membership-test', _is_complex_field_compare)
    suppress_message(linter, TypeChecker.visit_subscript,
                     'unsupported-assignment-operation',
                     _is_complex_field_subscript)
    suppress_message(linter, TypeChecker.visit_subscript,
                     'unsupported-delete-operation',
                     _is_complex_field_subscript)


def suppress_doc_messages(linter):
    suppress_message(linter, TypeChecker.visit_attribute, 'no-member',
                     _is_document_field)
    suppress_message(linter, TypeChecker.visit_attribute, 'no-member',
                     node_is_default_qs)
    suppress_message(linter, TypeChecker.visit_call, 'not-callable',
                     _is_doc_call)
