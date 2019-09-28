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

from pylint.checkers import BaseChecker
from pylint.checkers.utils import check_messages
from pylint.interfaces import IAstroidChecker

from pylint_mongoengine.utils import (
    name_is_from_qs,
    node_is_default_qs,
)


class MongoEngineChecker(BaseChecker):

    __implements__ = IAstroidChecker

    name = 'mongoengine-checker'

    msgs = {
        'W6199': ('Placeholder message to prevent disabling of checker',
                  'mongoengine-placeholder',
                  'PyLint does not recognise checkers as being enabled unless'
                  '  they have at least one message which is not fatal...')
    }

    def _called_thru_default_qs(self, node):
        """Checks if an attribute is being accessed throught the default
        queryset manager, ie: MyClass.objects.filter(some='value')"""
        last_child = node.last_child()
        if not last_child:
            return False
        return node_is_default_qs(last_child)

    def check_qs_name(self, node):
        if self._called_thru_default_qs(node) and not name_is_from_qs(
                node.attrname):
            self.add_message('no-member', node=node, args=(
                'QuerySet instance', 'objects', node.attrname, ''))

    @check_messages('no-member')
    def visit_attribute(self, node):
        self.check_qs_name(node)
