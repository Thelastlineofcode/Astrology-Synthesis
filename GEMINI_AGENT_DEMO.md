# Gemini LangChain Agent Demo

This guide shows you how to test the Gemini-powered LangChain agent in the Mula application.

## 🌟 Features

- **Free Tier Available**: Google Gemini offers a generous free tier for testing
- **Fast Response Times**: Gemini 1.5 Flash is optimized for speed
- **High Quality**: 90% quality score with advanced reasoning
- **Tool Calling**: Agent can use astrological tools and knowledge base
- **Conversation Memory**: Maintains context across multiple queries

## 📋 Prerequisites

1. **Python Environment**: Python 3.9+ with pip
2. **Google API Key**: Free API key from Google AI Studio

## 🚀 Quick Start

### Step 1: Get Your Google API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy your API key

### Step 2: Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

This will install:
- `langchain-google-genai==1.0.1` - Google Gemini integration for LangChain
- All other required dependencies

### Step 3: Configure Environment

Add your API key to the `.env` file:

```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your key
GOOGLE_API_KEY=your-actual-api-key-here
GEMINI_MODEL=gemini-1.5-flash
```

### Step 4: Test the Agent

#### Option A: Using the Test Script (Recommended)

```bash
python backend/test_gemini_agent.py
```

This will:
- ✅ Initialize the Gemini agent
- 📝 Run 3 sample astrological queries
- 📊 Display responses and metrics
- 📈 Show cumulative performance data

**Expected Output:**
```
🌟 Gemini LangChain Agent Test Script 🌟
================================================================================

🚀 Initializing Gemini Agent...
================================================================================

✅ Agent initialized: GeminiInterpretationAgent
   Model: gemini-1.5-flash
   Temperature: 0.7
   Max iterations: 5

================================================================================

📝 Test Query 1:
   Query: What does it mean to have Sun in Aries?
   Chart Data: {'sun_sign': 'Aries'}

🤔 Invoking agent...
✅ Response received!

📖 Interpretation:
[Detailed astrological interpretation from Gemini]

📊 Metrics:
   - Model: gemini-1.5-flash
   - Strategy: gemini_agent
   - Tokens: 250
   - Cost: $0.000000
   - Quality Score: 0.9
```

#### Option B: Using the API

1. **Start the FastAPI server:**

```bash
cd backend
uvicorn main:app --reload
```

2. **Check agent health:**

```bash
curl http://localhost:8000/api/v1/gemini-demo/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "message": "Gemini agent is ready",
  "agent_name": "GeminiInterpretationAgent",
  "model": "gemini-1.5-flash",
  "invocations": 0
}
```

3. **Query the agent:**

```bash
curl -X POST http://localhost:8000/api/v1/gemini-demo/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What does Sun in Aries mean?",
    "chart_data": {"sun_sign": "Aries"}
  }'
```

**Expected Response:**
```json
{
  "interpretation": "Having the Sun in Aries means...",
  "model": "gemini-1.5-flash",
  "cost": 0.0,
  "tokens": 200,
  "quality": 0.9,
  "strategy": "gemini_agent",
  "agent_name": "GeminiInterpretationAgent"
}
```

4. **Get agent info:**

```bash
curl http://localhost:8000/api/v1/gemini-demo/info
```

5. **Reset agent (clear memory):**

```bash
curl -X POST http://localhost:8000/api/v1/gemini-demo/reset
```

#### Option C: Using the Interactive API Docs

1. Start the server: `uvicorn main:app --reload`
2. Visit http://localhost:8000/docs
3. Find the "Gemini Demo" section
4. Try the `/api/v1/gemini-demo/query` endpoint

## 📚 Available Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/gemini-demo/query` | POST | Query the agent for interpretations |
| `/api/v1/gemini-demo/info` | GET | Get agent information and metrics |
| `/api/v1/gemini-demo/reset` | POST | Reset agent memory and metrics |
| `/api/v1/gemini-demo/health` | GET | Check agent health and configuration |

## 🧪 Sample Test Queries

```python
# Simple query
{
  "query": "What does Sun in Aries mean?"
}

# Query with chart data
{
  "query": "Interpret my Sun and Moon placement",
  "chart_data": {
    "sun_sign": "Aries",
    "moon_sign": "Taurus"
  }
}

# Nakshatra query
{
  "query": "Tell me about Ashwini nakshatra",
  "chart_data": {
    "nakshatra": "Ashwini"
  }
}

# Compatibility query
{
  "query": "How compatible are Aries and Taurus?",
  "chart_data": {
    "person1": {"sun_sign": "Aries"},
    "person2": {"sun_sign": "Taurus"}
  }
}
```

## 🔧 Configuration Options

You can customize the agent in [backend/agents/factory.py](backend/agents/factory.py):

```python
from backend.agents.factory import create_gemini_agent

agent = create_gemini_agent(
    api_key="your-key",
    model="gemini-1.5-flash",  # or "gemini-1.5-pro"
    temperature=0.7,           # 0.0 = deterministic, 1.0 = creative
    max_iterations=5,          # Max reasoning steps
    verbose=True               # Show detailed logs
)
```

### Available Models

| Model | Speed | Quality | Cost | Use Case |
|-------|-------|---------|------|----------|
| `gemini-1.5-flash` | ⚡ Fast | 90% | Free | **Recommended for demos** |
| `gemini-1.5-pro` | 🐢 Slower | 95% | Free* | High-quality interpretations |

*Subject to rate limits

## 📊 Understanding Agent Responses

The agent returns a structured response:

```json
{
  "interpretation": "The actual astrological interpretation",
  "model": "gemini-1.5-flash",
  "cost": 0.0,              // Free with Gemini
  "tokens": 250,            // Estimated tokens used
  "quality": 0.9,           // Quality score (0-1)
  "strategy": "gemini_agent",
  "agent_name": "GeminiInterpretationAgent"
}
```

## 🐛 Troubleshooting

### Error: "GOOGLE_API_KEY not configured"

**Solution:** Set your API key in `.env`:
```bash
GOOGLE_API_KEY=your-actual-key-here
```

### Error: "Module 'langchain_google_genai' not found"

**Solution:** Install dependencies:
```bash
pip install langchain-google-genai==1.0.1
```

### Error: "API key invalid"

**Solutions:**
1. Verify your API key is correct
2. Check if the key has been enabled (may take a few minutes)
3. Ensure you're not hitting rate limits

### Agent returns errors about tools

**Note:** The current implementation uses stub tools for demonstration. The agent can still provide interpretations without actual tool data.

## 📈 Rate Limits (Free Tier)

Google Gemini free tier limits:
- **Requests per minute:** 60
- **Requests per day:** 1,500
- **Tokens per minute:** 32,000

These limits are very generous for testing and demos!

## 🎯 Next Steps

1. **Integrate into Frontend**: Create a React component to query the agent
2. **Add Real Tools**: Implement actual chart data retrieval tools
3. **Enhance Prompts**: Customize the agent prompt for your use case
4. **Add Streaming**: Enable streaming responses for real-time output
5. **Multi-Agent**: Combine with other agents for complex queries

## 📖 Additional Resources

- [Google Gemini Documentation](https://ai.google.dev/docs)
- [LangChain Google Genai Docs](https://python.langchain.com/docs/integrations/chat/google_generative_ai)
- [Agent Implementation](backend/agents/gemini_agent.py)
- [API Endpoints](backend/api/v1/gemini_demo.py)

## 🤝 Contributing

Found an issue or want to improve the agent? Check out:
- [Backend Agents README](backend/agents/README.md)
- [Factory Functions](backend/agents/factory.py)

---

**Happy Testing! 🎉**
