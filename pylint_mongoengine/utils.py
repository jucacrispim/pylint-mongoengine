# -*- coding: utf-8 -*-

from astroid.bases import Instance
from astroid.nodes import ClassDef
from astroid.exceptions import InferenceError
from mongoengine import Document
from mongoengine.queryset import QuerySet
from pylint.checkers.utils import safe_infer

DOCUMENT_BASES = ('mongomotor.Document',
                  'mongoengine.Document',
                  'mongoengine.document.Document',
                  'mongomotor.document.Document')


FIELD_TYPES = {'mongoengine.fields.StringField': str(),
               'mongoengine.fields.IntField': int(),
               'mongoengine.fields.FloatField': float(),
               'mongoengine.fields.ListField': list(),
               'mongoengine.fields.DictField': dict()}


qs_names = set()
document_names = set()


def name_is_from_qs(attrname):
    global qs_names  # pylint: disable=global-statement

    if not qs_names:
        qs_names = set(dir(QuerySet))

    return attrname in qs_names


def name_is_from_model(attrname):
    global document_names  # pylint: disable=global-statement

    if not document_names:
        document_names = set(dir(Document))
        # these attributes are dynamically created
        document_names.add('id')
        document_names.add('objects')
        document_names.add('DoesNotExist')
        document_names.add('MultipleObjectsReturned')

    return attrname in document_names


def name_is_doc_callable(attrname):
    """Checks if a name is a callable in a document"""
    is_call = callable(getattr(Document, attrname, None))
    return name_is_from_model and is_call


def node_is_subclass(cls, *subclass_names):
    """Checks if cls node has parent with subclass_name."""
    if not isinstance(cls, (ClassDef, Instance)):
        return False

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


def node_is_document(node):
    """Checks if a node is a mongoengine document class.
    """
    return node_is_subclass(node, *DOCUMENT_BASES)


def node_is_doc_instance(node):
    return node_is_instance(node, *DOCUMENT_BASES)


def node_is_doc_field(node):
    inferred = safe_infer(node)
    if not inferred:
        return False

    return node_is_instance(inferred, 'mongoengine.base.fields.BaseField',
                            'mongoengine.base.fields.ComplexBaseField')


def node_is_default_qs(node):
    # the default qs manager is called 'objects', we check for it here
    attrname = getattr(node, 'attrname', None)
    if attrname != 'objects':
        return False

    base_cls = node.last_child()
    for cls in base_cls.inferred():
        if node_is_document(cls):
            return True

    return False


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


def get_node_parent_class(node):
    """Supposes that node is a mongoengine field in a class and tries to
    get its parent class"""

    while node.parent:  # pragma no branch
        if isinstance(node, ClassDef):
            return node

        node = node.parent


def node_is_embedded_doc(node):
    cls_name = 'mongoengine.fields.EmbeddedDocumentField'
    inferred = safe_infer(node)
    if not inferred:
        return False

    return node_is_instance(inferred, cls_name)


def get_field_definition(node):
    """"node is a class attribute that is a mongoengine. Returns
     the definition statement for the attribute
    """

    name = node.attrname
    cls = get_node_parent_class(node)
    definition = cls.lookup(name)[1][0].statement()
    return definition


def get_field_embedded_doc(node):
    """Returns de ClassDef for the related embedded document in a
    embedded document field."""

    definition = get_field_definition(node)
    cls_name = list(definition.last_child().get_children())[1]
    cls = next(cls_name.infer())
    return cls


def node_is_embedded_doc_attr(node):
    """Checks if a node is a valid field or method in a embedded document.
    """
    embedded_doc = get_field_embedded_doc(node.last_child())
    name = node.attrname
    try:
        r = bool(embedded_doc.lookup(name)[1][0])
    except (IndexError, TypeError):
        r = False

    return r


def node_is_complex_field(node):
    cls_name = 'mongoengine.base.fields.ComplexBaseField'
    inferred = safe_infer(node)
    r = node_is_subclass(inferred, cls_name)
    return r
