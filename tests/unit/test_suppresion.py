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

from unittest.mock import Mock, MagicMock, patch

from pylint_mongoengine import suppression


def test_is_custom_qs_ok():
    funcdef = Mock()
    dec = Mock()
    dec.name = 'queryset_manager'
    funcdef.decorators.get_children.return_value = [None, dec]
    r = suppression._is_custom_qs_manager(funcdef)
    assert r is True


def test_is_custom_qs_no_qs():
    funcdef = Mock()
    funcdef.decorators.get_children.return_value = []
    r = suppression._is_custom_qs_manager(funcdef)
    assert r is False


def test_is_call2custom_manager():
    node = MagicMock()
    node._proxied = MagicMock()
    r = suppression._is_call2custom_manager(node)
    assert r is False


def test_is_custom_manager_attribute_bad_name():
    node = MagicMock()
    node.attrname = 'not_from_qs'
    r = suppression._is_custom_manager_attribute(node)
    assert r is False


@patch.object(suppression, '_is_custom_qs_manager', Mock(return_value=False))
def test_is_custom_manager_attribute_no_qs_manager():
    node = MagicMock()
    node.attrname = 'filter'
    node.get_children.return_value = [MagicMock()]
    r = suppression._is_custom_manager_attribute(node)
    assert r is False


@patch.object(suppression, '_is_custom_qs_manager', Mock(return_value=True))
def test_is_custom_manager_attribute_true():
    node = MagicMock()
    node.attrname = 'filter'
    node.get_children.return_value = [MagicMock()]
    r = suppression._is_custom_manager_attribute(node)
    assert r is True


@patch.object(suppression, 'node_is_embedded_doc', Mock(return_value=True))
@patch.object(suppression, 'node_is_embedded_doc_attr',
              Mock(return_value=True))
def test_is_embedded_doc_attr_true():
    node = MagicMock()
    r = suppression._is_embedded_doc_attr(node)

    assert r is True


@patch.object(suppression, 'node_is_embedded_doc', Mock(return_value=False))
@patch.object(suppression, 'node_is_embedded_doc_attr',
              Mock(return_value=True))
def test_is_embedded_doc_attr_false():
    node = MagicMock()
    r = suppression._is_embedded_doc_attr(node)

    assert r is False
