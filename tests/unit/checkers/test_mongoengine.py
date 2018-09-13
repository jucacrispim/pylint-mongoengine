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

from unittest.mock import Mock, patch, MagicMock

from pylint_mongoengine.checkers.mongoengine import MongoEngineChecker


class TestMongoEngineChecker:

    def setup_method(self, test_method):
        linter = Mock()
        self.checker = MongoEngineChecker(linter)

    def test_called_thru_default_qs_no_last_child(self):
        node = Mock()
        node.last_child.return_value = None
        r = self.checker._called_thru_default_qs(node)
        assert r is False

    def test_called_thru_default_qs_no_objects(self):
        node = Mock()
        node.last_child.return_value.attrname = 'something'
        r = self.checker._called_thru_default_qs(node)
        assert r is False

    @patch('pylint_mongoengine.checkers.mongoengine.node_is_subclass',
           Mock(return_value=False))
    def test_called_thru_default_qs_no_qs(self):
        node = Mock()
        node.last_child.return_value.attrname = 'objects'
        base_cls = Mock()
        base_cls.inferred.return_value = [Mock()]
        node.last_child.return_value.last_child.return_value = base_cls
        r = self.checker._called_thru_default_qs(node)
        assert r is False

    @patch('pylint_mongoengine.checkers.mongoengine.node_is_subclass',
           Mock(return_value=True))
    def test_called_thru_default_qs_ok(self):
        node = Mock()
        node.last_child.return_value.attrname = 'objects'
        base_cls = Mock()
        base_cls.inferred.return_value = [Mock()]
        node.last_child.return_value.last_child.return_value = base_cls
        r = self.checker._called_thru_default_qs(node)
        assert r is True

    def test_visit_attribute_not_called_thru_qs(self):
        self.checker._called_thru_default_qs = Mock(return_value=False)
        self.checker.add_message = Mock()
        self.checker.visit_attribute(Mock())

        assert self.checker.add_message.called is False

    @patch('pylint_mongoengine.checkers.mongoengine.name_is_from_qs',
           Mock(return_value=False))
    def test_visit_attribute_not_qs_name(self):
        self.checker._called_thru_default_qs = Mock(return_value=True)
        self.checker.add_message = Mock()
        self.checker.visit_attribute(Mock())

        assert self.checker.add_message.called is True

    @patch('pylint_mongoengine.checkers.mongoengine.name_is_from_qs',
           Mock(return_value=True))
    def test_visit_attribute_qs_name(self):
        self.checker._called_thru_default_qs = Mock(return_value=True)
        self.checker.add_message = Mock()
        self.checker.visit_attribute(Mock())

        assert self.checker.add_message.called is False

    @patch('pylint_mongoengine.checkers.mongoengine.safe_infer', Mock())
    def test_visit_call_good_infer(self):
        node = MagicMock()
        r = self.checker.visit_call(node)
        assert r is False

    @patch('pylint_mongoengine.checkers.mongoengine.safe_infer',
           Mock(side_effect=[None, Mock()]))
    @patch('pylint_mongoengine.checkers.mongoengine.node_is_subclass',
           Mock(return_value=False))
    def test_visit_call_no_subclass(self):
        node = MagicMock()
        self.checker.add_message = Mock()
        self.checker.visit_call(node)
        assert self.checker.add_message.called is False

    @patch('pylint_mongoengine.checkers.mongoengine.safe_infer',
           Mock(side_effect=[None, Mock()]))
    @patch('pylint_mongoengine.checkers.mongoengine.node_is_subclass',
           Mock(return_value=True))
    @patch('pylint_mongoengine.checkers.mongoengine.name_is_from_model',
           Mock(return_value=True))
    def test_visit_call_good_name(self):
        node = MagicMock()
        self.checker.add_message = Mock()
        self.checker.visit_call(node)
        assert self.checker.add_message.called is False

    @patch('pylint_mongoengine.checkers.mongoengine.safe_infer',
           Mock(side_effect=[None, Mock()]))
    @patch('pylint_mongoengine.checkers.mongoengine.node_is_subclass',
           Mock(return_value=True))
    @patch('pylint_mongoengine.checkers.mongoengine.name_is_from_model',
           Mock(return_value=False))
    def test_visit_call_subclass_bad_name(self):
        node = MagicMock()
        self.checker.add_message = Mock()
        self.checker.visit_call(node)
        assert self.checker.add_message.called is True
