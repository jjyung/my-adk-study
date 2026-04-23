SHELL := /bin/bash

.PHONY: help sync lock run web lint fmt fix init-db clean

help:
	@echo "Available targets:"
	@echo "  make sync   - Install/update dependencies via uv"
	@echo "  make lock   - Refresh uv.lock"
	@echo "  make run    - Run ADK CLI agent"
	@echo "  make web    - Run ADK Web UI"
	@echo "  make lint   - Run Ruff checks"
	@echo "  make fmt    - Format code with Ruff"
	@echo "  make fix    - Auto-fix + format"
	@echo "  make init-db - Create sqlite db and users table"
	@echo "  make clean  - Remove local caches"

sync:
	uv sync --all-groups

lock:
	uv lock

run:
	uv run adk run agent

web:
	uv run adk web .

lint:
	uv run ruff check .

fmt:
	uv run ruff format .

fix:
	uv run ruff check --fix .
	uv run ruff format .

init-db:
	sqlite3 db/toolbox.db < db/create_users_table.sql
	sqlite3 db/toolbox.db ".schema users"

clean:
	rm -rf .venv .ruff_cache
