PYTHON_VERSION = 2.7

virtualenv:
	test -d .env || virtualenv -p python$(PYTHON_VERSION) .env

develop: virtualenv
	.env/bin/pip install --upgrade setuptools
	.env/bin/pip install wheel
	.env/bin/pip install twine
	.env/bin/pip install -r requirements-test.pip

test:
	.env/bin/python setup.py test

coverage:
	.env/bin/coverage run setup.py test
	.env/bin/coverage report

flake8:
	.env/bin/flake8 nygma --max-complexity=15

dist:
	.env/bin/python setup.py sdist
	.env/bin/python setup.py bdist_wheel --universal

upload:
	.env/bin/twine upload dist/*

release: dist upload
