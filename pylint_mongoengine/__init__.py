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

from pylint_mongoengine.checkers.mongoengine import MongoEngineChecker
from pylint_mongoengine.suppression import suppress_qs_decorator_messages
from pylint_mongoengine.transforms import add_transform


def register(linter):
    """Add the needed transformations and supressions.
    """

    linter.register_checker(MongoEngineChecker(linter))
    add_transform('mongoengine')
    add_transform('mongomotor')
    suppress_qs_decorator_messages(linter)
