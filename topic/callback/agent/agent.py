from google.adk.agents.llm_agent import Agent
from google.adk.agents.callback_context import CallbackContext
from google.adk.models import LlmResponse, LlmRequest
from google.adk.tools import FunctionTool, BaseTool, ToolContext
from google.genai import types
from typing import Optional, Dict, Any
from datetime import datetime

# 範例關鍵字清單 (小寫以便比對)
FORBIDDEN_KEYWORDS = ["secret", "confidential", "forbidden", "password"]

# ===== [Pattern 1: Dynamic State Management] =====
def manage_user_state(callback_context: CallbackContext) -> Optional[types.Content]:
    """獲取使用者資訊並寫入 Session State"""
    print("[State Management] Loading user info into state...")
    
    # 硬編碼寫入狀態，ADK Python 的 state 可以當字典使用
    callback_context.state["user_name"] = "samson"
    
    return None

# ===== [Pattern 2: Guardrails & Context Injector] =====
def keyword_guardrail_and_context_injector(
    callback_context: CallbackContext, llm_request: LlmRequest
) -> Optional[LlmResponse]:
    """Inspects the LLM request for forbidden keywords and injects user context."""
    
    # === [Phase 1: Guardrail 檢查] ===
    last_user_message = ""
    if llm_request.contents and llm_request.contents[-1].role == 'user':
        if llm_request.contents[-1].parts:
            part_text = llm_request.contents[-1].parts[0].text
            if part_text:
                last_user_message = part_text.lower()
            
    # 進行關鍵字檢查
    for keyword in FORBIDDEN_KEYWORDS:
        if keyword in last_user_message:
            print(f"[Guardrail] Request blocked. Keyword found: '{keyword}'")
            return LlmResponse(
                content=types.Content(
                    role="model",
                    parts=[types.Part(text="Policy Violation: 您的請求包含違規字詞，已被系統阻擋。")],
                )
            )
            
    # === [Phase 2: 動態優化回應 (Context Injection)] ===
    # 讀取在 before_agent_callback 寫入的狀態
    user_name = callback_context.state.get("user_name")
    
    if user_name:
        # 初始化 system_instruction (若無則建立)
        original_instruction = llm_request.config.system_instruction or types.Content(role="system", parts=[])
        if not isinstance(original_instruction, types.Content):
            original_instruction = types.Content(role="system", parts=[types.Part(text=str(original_instruction))])
        if not original_instruction.parts:
            original_instruction.parts.append(types.Part(text=""))
            
        # 加上提示詞，優化回應
        prefix = f"[系統提示：當前使用者的名字是 {user_name}，請在回覆時親切地稱呼他的名字。]\n"
        modified_text = prefix + (original_instruction.parts[0].text or "")
        original_instruction.parts[0].text = modified_text
        
        # 覆寫回 request
        llm_request.config.system_instruction = original_instruction
        print(f"[Context Injector] System instruction updated for user: {user_name}")

    return None

# ===== [Pattern 3: Logging and Monitoring (Tool)] =====
def get_current_time() -> str:
    """Get the current system date and time. Use this when the user asks for the current time."""
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

# 在 Python 版 ADK 中，FunctionTool 直接傳入 callable 即可，不使用 name 與 description 參數（會自動從函式 docstring 抓取）
get_current_time_tool = FunctionTool(get_current_time)

def tool_logger(
    tool: BaseTool, args: Dict[str, Any], tool_context: ToolContext, tool_response: Dict
) -> Optional[Dict]:
    """Logs the execution details of any tool called by the agent."""
    agent_name = tool_context.agent_name
    tool_name = tool.name
    print(f"\n[Tool Logger] Agent '{agent_name}' finished executing tool: '{tool_name}'")
    print(f"[Tool Logger] Arguments used: {args}")
    print(f"[Tool Logger] Tool Response: {tool_response}\n")
    
    # 回傳 None 表示不修改原始的 response
    return None

# ===== [Agent Definition] =====
root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='A helpful assistant for user questions.',
    instruction='Answer user questions to the best of your knowledge',
    before_agent_callback=manage_user_state,
    before_model_callback=keyword_guardrail_and_context_injector,
    tools=[get_current_time_tool],
    after_tool_callback=tool_logger
)
