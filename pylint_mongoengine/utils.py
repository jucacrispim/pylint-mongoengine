# -*- coding: utf-8 -*-

# from pylint-django

# from astroid.util import YES
from astroid.bases import Instance
from astroid.nodes import ClassDef
from astroid.exceptions import InferenceError

qs_names = set()
model_names = set()


def name_is_from_qs(attrname):
    global qs_names  # pylint: disable=global-statement

    if not qs_names:
        from mongoengine.queryset import QuerySet
        qs_names = set(dir(QuerySet))

    return attrname in qs_names


def name_is_from_model(attrname):
    global model_names  # pylint: disable=global-statement

    if not model_names:
        from mongoengine import Document
        model_names = set(dir(Document))

    return attrname in model_names


def node_is_subclass(cls, *subclass_names):
    """Checks if cls node has parent with subclass_name."""
    if not isinstance(cls, (ClassDef, Instance)):
        return False

    # if cls.bases == YES:
    #     return False
    for base_cls in cls.bases:
        try:
            for inf in base_cls.inferred():  # pragma no branch
                if inf.qname() in subclass_names:
                    return True

                if inf != cls and node_is_subclass(  # pragma no branch
                        inf, *subclass_names):
                    # check up the hierarchy in case we are a subclass of
                    # a subclass of a subclass ...
                    return True
        except InferenceError:  # pragma no cover
            continue

    return False
