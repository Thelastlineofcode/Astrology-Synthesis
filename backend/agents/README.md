# LangChain Agents for Astrological Interpretations

A sophisticated multi-agent system for generating astrological interpretations using LangChain's agent framework.

## Architecture

```
HybridOrchestratorAgent
├── PerplexityInterpretationAgent (LLM-powered, $0.0001/call)
├── InterpretationAgent (Template-based, $0)
└── KnowledgeBaseAgent (Vector search, $0)
```

## Agents

### 1. **PerplexityInterpretationAgent**
- **Model**: Perplexity sonar-small
- **Cost**: ~$0.0001 per interpretation
- **Quality**: 85%+
- **Features**:
  - ReAct-style reasoning
  - Tool calling for chart data
  - Conversation memory
  - Budget tracking

### 2. **InterpretationAgent**
- **Model**: Templates + Knowledge Base
- **Cost**: $0
- **Quality**: 70%+
- **Features**:
  - Instant responses
  - Template library
  - KB integration
  - Zero-cost operation

### 3. **HybridOrchestratorAgent**
- **Purpose**: Intelligent strategy selection
- **Features**:
  - Multi-agent coordination
  - Budget-aware routing
  - Quality optimization
  - Automatic fallbacks

## Tools

Agents have access to specialized tools:

- `get_chart_data`: Retrieve birth chart information
- `get_nakshatra_info`: Get Vedic nakshatra details
- `get_planetary_info`: Planet-sign-house interpretations
- `search_knowledge_base`: Vector search in KB

## Usage

### Basic Usage

```python
from backend.agents import create_orchestrator_agent

# Create orchestrator with all sub-agents
orchestrator = create_orchestrator_agent(
    perplexity_api_key="your-api-key",
    monthly_budget=5.0,
    verbose=True,
)

# Generate interpretation
result = orchestrator.invoke({
    "query": "What does my Sun in Aries mean?",
    "chart_data": {
        "sun_sign": "Aries",
        "moon_sign": "Taurus",
        "ascendant": "Gemini",
    },
    "strategy": "auto",  # Let orchestrator decide
})

print(result["interpretation"])
print(f"Cost: ${result['cost']:.6f}")
print(f"Strategy used: {result['strategy']}")
```

### Using Specific Agents

```python
from backend.agents import create_perplexity_agent, create_interpretation_agent

# Use only Perplexity agent
perplexity = create_perplexity_agent(
    api_key="your-key",
    temperature=0.7,
)

result = perplexity.invoke({
    "query": "Interpret my natal chart",
    "chart_data": {...},
})

# Use only template agent (free)
template_agent = create_interpretation_agent()

result = template_agent.invoke({
    "type": "sun_sign",
    "chart_data": {"sun_sign": "Leo"},
})
```

### Strategy Selection

The orchestrator automatically selects the best strategy:

```python
# Auto mode (recommended)
result = orchestrator.invoke({
    "query": "Complex multi-planet analysis",
    "strategy": "auto",  # Orchestrator decides
})

# Force specific strategy
result = orchestrator.invoke({
    "query": "Simple sun sign interpretation",
    "strategy": "template",  # Force template use
})

# Available strategies: "auto", "llm", "kb", "template"
```

## Configuration

### Environment Variables

```bash
# Perplexity API
PERPLEXITY_API_KEY=your_key_here
MONTHLY_BUDGET=5.0

# Strategy
DEFAULT_STRATEGY=auto

# Logging
LOG_LEVEL=INFO
VERBOSE=false
```

### Agent Configuration

```python
# Create with custom config
orchestrator = create_orchestrator_agent(
    perplexity_api_key="key",
    monthly_budget=10.0,          # $10/month
    default_strategy="auto",      # auto, llm, kb, template
    verbose=True,                 # Enable detailed logging
)
```

## Metrics & Monitoring

### Get Agent Metrics

```python
# Per-agent metrics
metrics = perplexity.get_metrics()
print(f"Invocations: {metrics['invocations']}")
print(f"Total cost: ${metrics['total_cost']:.4f}")
print(f"Avg tokens: {metrics['avg_tokens_per_call']}")

# Orchestrator statistics
stats = orchestrator.get_stats()
print(f"Total requests: {stats['total_requests']}")
print(f"Strategy breakdown: {stats['strategy_percentages']}")
```

### Budget Tracking

```python
# Check budget
budget = perplexity.get_budget_info()
print(f"Used: ${budget['used']:.4f}")
print(f"Remaining: ${budget['remaining']:.4f}")
print(f"Percentage: {budget['percentage_used']:.1f}%")

# Reset monthly
perplexity.reset_metrics()
```

## Advanced Features

### Conversation Memory

```python
# Agents maintain conversation history
result1 = orchestrator.invoke({"query": "What's my sun sign?"})
result2 = orchestrator.invoke({"query": "Tell me more about it"})
# Agent remembers context

# Get history
history = orchestrator.get_history(last_n=5)

# Clear history
orchestrator.clear_history()
```

### Custom Tools

```python
from langchain.tools import Tool

# Add custom tool
def my_custom_tool(input: str) -> str:
    return f"Custom result for: {input}"

custom_tool = Tool(
    name="my_tool",
    func=my_custom_tool,
    description="My custom astrological tool",
)

# Add to agent
perplexity.tools.append(custom_tool)
```

### Custom Templates

```python
# Add custom interpretation template
template_agent.add_template(
    template_id="custom_venus",
    template_text="Your Venus in {sign} shows {detailed_interpretation}",
)
```

## Performance

### Benchmarks

| Strategy | Speed | Cost | Quality | When to Use |
|----------|-------|------|---------|-------------|
| LLM | ~2s | $0.0001 | 85% | Complex queries |
| KB | ~100ms | $0 | 80% | Standard queries |
| Template | <10ms | $0 | 70% | Simple queries |

### Cost Optimization

```python
# Monthly budget example
# 50,000 interpretations/month @ $0.0001 = $5/month

# Strategy mix for 1000 interpretations:
# - 100 LLM (complex) = $0.01
# - 400 KB (standard) = $0
# - 500 Template (simple) = $0
# Total cost = $0.01 for 1000 interpretations
```

## Error Handling

```python
result = orchestrator.invoke({"query": "..."})

if "error" in result:
    print(f"Error: {result['error']}")
    print(f"Strategy: {result['strategy']}")
    # Orchestrator auto-falls back to next strategy
else:
    print(result["interpretation"])
```

## Testing

```python
# Test with mock data
from backend.agents.factory import create_default_orchestrator

orchestrator = create_default_orchestrator(verbose=True)

test_input = {
    "query": "Test interpretation",
    "chart_data": {
        "sun_sign": "Aries",
        "moon_sign": "Taurus",
    },
}

result = orchestrator.invoke(test_input)
assert "interpretation" in result
assert result["cost"] >= 0
```

## Migration Guide

### From Old Services to Agents

```python
# OLD: Direct Perplexity service
from backend.services.perplexity_llm_service import PerplexityLLMService
old_service = PerplexityLLMService(api_key="...")
result = old_service.generate_interpretation(...)

# NEW: LangChain agent
from backend.agents import create_perplexity_agent
new_agent = create_perplexity_agent(api_key="...")
result = new_agent.invoke({"query": "...", "chart_data": {...}})
```

Benefits of migration:
- ✅ Tool calling & multi-step reasoning
- ✅ Conversation memory
- ✅ Better error handling & fallbacks
- ✅ Metrics & observability
- ✅ LangSmith integration for debugging

## Troubleshooting

### Common Issues

**1. API Key Not Found**
```python
# Set in environment
export PERPLEXITY_API_KEY=your_key

# Or pass directly
agent = create_perplexity_agent(api_key="your_key")
```

**2. Budget Exhausted**
```python
# Check budget
budget = agent.get_budget_info()
if budget["remaining"] <= 0:
    # Use template fallback
    result = template_agent.invoke(...)
```

**3. Tool Errors**
```python
# Enable verbose mode to see tool calls
orchestrator = create_orchestrator_agent(verbose=True)
```

## Contributing

To add new agents:

1. Inherit from `BaseInterpretationAgent`
2. Implement `invoke()` and `get_tools()`
3. Add to factory.py
4. Update __init__.py

Example:
```python
from .base_agent import BaseInterpretationAgent

class MyCustomAgent(BaseInterpretationAgent):
    def __init__(self, **kwargs):
        super().__init__(
            agent_name="MyCustomAgent",
            description="Does something cool",
        )

    def invoke(self, input_data):
        # Your logic here
        pass

    def get_tools(self):
        return []
```

## License

Part of the Mula astrological calculation engine.
