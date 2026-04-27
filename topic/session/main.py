import argparse
import os
from pathlib import Path
import sys

from dotenv import load_dotenv
from google.adk.cli.fast_api import get_fast_api_app
import uvicorn

BASE_DIR = Path(__file__).resolve().parent
AGENTS_DIR = BASE_DIR / "agent"
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from session_factory import SessionFactory

# Load env from topic/session/.env
load_dotenv(BASE_DIR / ".env")

# Keep compatibility with PROJECT_ID / LOCATION naming in current .env.
if os.getenv("PROJECT_ID") and not os.getenv("GOOGLE_CLOUD_PROJECT"):
    os.environ["GOOGLE_CLOUD_PROJECT"] = os.environ["PROJECT_ID"]
if os.getenv("LOCATION") and not os.getenv("GOOGLE_CLOUD_LOCATION"):
    os.environ["GOOGLE_CLOUD_LOCATION"] = os.environ["LOCATION"]


def build_app():
    session_service_uri = SessionFactory.create_session_service_uri()
    return get_fast_api_app(
        agents_dir=str(AGENTS_DIR),
        session_service_uri=session_service_uri,
        web=False,
    )


fast_api_app = build_app()
# Backward compatibility for existing `uvicorn main:app` usage.
app = fast_api_app


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Session FastAPI entrypoint")
    subparsers = parser.add_subparsers(dest="command")

    run_parser = subparsers.add_parser("run", help="Run FastAPI server")
    run_parser.add_argument("--host", default=os.getenv("HOST", "127.0.0.1"))
    run_parser.add_argument("--port", type=int, default=int(os.getenv("PORT", "8000")))
    run_parser.add_argument("--reload", action="store_true", help="Enable auto-reload")

    args = parser.parse_args()
    if args.command is None:
        args.command = "run"
    return args


def main() -> int:
    args = parse_args()
    if args.command == "run":
        uvicorn.run(
            "main:fast_api_app",
            host=args.host,
            port=args.port,
            reload=args.reload,
        )
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
