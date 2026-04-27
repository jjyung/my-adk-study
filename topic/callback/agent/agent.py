from google.adk.agents.llm_agent import Agent
from google.adk.agents.callback_context import CallbackContext
from google.adk.models import LlmResponse, LlmRequest
from google.genai import types
from typing import Optional

# 範例關鍵字清單 (小寫以便比對)
FORBIDDEN_KEYWORDS = ["secret", "confidential", "forbidden", "password"]

def keyword_guardrail(
    callback_context: CallbackContext, llm_request: LlmRequest
) -> Optional[LlmResponse]:
    """Inspects the LLM request for forbidden keywords and blocks it if found."""
    
    # 提取最後一則 user message
    last_user_message = ""
    if llm_request.contents and llm_request.contents[-1].role == 'user':
        if llm_request.contents[-1].parts:
            # 取得 text，若為 None 則給預設空字串，轉小寫後比對
            part_text = llm_request.contents[-1].parts[0].text
            if part_text:
                last_user_message = part_text.lower()
            
    # 進行關鍵字檢查
    for keyword in FORBIDDEN_KEYWORDS:
        if keyword in last_user_message:
            print(f"[Guardrail] Request blocked. Keyword found: '{keyword}'")
            # 命中關鍵字，回傳 LlmResponse 以阻擋送往模型的請求
            return LlmResponse(
                content=types.Content(
                    role="model",
                    parts=[types.Part(text="Policy Violation: 您的請求包含違規字詞，已被系統阻擋。")],
                )
            )
            
    # 未命中關鍵字，回傳 None 讓流程繼續
    return None

root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='A helpful assistant for user questions.',
    instruction='Answer user questions to the best of your knowledge',
    before_model_callback=keyword_guardrail
)
