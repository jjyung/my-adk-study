# ADK Callbacks Pattern Implementation

這個專案展示了如何利用 Google Agent Development Kit (ADK) 提供的各式 Callbacks 來實現強大且靈活的代理 (Agent) 設計模式。透過 `agent/agent.py`，我們實作了多種常見的企業級模式，所有模式皆遵循切面導向設計 (AOP) 的精神。

## 實作的設計模式 (Patterns)

### 1. Dynamic State Management (動態狀態管理)

* **Callback:** `before_agent_callback`
* **說明:** 在 Agent 開始任何工作之前，攔截呼叫並進行環境的初始化。
* **實作內容:** `manage_user_state` 會在呼叫前，將硬編碼的使用者資訊（例如 `user_name = "samson"`）注入到 `callback_context.state` 中。這保證了在後續的流程中，模型與工具都能存取到最新的使用者上下文。

### 2. Guardrails & Context Injector (安全防護與提示詞注入)

* **Callback:** `before_model_callback`
* **說明:** 在送出請求給底層的大語言模型 (LLM) 之前觸發，是確保安全性與優化 Prompt 的最佳時機。
* **實作內容:**
  * **Guardrail:** 檢查使用者最新的訊息中是否包含定義在 `FORBIDDEN_KEYWORDS` 的違規字詞。若命中，則回傳自定義的 `LlmResponse` 來**中斷** LLM 的呼叫，直接回覆拒絕訊息。
  * **Context Injection:** 若未違規，程式會讀取先前寫入 `state` 中的 `user_name`，並將其動態注入到傳送給模型的 `system_instruction` 中，指示模型親切地稱呼使用者。

### 3. Tool Caching (工具快取機制)

* **Callback:** `before_tool_callback` & `after_tool_callback`
* **說明:** 針對耗時或需要控制 API 成本的工具，在執行前後建立快取機制。支援跨節點的分散式部署（依賴 ADK 底層 Session State）。
* **實作內容:**
  * `get_stock_price` 工具負責查詢股價。
  * **Before:** `cache_before_tool` 檢查 `tool_context.state` 中是否存在 `cache:stock:{symbol}`。若存在，則回傳 `{"result": cached_price}`，這會阻擋工具真實執行，直接使用快取。
  * **After:** `cache_after_tool` 會在工具實際執行完畢後，把新的股價存回 state，供未來的請求使用。

### 4. Logging and Monitoring (日誌與監控)

* **Callback:** `after_tool_callback`
* **說明:** 統一監控與紀錄所有工具的執行細節。
* **實作內容:**
  * `tool_logger` 獨立函式負責在工具執行後印出 `tool.name`、傳入的 `args` 與輸出的 `tool_response`。
  * 透過 `composite_after_tool` 的 Dispatcher Wrapper 模式，將 Logging 邏輯與 Caching 邏輯以 Chain Calling 的方式無縫整合。

## 程式碼結構

主要實作均位於 `agent/agent.py` 內：

* `manage_user_state`
* `keyword_guardrail_and_context_injector`
* `get_current_time` (Time Function Tool)
* `get_stock_price` (Stock Function Tool)
* `cache_before_tool` & `cache_after_tool` (Caching Logic)
* `tool_logger` (Monitoring Logic)
* `composite_before_tool` & `composite_after_tool` (Callback Chain Dispatchers)
* `root_agent` (整合所有 Callbacks 與 Tools 的 LlmAgent)

## 執行與測試

本專案實作的 Agent 已封裝完畢。可配合 ADK 的 `Runner` (例如 `InMemoryRunner`) 載入 `root_agent`，並進行以下測試腳本驗證：

1. 詢問包含 "secret" 的敏感字詞，測試 Guardrail。
2. 觀察回應是否會稱呼您為 "samson"，測試 Context Injection。
3. 詢問 "AAPL 的股價"，觀察 Console 上的 Logger。
4. 再次詢問 "AAPL 的股價"，觀察是否觸發 Cache Hit。
