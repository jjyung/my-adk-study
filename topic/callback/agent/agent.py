from google.adk.agents.llm_agent import Agent
from google.adk.agents.callback_context import CallbackContext
from google.adk.models import LlmResponse, LlmRequest
from google.adk.tools import FunctionTool, BaseTool, ToolContext
from google.genai import types
from typing import Optional, Dict, Any
from datetime import datetime
import random

# 範例關鍵字清單 (小寫以便比對)
FORBIDDEN_KEYWORDS = ["secret", "confidential", "forbidden", "password"]

# ===== [Pattern 1: Dynamic State Management] =====
def manage_user_state(callback_context: CallbackContext) -> Optional[types.Content]:
    """獲取使用者資訊並寫入 Session State"""
    print("[State Management] Loading user info into state...")
    callback_context.state["user_name"] = "samson"
    return None

# ===== [Pattern 2: Guardrails & Context Injector] =====
def keyword_guardrail_and_context_injector(
    callback_context: CallbackContext, llm_request: LlmRequest
) -> Optional[LlmResponse]:
    """Inspects the LLM request for forbidden keywords and injects user context."""
    
    # Phase 1: Guardrail
    last_user_message = ""
    if llm_request.contents and llm_request.contents[-1].role == 'user':
        if llm_request.contents[-1].parts:
            part_text = llm_request.contents[-1].parts[0].text
            if part_text:
                last_user_message = part_text.lower()
            
    for keyword in FORBIDDEN_KEYWORDS:
        if keyword in last_user_message:
            print(f"[Guardrail] Request blocked. Keyword found: '{keyword}'")
            return LlmResponse(
                content=types.Content(
                    role="model",
                    parts=[types.Part(text="Policy Violation: 您的請求包含違規字詞，已被系統阻擋。")],
                )
            )
            
    # Phase 2: Context Injection
    user_name = callback_context.state.get("user_name")
    if user_name:
        original_instruction = llm_request.config.system_instruction or types.Content(role="system", parts=[])
        if not isinstance(original_instruction, types.Content):
            original_instruction = types.Content(role="system", parts=[types.Part(text=str(original_instruction))])
        if not original_instruction.parts:
            original_instruction.parts.append(types.Part(text=""))
            
        prefix = f"[系統提示：當前使用者的名字是 {user_name}，請在回覆時親切地稱呼他的名字。]\n"
        modified_text = prefix + (original_instruction.parts[0].text or "")
        original_instruction.parts[0].text = modified_text
        llm_request.config.system_instruction = original_instruction

    return None

# ===== [Tools Definition] =====
def get_current_time() -> str:
    """Get the current system date and time. Use this when the user asks for the current time."""
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

def get_stock_price(symbol: str) -> str:
    """Get the current stock price for a given ticker symbol. Use this when the user asks for a stock price."""
    # 模擬 API 呼叫，隨機回傳萬元以下的數字
    price = random.randint(100, 10000)
    print(f"[Tool Execution] Fetching fresh stock price for {symbol}: {price}")
    return str(price)

get_current_time_tool = FunctionTool(get_current_time)
get_stock_price_tool = FunctionTool(get_stock_price)

# ===== [Pattern 3: Caching & Logging (Tool Callbacks)] =====

# 獨立方法：Caching (Before)
def cache_before_tool(
    tool: BaseTool, args: Dict[str, Any], tool_context: ToolContext
) -> Optional[Dict]:
    """Check state for cached stock price before executing the tool."""
    if tool.name == "get_stock_price":
        symbol = args.get("symbol", "").upper()
        cache_key = f"cache:stock:{symbol}"
        cached_price = tool_context.state.get(cache_key)
        
        if cached_price is not None:
            print(f"[Cache Hit] Found cached price for {symbol}: {cached_price}")
            # 回傳字典，攔截工具執行
            return {"result": cached_price}
            
    return None

# 獨立方法：Caching (After)
def cache_after_tool(
    tool: BaseTool, args: Dict[str, Any], tool_context: ToolContext, tool_response: Any
):
    """Save the fresh stock price to state after executing the tool."""
    if tool.name == "get_stock_price":
        symbol = args.get("symbol", "").upper()
        cache_key = f"cache:stock:{symbol}"
        
        # 根據實際傳入的 tool_response 型別安全取值
        result_value = None
        if isinstance(tool_response, dict):
            result_value = tool_response.get("result")
        else:
            result_value = tool_response

        if result_value is not None:
            # 將結果寫入 session state，供下次呼叫使用
            tool_context.state[cache_key] = result_value
            print(f"[Cache Set] Saved fresh price for {symbol} to state.")

# 獨立方法：Logger
def tool_logger(
    tool: BaseTool, args: Dict[str, Any], tool_context: ToolContext, tool_response: Any
):
    """Logs the execution details of any tool called by the agent."""
    agent_name = tool_context.agent_name
    tool_name = tool.name
    print(f"\n[Tool Logger] Agent '{agent_name}' finished executing tool: '{tool_name}'")
    print(f"[Tool Logger] Arguments used: {args}")
    print(f"[Tool Logger] Tool Response: {tool_response}\n")

# Chain Dispatchers (組裝多個 callback)
def composite_before_tool(
    tool: BaseTool, args: Dict[str, Any], tool_context: ToolContext
) -> Optional[Dict]:
    # 1. 執行 Caching 邏輯
    cache_result = cache_before_tool(tool, args, tool_context)
    if cache_result is not None:
        return cache_result # 命中快取，中斷後續與工具執行
    
    return None

def composite_after_tool(
    tool: BaseTool, args: Dict[str, Any], tool_context: ToolContext, tool_response: Any
) -> Optional[Dict]:
    # 1. 執行 Caching 寫入
    cache_after_tool(tool, args, tool_context, tool_response)
    
    # 2. 執行 Logging
    tool_logger(tool, args, tool_context, tool_response)
    
    # 回傳 None 表示不竄改原始回傳給 LLM 的結果
    return None

# ===== [Agent Definition] =====
root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='A helpful assistant for user questions.',
    instruction='Answer user questions to the best of your knowledge',
    before_agent_callback=manage_user_state,
    before_model_callback=keyword_guardrail_and_context_injector,
    tools=[get_current_time_tool, get_stock_price_tool],
    before_tool_callback=composite_before_tool,
    after_tool_callback=composite_after_tool
)
