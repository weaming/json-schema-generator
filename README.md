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

## Special rules to determine the type

* suffix definitions
    * `?`: optional
    * `!`: `enum`
    * default: based on sample value

## Example

```json
{
  "account": {
    "name": "",
    "telephone?": "",
    "address?": "",
    "city": "",
    "state": "",
    "zip_code": "",
    "balance": 3.14,
    "child": {
        "name": "",
        "age": 13,
        "gender!": "boy"
    }
  }
}
```
Will produce:


```json
{
  "$schema": "http://json-schema.org/draft-04/schema#",
  "version": 1,
  "additionalProperties": false,
  "requried": [
    "account"
  ],
  "type": "object",
  "properties": {
    "account": {
      "additionalProperties": false,
      "requried": [
        "city",
        "name",
        "state",
        "child",
        "balance",
        "zip_code"
      ],
      "type": "object",
      "properties": {
        "city": {
          "type": "string"
        },
        "name": {
          "type": "string"
        },
        "address": {
          "type": "string"
        },
        "telephone": {
          "type": "string"
        },
        "state": {
          "type": "string"
        },
        "child": {
          "additionalProperties": false,
          "requried": [
            "age",
            "gender!",
            "name"
          ],
          "type": "object",
          "properties": {
            "gender": {
              "enum": [],
              "type": "string"
            },
            "age": {
              "type": "integer"
            },
            "name": {
              "type": "string"
            }
          }
        },
        "balance": {
          "type": "number"
        },
        "zip_code": {
          "type": "string"
        }
      }
    }
  }
}
```
