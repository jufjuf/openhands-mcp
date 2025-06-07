# OpenHands MCP Server

This repository contains a simple **Model Context Protocol (MCP)** server to extend the capabilities of [OpenHands](https://github.com/All-Hands-AI/OpenHands). It includes three standalone tools that can be used via MCP to run commands, fetch APIs, and simulate audio analysis.

## 📋 Requirements

- **Python 3.x** (for `analyze_audio.py`)
- **Node.js 18+** (for `call_api.js` - uses built-in fetch API)
- **Bash** (for `run_lint.sh`)

**No external dependencies required** - all scripts use built-in functionality.

---

## 📁 Included Scripts

### `analyze_audio.py` (Python)
Simulates transcription and summarization of an audio file.

**Usage:**
```bash
echo '{}' | python3 analyze_audio.py
```

### `call_api.js` (Node.js)
Fetches JSON data from a specified API URL and returns the response. Includes comprehensive error handling for network issues, HTTP errors, and JSON parsing failures.

**Usage:**
```bash
echo '{"url": "https://api.coindesk.com/v1/bpi/currentprice.json"}' | node call_api.js
```

**Error Handling:**
- Returns structured JSON error messages for debugging
- Handles network connectivity issues
- Validates HTTP response status codes
- Catches JSON parsing errors

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

## 🚀 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/jufjuf/openhands-mcp.git
   cd openhands-mcp
   ```

2. **Make scripts executable:**
   ```bash
   chmod +x run_lint.sh
   ```

3. **Verify Node.js version:**
   ```bash
   node --version  # Should be 18.0.0 or higher
   ```

4. **Test the scripts:**
   ```bash
   # Test Python script
   echo '{}' | python3 analyze_audio.py
   
   # Test Node.js script
   echo '{"url": "https://httpbin.org/json"}' | node call_api.js
   
   # Test shell script
   ./run_lint.sh
   ```

---

## 💡 Examples of Usage in OpenHands

- `Use "call_api" to fetch the current Bitcoin price and summarize it`
- `Run "shell_ops" to check code quality`
- `Transcribe a podcast episode using "analyze_audio"`

---

## 🔧 Troubleshooting

### Common Issues

**Node.js version too old:**
```bash
# Check version
node --version

# If < 18.0.0, update Node.js
# Visit: https://nodejs.org/
```

**Permission denied on run_lint.sh:**
```bash
chmod +x run_lint.sh
```

**call_api.js network errors:**
- The script includes error handling for network issues
- Check your internet connection
- Verify the API URL is accessible
- Error messages are returned in JSON format for debugging

**JSON parsing errors:**
- Ensure input is valid JSON format
- Use double quotes for JSON strings
- Example: `{"url": "https://example.com"}` ✅
- Not: `{url: 'https://example.com'}` ❌

---

## 📄 License

MIT License © You
