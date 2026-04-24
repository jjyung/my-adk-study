import os
from google.adk.sessions import BaseSessionService, InMemorySessionService

class SessionFactory:
    """Factory to create the appropriate SessionService based on mode."""

    @staticmethod
    def create(mode: str | None = None) -> BaseSessionService:
        """
        Creates a SessionService using google.adk built-in services.
        If mode is not provided, it falls back to the SESSION_MODE env variable,
        and defaults to 'in_memory' if not set.
        """
        mode = mode or os.getenv("SESSION_MODE", "in_memory").lower()

        if mode == "in_memory":
            return InMemorySessionService()
            
        elif mode == "vertex_ai":
            from google.adk.sessions.vertex_ai_session_service import VertexAiSessionService
            project_id = os.getenv("PROJECT_ID")
            location = os.getenv("LOCATION")
            if not project_id or not location:
                raise ValueError("PROJECT_ID and LOCATION must be set in .env for vertex_ai mode.")
            return VertexAiSessionService(project=project_id, location=location)
            
        elif mode == "database":
            from google.adk.sessions.database_session_service import DatabaseSessionService
            db_url = os.getenv("DB_URL")
            if not db_url:
                raise ValueError("DB_URL must be set in .env for database mode.")
            return DatabaseSessionService(db_url=db_url)
            
        else:
            raise ValueError(f"Unknown session mode: {mode}")
