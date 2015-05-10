

test:
	flake8 --select=F .
	python -m unittest discover
	flake8 .
