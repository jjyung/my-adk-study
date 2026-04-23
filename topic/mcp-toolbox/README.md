# MCP Toolbox Demo (uv + Make)

這個範例示範如何用 `uv` 管理依賴，並透過 `Makefile` 快速操作 ADK + MCP Toolbox。

## 專案結構

```text
topic/mcp-toolbox
├─ .python-version
├─ Makefile
├─ pyproject.toml
├─ README.md
├─ agent/
│  ├─ __init__.py
│  ├─ agent.py
│  └─ .env
└─ mcp/
```

## 先備條件

- 已安裝 `uv`
- 已安裝 `make`
- Python 3.11+
- 已在 `agent/.env` 放入模型金鑰
- 有一個可用的 MCP Toolbox Server（預設 `http://127.0.0.1:5000`）

## 環境變數

`agent/.env` 建議至少包含：

```env
GOOGLE_GENAI_USE_VERTEXAI=0
GOOGLE_API_KEY=YOUR_KEY

# Optional
ADK_MODEL=gemini-2.5-flash
TOOLBOX_SERVER_URL=http://127.0.0.1:5000
TOOLBOX_TOOLSET=demo-toolset
```

## 快速開始

在 `topic/mcp-toolbox` 目錄下：

```bash
make sync
make run
```

啟動 Web UI：

```bash
make web
```

## Make 指令

- `make sync`: 用 `uv` 安裝/同步依賴（含 dev）
- `make lock`: 重新產生 `uv.lock`
- `make run`: 啟動 ADK CLI（`adk run agent`）
- `make web`: 啟動 ADK Web UI（`adk web .`）
- `make lint`: Ruff 檢查
- `make fmt`: Ruff 格式化
- `make fix`: Ruff 自動修正 + 格式化
- `make clean`: 清除 `.venv` 與快取

## Demo 對話建議

- `幫我查詢今天台北天氣，並給我一句穿搭建議。`
- `請先列出你目前可用的工具，再幫我完成需求。`
- `把查詢結果整理成三點摘要。`

## 常見問題

- `ImportError: ToolboxToolset requires the 'toolbox-adk' package`
  - 執行 `make sync`（依賴已透過 `google-adk[toolbox]` 安裝）
- 連不到 Toolbox Server
  - 檢查 `TOOLBOX_SERVER_URL`、port、防火牆與 server 是否已啟動
- 找不到工具名稱
  - 檢查 `TOOLBOX_TOOLSET` 是否與 Toolbox 設定一致

## 參考

- [MCP Toolbox for Databases tool for ADK](https://adk.dev/integrations/mcp-toolbox-for-databases/)
- [mcp-toolbox integrations](https://mcp-toolbox.dev/integrations/)
