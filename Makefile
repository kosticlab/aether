MAKEFILE_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
LOG_DIR?=$(MAKEFILE_DIR)/logs

.PHONY: clean build test docs build-noconda

build:
	conda install -y pip
	conda install -y numpy
	conda install -y scipy
	conda install -c conda-forge jq=1.5
	pip install --upgrade --user awscli
	pip install -q azure-cli
	conda install -y -c bioconda azure-cli
	conda install -y -c ibmdecisionoptimization cplex
	conda install -y -c ibmdecisionoptimization docplex
	make build-noconda

build-noconda:
	pip install --editable $(MAKEFILE_DIR)/.;
	if [ ! -e $(LOG_DIR) ]; then \
		mkdir $(LOG_DIR); \
	fi;

clean:
	pip uninstall $(MAKEFILE_DIR)/.;
	rm -rf $(MAKEFILE_DIR)/*.egg-info;
	rm -rf $(MAKEFILE_DIR)/.eggs;
	rm -rf $(MAKEFILE_DIR)/.cache;
	rm -rf $(LOG_DIR);

test: build-noconda
	python setup.py test

docs:
	pip install mkdocs; \
	cd documentation;\
	mkdocs build --clean; \
	cd ..;
	@echo 'To view documentation, go to the documentation directory, run "mkdocs serve", and then open "http://127.0.0.1:8000" in a web browser.'
