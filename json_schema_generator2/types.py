import sys
import re
import os
from copy import deepcopy


def get_schema_type_for(data, key=None):
    t = type(data)
    if key and key[-1] == '!':
        schema_type = EnumType
    else:
        schema_type = SCHEMA_TYPES.get(t)

    if not schema_type:
        raise JsonSchemaTypeNotFound(
            "There is no schema type for %s.\n Try:\n %s" %
            (str(t), ",\n".join(["\t%s" % str(k)
                                 for k in SCHEMA_TYPES.keys()])))

    return schema_type


def entry(data, key=None):
    obj = get_schema_type_for(data, key)(data)
    return obj.gen()


def underscore(name):
    name = name.replace(' ', '_')
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


class Base(object):
    def __init__(self, data):
        self.data = data
        self.after_init()

    def after_init(self):
        pass

    def gen(self):
        rv = {
            "type": self.json_type,
        }
        if hasattr(self, 'properties'):
            rv.update(deepcopy(self.properties))

        if hasattr(self, 'after_gen'):
            self.after_gen(rv)
        return rv


class NumberType(Base):
    json_type = "number"


class IntegerType(Base):
    json_type = "integer"


class StringType(Base):
    json_type = "string"


class NullType(Base):
    json_type = "null"


class BooleanType(Base):
    json_type = "boolean"


class ArrayType(Base):
    json_type = "array"

    def after_gen(self, rv):
        if len(self.data) > 0:
            t = get_schema_type_for(self.data[0]).json_type
            if t == ObjectType.json_type:
                rv['items'] = entry(self.data[0])
            else:
                rv['items'] = {'type': t}


class ObjectType(Base):
    json_type = "object"
    properties = {
        'properties': {},
        'required': [],
        'additionalProperties': False,
    }

    @staticmethod
    def get_real_key(k):
        return k[:-1] if k[-1] in '?!' else k

    def after_gen(self, rv):
        for k, v in self.data.items():
            real_k = self.get_real_key(k)
            if not k.endswith('?'):
                rv['required'].append(real_k)

            rv['properties'][real_k] = entry(v, k)
            if os.getenv('JSON_SCHEMA_TITLE'):
                rv['properties'][real_k]['title'] = real_k.replace(
                    '_', ' ').title()
            if os.getenv('JSON_SCHEMA_ID'):
                rv['properties'][real_k]['id'] = underscore(real_k)


class EnumType(Base):
    json_type = "string"
    properties = {'enum': []}

    def after_init(self):
        self.json_type = get_schema_type_for(self.data).json_type
        assert self.json_type not in ['object', 'array']

    def after_gen(self, rv):
        rv['enum'].append(self.data)


class JsonSchemaTypeNotFound(Exception):
    pass


SCHEMA_TYPES = {
    type(None): NullType,
    str: StringType,
    int: IntegerType,
    float: NumberType,
    bool: BooleanType,
    list: ArrayType,
    dict: ObjectType,
}
