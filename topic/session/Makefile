SHELL := /bin/bash

UV ?= uv
HOST ?= 127.0.0.1
PORT ?= 8000
AGENT_DIR ?= agent
PY_DEPS := --with google-adk --with python-dotenv --with uvicorn
PY_DEPS := $(PY_DEPS) --with asyncpg

.PHONY: help run dev cli web check k8000

help:
	@echo "Available targets:"
	@echo "  make run   - Run FastAPI app (API mode)"
	@echo "  make dev   - Run FastAPI app with reload (API mode)"
	@echo "  make cli   - Open ADK interactive CLI chat with agent"
	@echo "  make web   - Run ADK web UI in this agent directory"
	@echo "  make check - Verify main/session_factory import and syntax"
	@echo "  make k8000 - Kill process(es) listening on port 8000"

run:
	$(UV) run $(PY_DEPS) python main.py run --host $(HOST) --port $(PORT)

dev:
	HOST=$(HOST) PORT=$(PORT) $(UV) run $(PY_DEPS) python main.py run --host $(HOST) --port $(PORT) --reload

cli:
	@set -a; \
	[ -f .env ] && source .env; \
	set +a; \
	session_uri="$$( $(UV) run $(PY_DEPS) python -c 'from session_factory import SessionFactory; print(SessionFactory.create_session_service_uri())' )"; \
	echo "Using session_service_uri=$$session_uri"; \
	$(UV) run $(PY_DEPS) adk run $(AGENT_DIR) --session_service_uri "$$session_uri"

web:
	$(UV) run $(PY_DEPS) adk web .

check:
	$(UV) run $(PY_DEPS) python -m py_compile main.py session_factory.py agent/agent.py

k8000:
	@pids="$$(lsof -ti tcp:8000 -sTCP:LISTEN 2>/dev/null)"; \
	if [ -z "$$pids" ]; then \
		echo "No process is listening on port 8000"; \
		exit 0; \
	fi; \
	targets="$$pids"; \
	for pid in $$pids; do \
		ppid="$$(ps -o ppid= -p $$pid 2>/dev/null | tr -d ' ')"; \
		if [ -n "$$ppid" ] && [ "$$ppid" -gt 1 ] 2>/dev/null; then \
			targets="$$targets $$ppid"; \
		fi; \
	done; \
	targets="$$(echo "$$targets" | tr ' ' '\n' | awk 'NF' | sort -u | tr '\n' ' ')"; \
	echo "Killing port 8000 process tree: $$targets"; \
	ps -p $$targets -o pid,ppid,command; \
	kill $$targets 2>/dev/null || true; \
	sleep 1; \
	still="$$(lsof -ti tcp:8000 -sTCP:LISTEN 2>/dev/null)"; \
	if [ -n "$$still" ]; then \
		echo "Still listening after SIGTERM, force kill: $$still"; \
		kill -9 $$still; \
	fi; \
	echo "Port 8000 clear."
