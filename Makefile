MAKEFILE_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
LOG_DIR?=$(MAKEFILE_DIR)/logs

.PHONY: clean build test docs

build:
	pip install -e $(MAKEFILE_DIR)/.;
	if [ ! -e $(LOG_DIR) ]; then \
		mkdir $(LOG_DIR); \
	fi; \

clean:
	pip uninstall $(MAKEFILE_DIR)/.;
	rm -rf $(MAKEFILE_DIR)/*.egg-info;
	rm -rf $(MAKEFILE_DIR)/.eggs;
	rm -rf $(MAKEFILE_DIR)/.cache;
	rm -rf $(LOG_DIR);

test: build
	python setup.py test

docs:
	pip install mkdocs; \
	cd documentation;\
	mkdocs build; \
	cd ..;
	@echo 'To view documentation, go to the documentation directory, run "mkdocs serve", and then open "http://127.0.0.1:8000" in a web browser.'
