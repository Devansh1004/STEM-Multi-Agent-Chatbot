# STEM Multi-Agent Chatbot

A command-line STEM assistant built with LangChain and Claude. The agent answers questions in mathematics, physics, astronomy, engineering, chemistry and computer science. It does this by calling tools served over MCP (Model Context Protocol) instead of doing the maths itself:

- **Computation tools** for symbolic maths, physics, chemistry and similar calculations.
- **Knowledge search tools** that run retrieval-augmented generation (RAG) over local Markdown notes.

## Architecture

```
┌──────────────┐   MCP (streamable HTTP)   ┌─────────────────────────┐
│  app/        │ ────────────────────────► │  mcp_server/            │
│  Claude agent│ ◄──────────────────────── │  computation + RAG tools│
│  (LangChain) │      127.0.0.1:8000/mcp   │  (Chroma + MiniLM)      │
└──────────────┘                           └─────────────────────────┘
```

- [app/](app/) is the chat client. [agent.py](app/agent.py) builds a LangChain agent on `ChatAnthropic` (`claude-opus-5-5`). [mcp_client.py](app/mcp_client.py) and [mcp_bridge.py](app/mcp_bridge.py) expose the MCP tools to it. [main.py](app/main.py) is the interactive loop, rate-limited to 25 calls per minute.
- [mcp_server/](mcp_server/) is the MCP server. [server.py](mcp_server/server.py) registers the tools and serves them over HTTP.
- [knowledge/documents/](knowledge/documents/) holds Markdown notes for each topic. They are embedded with `sentence-transformers/all-MiniLM-L6-v2` into a persistent Chroma store in `knowledge/chroma/`.
- [benchmark/](benchmark/) measures whether the agent picks the right tools.
- [tests/](tests/) contains the pytest suite.

## Tools

| Domain | Tools |
|---|---|
| Math | `solve_algebra`, `differentiate`, `integrate`, `find_limit`, `get_power` |
| Physics | `calculate_force`, `kinematics_velocity` |
| Astronomy | `orbital_period`, `escape_velocity` |
| Engineering | `ohms_law`, `stress_calculation` |
| Chemistry | `ideal_gas_law`, `ph_from_concentration` |
| Computer science | `base_convert`, `time_complexity_compare` |
| Knowledge (RAG) | `search_{math,physics,astronomy,engineering,chemistry,computer_science}_knowledge` |

## Setup

Requires Python 3.10 or newer and an [Anthropic API key](https://console.anthropic.com/).

```bash
python -m venv stem-venv
stem-venv\Scripts\activate        # Windows
# source stem-venv/bin/activate   # macOS / Linux

pip install -r requirements.txt
```

Create a `.env` file in the project root:

```
ANTHROPIC_API_KEY=sk-ant-...
```

`.env` is already in `.gitignore`. Do not commit it.

## Running

Run both commands from the project root. The knowledge paths are relative, so the working directory matters.

**1. Start the MCP server** (terminal 1):

```bash
python -m mcp_server.server
```

**2. Start the chatbot** (terminal 2):

```bash
python -m app.main
```

Type a question at the `You:` prompt, or `exit` to quit. Example prompts:

- `Differentiate x**3 * sin(x)`
- `What is the escape velocity of a planet with mass 6e24 kg and radius 6.4e6 m?`
- `Convert 255 from base 10 to base 2`
- `What is the definition of a Lagrange point?` (answered from the knowledge base)

### Knowledge base

Documents are indexed into Chroma by `create_all_vector_stores()` in [rag.py](mcp_server/rag.py). It skips any topic that already has entries. If you add or edit notes, delete `knowledge/chroma/` so they are re-indexed. The first run downloads the embedding model.

## Tests and benchmark

```bash
pytest                                   # unit and integration tests
python -m benchmark.evaluate_retrieval   # tool-selection benchmark (calls the Claude API)
```

The benchmark runs real model calls, so it uses API credits and needs the MCP server running.

### Benchmark results

Latest run of [evaluate_retrieval.py](benchmark/evaluate_retrieval.py) (80 queries, agent on `claude-opus-5-5`):

| Metric | Score |
|---|---|
| Tool selection accuracy | 87.50% (70/80) |
| Multi-tool accuracy | 76.92% (10/13) |

Tool selection accuracy counts a query as correct when the set of tools the agent called equals the expected set. Multi-tool accuracy is the same check, limited to queries that need more than one tool.

## Configuration

| Setting | Where |
|---|---|
| Model | `ChatAnthropic(model=...)` in [app/agent.py](app/agent.py) |
| System prompt | `create_agent(system_prompt=...)` in [app/agent.py](app/agent.py) |
| Rate limit | `RateLimiter(max_calls, period)` in [app/main.py](app/main.py) |
| MCP server host and port | [mcp_server/server.py](mcp_server/server.py) and the `url` default in [app/mcp_client.py](app/mcp_client.py) |
| Embedding model and topics | [mcp_server/rag.py](mcp_server/rag.py) |

`claude-opus-5-5` rejects sampling parameters such as `temperature`. To cut cost or latency, switch to `claude-sonnet-5-5`.
