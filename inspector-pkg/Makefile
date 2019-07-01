
clean:
	rm -rf build
	rm -rf dist
	rm -rf src/*.egg-info
	rm -rf .eggs

test:
	python3 setup.py test

install:
	pip3 install --user .

ciinstall:
	pip3 install .

uninstall:
	pip3 uninstall -y shminspector

release:
	python3 -m pip install --user --upgrade setuptools wheel
	python3 setup.py sdist bdist_wheel
	python3 -m pip install --user --upgrade twine
	python3 -m twine upload --verbose dist/*
