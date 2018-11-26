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

import astroid
from pylint_mongoengine import utils
from pylint_mongoengine.checkers.mongoengine import DOCUMENT_BASES


def test_name_is_from_qs_true():
    attrname = 'filter'
    r = utils.name_is_from_qs(attrname)
    assert r is True


def test_name_is_from_qs_false():
    attrname = 'i_dont_exist'
    r = utils.name_is_from_qs(attrname)
    assert r is False


def test_name_is_from_model_true():
    attrname = 'delete'
    r = utils.name_is_from_model(attrname)
    assert r is True


def test_name_is_from_model_false():
    attrname = 'who_are_you'
    r = utils.name_is_from_model(attrname)
    assert r is False


test_doc = """
from mongomotor import Document

class TestDoc(Document):
    meta = {'inherit': True}


class OtherDoc(TestDoc):
    pass
"""

test_cls = """
class TestCls:
    pass
"""

test_funcdef = """
def bla():
    pass
"""


def test_node_is_subclass_false():
    module = astroid.parse(test_cls)
    cls = module.body[0]
    r = utils.node_is_subclass(cls, *DOCUMENT_BASES)
    assert r is False


def test_node_is_subclass_true():
    module = astroid.parse(test_doc)
    cls = module.body[2]
    r = utils.node_is_subclass(cls, *DOCUMENT_BASES)
    assert r is True


def test_node_is_subclass_bad_node():
    module = astroid.parse(test_funcdef)
    funcdef = module.body[0]
    r = utils.node_is_subclass(funcdef, *DOCUMENT_BASES)
    assert r is False
