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

# pylint: disable=missing-docstring, no-self-use, no-self-argument

from mongoengine import Document
from mongoengine.queryset import queryset_manager
from mongomotor import Document as MMDocument


class TestDoc(Document):

    @queryset_manager
    def objects(cls_doc, queryset):
        return queryset

    def filter_qs(self):
        type(self).objects(a=1)

    def do_aggregate(self):
        pipeline = []
        return type(self).objects.aggregate(*pipeline)

    def do_update(self):
        kwargs = {'field': 'a'}
        self.objects.update(**kwargs)


class MMTestDoc(MMDocument):

    @queryset_manager
    def objects(cls_doc, queryset):
        return queryset

    def filter_qs(self):
        type(self).objects(a=1)

    def do_aggregate(self):
        pipeline = []
        return type(self).objects.aggregate(*pipeline)

    async def get_item(self):
        queryset = self.objects.order_by('-field').clone()
        await queryset[0]

    async def do_update(self):
        kwargs = {'field': 'a'}
        await self.objects.update(**kwargs)
