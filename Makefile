.DEFAULT_GOAL := help

PRETTIER ?= prettier
PYTHON   ?= python3
MD       := "**/*.md"

.PHONY: help
help: ## Show available targets
	@grep -E '^[a-zA-Z_-]+:.*## ' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*## "}; {printf "  %-12s %s\n", $$1, $$2}'

.PHONY: fmt
fmt: ## Format all Markdown with Prettier
	$(PRETTIER) --write $(MD)

.PHONY: fmt-check
fmt-check: ## Check Markdown formatting without writing
	$(PRETTIER) --check $(MD)

.PHONY: audit
audit: ## Run the docmap documentation audit
	$(PYTHON) skills/docmap/scripts/docmap.py audit --root ./

.PHONY: test
test: ## Run the docmap script tests
	cd skills/docmap/scripts && $(PYTHON) test_docmap.py

.PHONY: check
check: fmt-check audit test ## Run all verifications
