tests_dir = tests
documentation_dir = docs
package_dir = watch_do

docker_image = watch-do-build-environment

# Define the base command to run another command inside our build environment
define docker_run
	docker run \
	--rm \
	--volume=$(PWD):/watch-do \
	--name $(docker_image)-$(shell hexdump -n 5 -e '"%02x"' /dev/urandom) \
	$(2) \
	$(docker_image) \
	$(1)
endef

.PHONY: all
all: test lint docs

.PHONY: build-environment
build-environment:
	@echo "Building environment"
	@docker build --tag $(docker_image) .

.PHONY: run-build-environment
run-build-environment: build-environment
	@echo "Running build environment"
	@$(call docker_run, /bin/sh, -it)

.PHONY: docs
docs: build-environment
	@echo "Building documentation"
	@$(call docker_run, $(MAKE) -C $(documentation_dir) html)

.PHONY: test
test: build-environment
	@echo "Running tests"
	@$(call docker_run, \
		python3 \
			-m unittest discover \
			--start-directory $(tests_dir) \
			--pattern '*.py')

.PHONY: lint
lint: lint-package lint-tests

.PHONY: lint-package
lint-package: build-environment
	@echo "Linting the package code"
	@$(call docker_run, \
		pylint \
			--reports no \
			$(package_dir) setup.py)

.PHONY: lint-tests
lint-tests: build-environment
	@echo "Linting the test code"
	@$(call, docker_run, \
		pylint \
			--reports no \
			--disable protected-access \
			$(tests_dir))
