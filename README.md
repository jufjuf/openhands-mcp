# OpenHands MCP Server

This repository contains a simple **Model Context Protocol (MCP)** server to extend the capabilities of [OpenHands](https://github.com/All-Hands-AI/OpenHands). It includes three standalone tools that can be used via MCP to run commands, fetch APIs, and simulate audio analysis.

---

## 📁 Included Scripts

### `analyze_audio.py` (Python)
Simulates transcription and summarization of an audio file.

**Usage:**
```bash
echo '{}' | python3 analyze_audio.py
```

### `call_api.js` (Node.js)
Fetches JSON data from a specified API URL and returns the response.

**Usage:**
```bash
echo '{"url": "https://api.coindesk.com/v1/bpi/currentprice.json"}' | node call_api.js
```

### `run_lint.sh` (Shell)
Simulates running a lint check on a codebase.

**Usage:**
```bash
./run_lint.sh
```

---

## 🔧 MCP Configuration (OpenHands)

Use the following configuration under `Settings → MCP` in OpenHands:

```json
{
  "stdio_servers": [
    {
      "name": "analyze_audio",
      "command": "python3",
      "args": ["analyze_audio.py"]
    },
    {
      "name": "call_api",
      "command": "node",
      "args": ["call_api.js"]
    },
    {
      "name": "shell_ops",
      "command": "bash",
      "args": ["run_lint.sh"]
    }
  ],
  "sse_servers": []
}
```

---

## 💡 Examples of Usage in OpenHands

- `Use "call_api" to fetch the current Bitcoin price and summarize it`
- `Run "shell_ops" to check code quality`
- `Transcribe a podcast episode using "analyze_audio"`

---

## 📄 License

MIT License © You
