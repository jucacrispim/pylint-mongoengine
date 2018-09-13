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

from mongoengine import Document as MEDocument
from mongoengine.errors import DoesNotExist, MultipleObjectsReturned
from mongoengine.queryset.manager import QuerySetManager


class Document(MEDocument):  # pylint: disable=duplicate-code
    _meta = {}
    objects = QuerySetManager()

    id = None
    pk = None

    MultipleObjectsReturned = MultipleObjectsReturned
    DoesNotExist = DoesNotExist

    _data = {}
