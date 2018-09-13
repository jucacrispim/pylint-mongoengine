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

# pylint: disable=missing-docstring, too-few-public-methods
# pylint: disable=no-self-use, no-self-argument

from mongoengine import Document
from mongoengine.queryset import queryset_manager
from mongomotor import Document as MMDocument


class TestDoc(Document):

    @queryset_manager
    def custom_qs_manager(cls_doc, queryset):
        return queryset

    def a_bad_qs_method(self):
        return type(self).custom_qs_manager.bad_method()  # [no-member]


class AnotherTestDoc(Document):

    def a_bad_qs_method(self):
        return type(self).objects.bad_method()  # [no-member]


class MMTestDoc(MMDocument):

    @queryset_manager
    def custom_qs_manager(cls_doc, queryset):
        return queryset

    def a_bad_qs_method(self):
        return type(self).custom_qs_manager.bad_method()  # [no-member]


class AnotherMMTestDoc(MMDocument):

    def a_bad_qs_method(self):
        return type(self).objects.bad_method()  # [no-member]
