tests_dir = tests
documentation_dir = docs
package_dir = watch_do

.PHONY: docs
docs:
	@echo "Building documentation"
	@$(MAKE) -C $(documentation_dir) html

.PHONY: test
test:
	@echo "Running tests"
	@python3 -m unittest discover \
		--start-directory $(tests_dir) \
		--pattern '*.py'

.PHONY: lint
lint: lint-package lint-tests

.PHONY: lint-package
lint-package:
	@echo "Linting the package code"
	@pylint \
		$(package_dir) \
		setup.py

.PHONY: lint-tests
lint-tests:
	@echo "Linting the test code"
	@pylint \
		--disable protected-access \
		$(tests_dir)
