# -*- coding: utf-8 -*-

from astroid.bases import Instance
from astroid.nodes import ClassDef
from astroid.exceptions import InferenceError
from pylint.checkers.utils import safe_infer

FIELD_TYPES = {'mongoengine.fields.StringField': str(),
               'mongoengine.fields.IntField': int(),
               'mongoengine.fields.FloatField': float(),
               'mongoengine.fields.ListField': list(),
               'mongoengine.fields.DictField': dict()}


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


def node_is_instance(inst, *cls_names):
    if not isinstance(inst, Instance):
        return False

    if inst.qname() in cls_names:
        return True
    if node_is_subclass(inst, *cls_names):
        return True
    return False


def node_is_doc_field(node):
    inferred = safe_infer(node)
    if not inferred:
        return False

    return node_is_instance(inferred, 'mongoengine.base.fields.BaseField',
                            'mongoengine.base.fields.ComplexBaseField')


def is_field_method(node):
    """Checks if a call to a field instance method is valid. A call is
    valid if the call is a method of the underlying type. So, in a StringField
    the methods from str are valid, in a ListField the methods from list are
    valid and so on..."""
    name = node.attrname
    parent = node.last_child()
    inferred = safe_infer(parent)

    if not inferred:
        return False

    for cls_name, inst in FIELD_TYPES.items():
        if node_is_instance(inferred, cls_name) and hasattr(inst, name):
            return True

    return False
