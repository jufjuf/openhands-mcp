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

4. **Set up credentials (optional):**
   ```bash
   # Copy the template
   cp .env.example .env
   
   # Edit .env with your actual credentials
   nano .env  # or use your preferred editor
   ```

5. **Test the scripts:**
   ```bash
   # Test Python script
   echo '{}' | python3 analyze_audio.py
   
   # Test Node.js script (basic)
   echo '{"url": "https://httpbin.org/json"}' | node call_api.js
   
   # Test Node.js script with auth
   echo '{"url": "https://api.example.com", "auth_type": "bearer"}' | node call_api_with_auth.js
   
   # Test shell script
   ./run_lint.sh
   
   # Test environment loading
   python3 load_env.py
   ```

---

## 🔐 Credentials Management

### Setting up API Keys and Credentials

1. **Copy the environment template:**
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` with your credentials:**
   ```bash
   # Social Media
   FACEBOOK_ACCESS_TOKEN=your_actual_token
   EMAIL_ADDRESS=yufit15@walla.co.il
   EMAIL_PASSWORD=your_email_password
   
   # API Keys
   OPENAI_API_KEY=sk-your_openai_key
   GOOGLE_API_KEY=your_google_key
   ```

3. **Use the password manager:**
   ```bash
   # List all available services
   python3 password_manager.py list
   
   # Show credentials for a service (passwords partially hidden)
   python3 password_manager.py show facebook
   
   # Get specific credentials
   python3 password_manager.py password google
   python3 password_manager.py email zapier
   python3 password_manager.py api twilio
   
   # Get login data as JSON
   python3 auto_login.py facebook
   ```

4. **Use authenticated API calls:**
   ```bash
   # Facebook API with authentication
   echo '{"url": "https://graph.facebook.com/me", "auth_type": "facebook"}' | node call_api_with_auth.js
   
   # Custom API with bearer token
   echo '{"url": "https://api.example.com/data", "auth_type": "bearer"}' | node call_api_with_auth.js
   ```

### Password Management Tools

The project includes built-in password management tools:

- **`password_manager.py`** - Main password manager
  - List all services: `python3 password_manager.py list`
  - Show service info: `python3 password_manager.py show <service>`
  - Get specific credentials: `python3 password_manager.py password <service>`

- **`auto_login.py`** - Auto-login helper
  - Get login data as JSON: `python3 auto_login.py <service>`
  - Perfect for automation scripts

- **`credentials.env`** - Your actual credentials (keep private!)
- **`.env.example`** - Template for sharing

### Security Notes
- ✅ `.env` files are automatically ignored by git
- ✅ Never commit credentials to version control
- ✅ Use environment variables in production
- ✅ Rotate API keys regularly
- ✅ Passwords are partially hidden when displayed
- ✅ Secure credential loading and management

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
