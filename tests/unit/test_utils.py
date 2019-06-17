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

from unittest.mock import Mock

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

test_doc_int = """
from mongomotor import Document
from mongomotor.fields import IntField

class Doc(Document):
    intf = IntField()
"""

test_doc_str = """
from mongomotor import Document
from mongomotor.fields import StringField

class Doc(Document):
    strf = StringField()
"""

test_doc_other_str = """
from mongomotor import Document
from mongomotor.fields import StringField

class OtherStringField(StringField):
    pass

class Doc(Document):
    strf = OtherStringField()
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


def test_node_isinstance_bad_node():
    module = astroid.parse(test_funcdef)
    funcdef = module.body[0]
    r = utils.node_is_instance(funcdef, 'mongomotor.Document')
    assert r is False


def test_node_is_instance_false():
    module = astroid.parse(test_doc_int)
    cls = module.body[2]
    node = list(cls.body[0].get_children())[-1]
    r = utils.node_is_instance(next(node.infer()),
                               'mongoengine.fields.StringField')
    assert r is False


def test_node_is_instance_true():
    module = astroid.parse(test_doc_str)
    cls = module.body[2]
    node = list(cls.body[0].get_children())[-1]
    r = utils.node_is_instance(next(node.infer()),
                               'mongoengine.fields.StringField')
    assert r is True


def test_node_is_instance_inheritance():
    module = astroid.parse(test_doc_other_str)
    cls = module.body[3]
    node = list(cls.body[0].get_children())[-1]
    r = utils.node_is_instance(next(node.infer()),
                               'mongoengine.fields.StringField')
    assert r is True


test_field_method = """
from mongomotor import Document
from mongomotor.fields import StringField

class Doc(Document):
    strf = StringField()

    def do_stuff(self):
        return self.strf.split()
"""


def test_is_field_method_true():
    m = astroid.parse(test_field_method)
    attr = m.body[2].last_child().last_child().value.last_child()
    r = utils.is_field_method(attr)
    assert r is True


test_not_field_method = """
from mongomotor import Document
from mongomotor.fields import StringField

class Doc(Document):
    strf = StringField()

    def do_stuff(self):
        return self.strf.bad()
"""


def test_is_field_method_false():
    m = astroid.parse(test_not_field_method)
    attr = m.body[2].last_child().last_child().value.last_child()
    r = utils.is_field_method(attr)
    assert r is False


def test_node_is_doc_field_true():
    m = astroid.parse(test_not_field_method)
    attr = m.body[2].last_child().last_child().value.last_child()
    parent = attr.last_child()
    r = utils.node_is_doc_field(parent)

    assert r is True


test_no_doc_field = """
from mongomotor import Document

class Doc(Document):
    something = 'bla'

    def do_stuff(self):
        return self.something.split()

"""


def test_node_is_doc_field_false():
    m = astroid.parse(test_no_doc_field)
    attr = m.body[1].last_child().last_child().value.last_child()
    parent = attr.last_child()
    r = utils.node_is_doc_field(parent)

    assert r is False


def test_node_is_doc_field_no_infer(mocker):
    mocker.patch.object(utils, 'safe_infer', Mock(return_value=False))
    m = astroid.parse(test_not_field_method)
    attr = m.body[2].last_child().last_child().value.last_child()
    parent = attr.last_child()
    r = utils.node_is_doc_field(parent)

    assert r is False


test_doc_embedded_field = """
from mongomotor import Document, EmbeddedDocument
from mongomotor.fields import EmbeddedDocumentField


class Edoc(EmbeddedDocument):

    def meth(self):
        pass


class ReqEDoc(EmbeddedDocument):

    def meth(self):
        pass


class Doc(Document):
    something = EmbeddedDocumentField(Edoc)
    other = EmbeddedDocumentField(ReqEdoc, required=True)

    def do_bad_stuff(self):
        return self.something.bad()

    def do_stuff(self):
        return self.something.meth()

"""


def test_node_is_embedded_doc():
    m = astroid.parse(test_doc_embedded_field)
    attr = m.body[4].last_child().last_child().value.last_child()
    parent = attr.last_child()
    r = utils.node_is_embedded_doc(parent)

    assert r is True


def test_get_node_parent_class():
    m = astroid.parse(test_doc_embedded_field)
    attr = m.body[4].last_child().last_child().value.last_child()
    parent = attr.last_child()
    cls = utils.get_node_parent_class(parent)

    assert isinstance(cls, utils.ClassDef)


def test_get_field_definition():
    m = astroid.parse(test_doc_embedded_field)
    attr = m.body[4].last_child().last_child().value.last_child()
    parent = attr.last_child()
    definition = utils.get_field_definition(parent)
    real_def = m.body[4].body[0]

    assert definition is real_def


def test_get_field_embedded_doc():
    m = astroid.parse(test_doc_embedded_field)
    attr = m.body[4].last_child().last_child().value.last_child()
    parent = attr.last_child()
    cls = utils.get_field_embedded_doc(parent)
    real_cls = m.body[2]

    assert cls is real_cls


def test_node_is_embedded_doc_attr_false():
    m = astroid.parse(test_doc_embedded_field)
    attr = m.body[4].body[2].last_child().last_child().last_child()
    r = utils.node_is_embedded_doc_attr(attr)

    assert r is False


def test_node_is_embedded_doc_attr_true():
    m = astroid.parse(test_doc_embedded_field)
    attr = list(m.body[4].body[3].last_child().last_child().get_children())[0]
    r = utils.node_is_embedded_doc_attr(attr)

    assert r is True
