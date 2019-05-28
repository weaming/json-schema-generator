# JSON schema generator

Generate the initial json schema from your given example json.

## Install

    pip install json-schema-generator2

## Usage

```
$ generate-json-schema help
 Usage:
    cat sample.json | generate-json-schema
    generate-json-schema sample.json
    generate-json-schema sample.json > output.schema.json
```

## Envrioment variables

* `JSON_SCHEMA_ID`
* `JSON_SCHEMA_TITLE`

## Special rules to determine the type

* suffix definitions
    * `?`: optional
    * `!`: `enum`
    * `!?`: optional `enum`
    * default: based on sample value
* Will update `~/.config/json-schema-generator/extra.json` to every generated object.

## Example

```json
{
  "account": {
    "name": "",
    "telephone?": "",
    "nationality!?": "CHN",
    "address?": "",
    "city": "",
    "state": "",
    "zip code": "",
    "balance": 100,
    "child": [{
        "name": "",
        "age": 18,
        "gender!": "BOY"
    }],
    "hobby": [],
    "favorite numbers": [3.14]
  }
}

```

And the content of `extra.json`:

```
{
    "title": "example title",
    "description": "example description"
}
```

Will produce:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "account": {
      "type": "object",
      "properties": {
        "name": {
          "type": "string"
        },
        "telephone": {
          "type": "string"
        },
        "nationality": {
          "type": "string",
          "enum": [
            "CHN"
          ]
        },
        "address": {
          "type": "string"
        },
        "city": {
          "type": "string"
        },
        "state": {
          "type": "string"
        },
        "zip code": {
          "type": "string"
        },
        "balance": {
          "type": "integer"
        },
        "child": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "name": {
                "type": "string"
              },
              "age": {
                "type": "integer"
              },
              "gender": {
                "type": "string",
                "enum": [
                  "BOY"
                ]
              }
            },
            "required": [
              "name",
              "age",
              "gender"
            ],
            "additionalProperties": false,
            "title": "example title",
            "description": "example description"
          }
        },
        "hobby": {
          "type": "array"
        },
        "favorite numbers": {
          "type": "array",
          "items": {
            "type": "number"
          }
        }
      },
      "required": [
        "name",
        "city",
        "state",
        "zip code",
        "balance",
        "child",
        "hobby",
        "favorite numbers"
      ],
      "additionalProperties": false,
      "title": "example title",
      "description": "example description"
    }
  },
  "required": [
    "account"
  ],
  "additionalProperties": false,
  "title": "example title",
  "description": "example description"
}
```
