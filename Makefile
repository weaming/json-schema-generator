.PHONY: test build install publish

# the library name
name = json-schema-generator2
# may change to pip3 or python3 -m pip, etc.
pip = pip

test:
	JSON_SCHEMA_ID=1 JSON_SCHEMA_TITLE=1 generate-json-schema test.json

build:
	python setup.py sdist
	python setup.py bdist_wheel --universal

install: clean build
	$(pip) install --force-reinstall ./dist/*.whl

publish: clean build
	twine upload dist/* && git push

uninstall:
	$(pip) uninstall $(name)

clean:
	rm -fr build dist *.egg-info
