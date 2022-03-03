SHELL := /usr/bin/bash
.DEFAULT_GOAL := help

# AutoDoc
# -------------------------------------------------------------------------
.PHONY: help
help: ## This help. Please refer to the Makefile to more insight about the usage of this script.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)
.DEFAULT_GOAL := help

# Docker
# -------------------------------------------------------------------------

# API
# -------------------------------------------------------------------------
.PHONY: build-docker-api
build-docker-api: ## Build the API Dockerfile. Optional variables BUILDKIT, DOCKER_API_IMAGE and DOCKER_API_TAG
	export BUILDKIT=$(or $(BUILDKIT_ENABLED),1) \
		DOCKER_API_IMAGE=$(or $(DOCKER_API_IMAGE),mairror-api) \
		DOCKER_API_TAG=$(or $(DOCKER_API_TAG),test) && \
	docker build -t $$DOCKER_API_IMAGE:$$DOCKER_API_TAG .
.DEFAULT_GOAL := build-docker-api

.PHONY: lint-docker-api
lint-docker-api: ## Lint the API Dockerfile
	docker run --rm -i -v ${PWD}:/hadolint --workdir=/hadolint hadolint/hadolint < Dockerfile
.DEFAULT_GOAL := lint-docker-api

.PHONY: run-docker-api
run-docker-api: ## Run the API isolated. Optional variables BUILDKIT, DOCKER_API_IMAGE and DOCKER_API_TAG
	export BUILDKIT=$(or $(BUILDKIT_ENABLED),1) \
		DOCKER_API_IMAGE=$(or $(DOCKER_API_IMAGE),mairror-api) \
		DOCKER_API_TAG=$(or $(DOCKER_API_TAG),test) && \
	docker run --rm --name $$DOCKER_API_IMAGE --env-file .env -p 8000:8000 $$DOCKER_API_IMAGE:$$DOCKER_API_TAG
.DEFAULT_GOAL := run-docker-api

# Python
# -------------------------------------------------------------------------

# Cache
# -------------------------------------------------------------------------
.PHONY: clean-pyc
clean-pycache: ## Clean pycache files

	find . -name '__pycache__' -exec rm -rf {} +
.DEFAULT_GOAL := clean-pyc

# Tests
# -------------------------------------------------------------------------
.PHONY: test
test: ## Run all test with pytest
	pytest src/tests
.DEFAULT_GOAL := test
