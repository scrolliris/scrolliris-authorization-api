ifeq (, $(ENV))
	env := development
else ifeq (test, $(ENV))
	env := testing
else
	env := $(ENV)
endif

app := bern

# -- installation

setup: ## Install dependencies
	pip install -e '.[${env}]' -c constraints.txt
.PHONY: setup

# -- application

serve: ## Start server using waitress
	./serve --env ${env} --config config/${env}.ini --reload
.PHONY: serve

start:  ## Start server on the process by cherrypy via honcho
	honcho -e ${env} start
.PHONY: start

# -- testing/coverage

test: ## Run tests
	ENV=test py.test -c 'config/testing.ini' -q
.PHONY: test

cov: ## Print coverage report in console
	ENV=test py.test -c 'config/testing.ini' -q --cov=${app} \
	  --cov-report term-missing:skip-covered
.PHONY: cov

coverage: ## Generate coverage report as HTML
	ENV=test py.test -c 'config/testing.ini' -q --cov=${app} \
	  --cov-report term-missing \
	  --cov-report html:tmp/coverage
.PHONY: coverage

# -- utility

check: ## Check coding style
	flake8
.PHONY: check

lint: ## Lint
	pylint test ${app}
.PHONY: lint

vet: | check lint ## Run check and lint both
.PHONY: vet

clean: ## Spruce up
	find . ! -readable -prune -o \
	  ! -path "./.git/*" ! -path "./venv*" \
	  ! -path "./doc/*" ! -path "./tool/*" ! -path "./tmp/*" \
	  -print | \
	  grep -E "(__pycache__|\.egg-info|\.pyc|\.pyo)" | \
	  xargs rm -rf
.PHONY: clean

help: ## Display this message
	@grep -E '^[a-zA-Z_.-]+: ## .*$$' $(MAKEFILE_LIST) | \
		sort | \
		awk 'BEGIN {FS = ": ## "}; {printf "\033[36m%-11s\033[0m %s\n", $$1, $$2}'
.PHONY: help

.DEFAULT_GOAL = test
default: test
