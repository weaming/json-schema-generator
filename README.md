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
    "zip code": "",
    "balance": 100,
    "child": {
        "name": "",
        "age": 18,
        "gender!": "BOY"
    },
    "hobby": [],
    "favorite numbers": [3.14]
  }
}
```

Will produce:

```json
{
  "$schema": "http://json-schema.org/draft-04/schema#",
  "version": 1,
  "additionalProperties": false,
  "required": [
    "account"
  ],
  "type": "object",
  "properties": {
    "account": {
      "title": "Account",
      "required": [
        "hobby",
        "city",
        "name",
        "favorite numbers",
        "zip code",
        "state",
        "child",
        "balance"
      ],
      "properties": {
        "city": {
          "type": "string",
          "id": "city",
          "title": "City"
        },
        "name": {
          "type": "string",
          "id": "name",
          "title": "Name"
        },
        "favorite numbers": {
          "items": {
            "type": "number"
          },
          "type": "array",
          "id": "favorite_numbers",
          "title": "Favorite Numbers"
        },
        "child": {
          "items": {
            "additionalProperties": false,
            "required": [
              "age",
              "gender",
              "name"
            ],
            "type": "object",
            "properties": {
              "gender": {
                "enum": [
                  "BOY"
                ],
                "type": "string",
                "id": "gender",
                "title": "Gender"
              },
              "age": {
                "type": "integer",
                "id": "age",
                "title": "Age"
              },
              "name": {
                "type": "string",
                "id": "name",
                "title": "Name"
              }
            }
          },
          "type": "array",
          "id": "child",
          "title": "Child"
        },
        "zip code": {
          "type": "string",
          "id": "zip_code",
          "title": "Zip Code"
        },
        "telephone": {
          "type": "string",
          "id": "telephone",
          "title": "Telephone"
        },
        "state": {
          "type": "string",
          "id": "state",
          "title": "State"
        },
        "address": {
          "type": "string",
          "id": "address",
          "title": "Address"
        },
        "hobby": {
          "type": "array",
          "id": "hobby",
          "title": "Hobby"
        },
        "balance": {
          "type": "integer",
          "id": "balance",
          "title": "Balance"
        }
      },
      "additionalProperties": false,
      "type": "object",
      "id": "account"
    }
  }
}
```
