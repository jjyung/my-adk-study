import asyncio
import os
from dotenv import load_dotenv

from session_factory import SessionFactory

async def test_factory():
    print("--- Testing InMemory ---")
    os.environ["SESSION_MODE"] = "in_memory"
    service1 = SessionFactory.create()
    session1 = await service1.create_session(app_name="test_app", user_id="user_123")
    print("Created InMemory Session ID:", session1.id)
    retrieved1 = await service1.get_session(app_name="test_app", user_id="user_123", session_id=session1.id)
    print("Get user_123 session:", retrieved1.id if retrieved1 else None)

    print("\n--- Testing Database ---")
    os.environ["SESSION_MODE"] = "database"
    service2 = SessionFactory.create()
    session2 = await service2.create_session(app_name="test_app", user_id="user_456")
    print("Created Database Session ID:", session2.id)
    retrieved2 = await service2.get_session(app_name="test_app", user_id="user_456", session_id=session2.id)
    print("Get user_456 session:", retrieved2.id if retrieved2 else None)

    print("\n--- Testing Vertex AI ---")
    os.environ["SESSION_MODE"] = "vertex_ai"
    try:
        service3 = SessionFactory.create()
        print("VertexAiSessionService successfully created.")
    except Exception as e:
        # Catch exceptions if environment isn't fully set up for GCP auth
        print(f"VertexAiSessionService initialization error: {e}")

if __name__ == "__main__":
    # Load .env variables initially
    load_dotenv()
    asyncio.run(test_factory())
