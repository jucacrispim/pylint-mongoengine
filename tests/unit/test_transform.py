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

from unittest.mock import patch
from pylint_mongoengine import transforms


def test_fake_module_builder():
    r = transforms.fake_module_builder('mongoengine')
    assert r.body[3].name == 'Document'


@patch('pylint_mongoengine.transforms.astroid.register_module_extender')
def test_add_transform(*args, **kwargs):
    transforms.add_transform('mongomotor')
    assert transforms.astroid.register_module_extender.called is True
