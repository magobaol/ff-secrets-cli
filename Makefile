# install: build a single-file executable with zipapp and place it on PATH.
# Pure stdlib, so the whole package collapses into one self-contained .pyz (named
# ff-secrets) with a python3 shebang — a real single file in ~/.local/bin, no opt subtree.
PREFIX ?= $(HOME)/.local
BINDIR := $(PREFIX)/bin
BUILD  := build

.PHONY: install
install:
	rm -rf "$(BUILD)"
	mkdir -p "$(BUILD)" "$(BINDIR)"
	cp -R ff_secrets_cli "$(BUILD)/"
	rm -rf "$(BUILD)/ff_secrets_cli/__pycache__"
	rm -f "$(BINDIR)/ff-secrets"
	python3 -m zipapp "$(BUILD)" -p '/usr/bin/env python3' -m 'ff_secrets_cli.cli:main' -o "$(BINDIR)/ff-secrets"
	chmod 0755 "$(BINDIR)/ff-secrets"
	rm -rf "$(BUILD)"
	@echo "installed: $(BINDIR)/ff-secrets (zipapp single file)"
