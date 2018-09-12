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

# pylint: disable=missing-docstring

from mongoengine import Document
from mongomotor import Document as MMDocument


class TestDoc(Document):

    @classmethod
    def create_obj(cls, **kwargs):
        doc = cls(**kwargs)
        doc.save()
        doc.reload()
        return doc

    def update_obj(self):
        self.update(something='bla')

    def remove(self):
        self.delete()


TestDoc.ensure_indexes()


class MMTestDoc(MMDocument):

    @classmethod
    async def create_obj(cls, **kwargs):
        doc = cls(**kwargs)
        await doc.save()
        await doc.reload()
        return doc

    async def update_obj(self):
        await self.update(something='bla')

    async def remove(self):
        await self.delete()

MMTestDoc.ensure_indexes()
MMTestDoc.drop_collection()
