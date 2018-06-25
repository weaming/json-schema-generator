import sys
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


class Base(object):
    def __init__(self, data):
        self.data = data

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
    properties = {'items': []}

    def after_gen(self, rv):
        for x in self.data:
            rv['items'].append(entry(x))


class ObjectType(Base):
    json_type = "object"
    properties = {
        'properties': {},
        'requried': [],
        "additionalProperties": False,
    }

    def after_gen(self, rv):
        for k, v in self.data.items():
            real_k = k[:-1] if k[-1] in '?!' else k
            if not k.endswith('?'):
                rv['requried'].append(k)

            rv['properties'][real_k] = entry(v, k)


class EnumType(Base):
    json_type = "string"
    properties = {'enum': []}


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
