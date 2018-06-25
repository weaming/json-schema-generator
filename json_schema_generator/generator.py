import os
import sys
import json
from pretty_format_json.format import get_text, parse_text
from collections import OrderedDict
from .types import entry


class Generator(object):
    def __init__(self, data, include_origin=False, indent=2):
        self.data = data
        self.include_origin = include_origin
        self.indent = indent
        self.schema_version = os.getenv(
            'JSON_SCHEMA_VERSION', "http://json-schema.org/draft-04/schema#")

    def meta(self):
        return OrderedDict([
            ('$schema', self.schema_version),
            ('version', 1),
        ])

    def generate(self):
        rv = self.meta()
        body = entry(self.data)
        rv.update(body)
        if self.include_origin:
            rv['$origin'] = self.data
        return rv

    def output(self, filepath=None):
        c = json.dumps(self.generate(), ensure_ascii=False, indent=self.indent)

        print(c)
        if filepath:
            with open(filepath, 'w') as f:
                f.write(c)


def help():
    print(""" Usage:
    cat sample.json | generate-json-schema
    generate-json-schema sample.json
    generate-json-schema sample.json > output.schema.json
    """)


def main():
    fp = None
    if len(sys.argv) > 1:
        fp = sys.argv[1]

    if fp == 'help':
        help()
        return

    text = get_text(fp)
    data = parse_text(text)
    g = Generator(data)
    g.output()


if __name__ == "__main__":
    main()
