include .env
EXPORT = export PYTHONPATH=$(PWD)

checks:
	$(EXPORT) && pipenv run sh scripts/checks.sh

install:
	$(EXPORT) && pipenv install --dev

sync:
	$(EXPORT) && pipenv sync --dev

clean:
	$(EXPORT) && pipenv clean