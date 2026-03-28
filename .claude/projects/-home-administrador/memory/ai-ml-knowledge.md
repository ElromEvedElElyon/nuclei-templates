# AI/ML Knowledge Base (25 Mar 2026)

## LLM ARCHITECTURE (Core Understanding)
### Transformer Architecture
- Self-attention: O(n^2) compute, queries/keys/values
- Multi-head attention: parallel attention patterns (32-128 heads)
- Positional encoding: RoPE (rotary) most common now
- Context windows: 8K-2M tokens (Claude 200K, Gemini 2M)
- Vocabulary: BPE tokenizer (50K-100K tokens)

### Scaling Laws (Chinchilla)
- Optimal: tokens ≈ 20x parameters
- 7B model → 140B tokens optimal training
- Compute-optimal training > bigger model with less data
- Inference cost scales linearly with parameters

### Fine-Tuning Methods
| Method | Params Trained | VRAM | Best For |
|--------|---------------|------|----------|
| Full FT | 100% | 4x model | Maximum quality |
| LoRA | 0.1-1% | model+10% | Most practical |
| QLoRA | 0.1-1% | 0.25x model | Low VRAM (our case) |
| Prompt tuning | <0.01% | model only | Fast experiments |
- QLoRA: 4-bit quantized base + LoRA adapters in fp16
- For 3.3GB RAM: QLoRA on 1B-3B models (TinyLlama, Phi-2, Gemma-2B)

### RLHF / Alignment
- PPO: reward model → policy optimization (expensive, unstable)
- DPO: direct preference optimization (simpler, no reward model)
- RLAIF: AI-generated preferences (Constitutional AI)
- KTO: Kahneman-Tversky optimization (binary feedback)

## AI AGENT FRAMEWORKS
### LangChain / LangGraph
- LangChain: chains, tools, memory, retrievers
- LangGraph: stateful graphs, cycles, conditional edges
- Best for: complex multi-step reasoning with state
- Pattern: State → Node (agent) → Edge (conditional) → State

### CrewAI
- Role-based agents with goals and backstories
- Sequential or hierarchical task execution
- Best for: team-of-agents simulations

### AutoGen (Microsoft)
- Multi-agent conversation framework
- GroupChat: multiple agents discuss and decide
- Best for: code generation, multi-perspective analysis

### MCP (Model Context Protocol)
- Anthropic standard for tool integration
- Server exposes tools, client (Claude) calls them
- Transport: stdio (local), SSE (remote)
- Our implementations: claw-mcp-toolkit (TS), polymarket-mcp-server (Python)

### Agent Memory Architectures
```
Short-term: conversation buffer (current context)
Long-term: vector store (RAG) or structured JSON
Episodic: specific experiences with timestamps
Semantic: facts and knowledge (embeddings)
Procedural: learned skills and patterns
```
- Our approach (AgentMemory): JSON-based with dedup hashes, daily counts, learned patterns
- For scale: ChromaDB/Qdrant for vector search, SQLite for structured

## AI x CRYPTO (Convergence)
### Decentralized AI
- **Bittensor (TAO)**: subnet-based AI marketplace, validators score miners
- **Ritual**: on-chain AI inference, Infernet SDK
- **Gensyn**: decentralized GPU training network
- **Akash**: decentralized cloud compute (GPU marketplace)
- **io.net**: distributed GPU clustering

### ZKML (Zero-Knowledge ML)
- Prove model inference without revealing weights/inputs
- EZKL: circuits from ONNX models
- Modulus Labs: on-chain AI verification
- Use case: verifiable AI predictions for DeFi oracles

### AI Agents in Crypto
- Trading agents: MEV, arbitrage, liquidation bots
- Security agents: real-time exploit detection (our chainlink-sentinel)
- Social agents: autonomous posting (our Israel/One)
- Governance agents: proposal analysis, voting recommendations
- Bridge agents: cross-chain routing optimization

### Token-Gated AI
- NFT-gated model access
- Token-weighted model fine-tuning
- Revenue sharing for training data providers
- Decentralized model registries

## PRACTICAL AI TOOLS (For Our Hardware: 3.3GB RAM)
### Local Models That Run
| Model | Params | VRAM | Quality |
|-------|--------|------|---------|
| TinyLlama 1.1B | 1.1B | ~1GB q4 | Basic tasks |
| Phi-2 | 2.7B | ~2GB q4 | Surprisingly capable |
| Gemma-2B | 2B | ~1.5GB q4 | Google quality |
| Qwen2.5-1.5B | 1.5B | ~1GB q4 | Multilingual |
- Use: ollama, llama.cpp, or vLLM for serving
- Quantization: GGUF Q4_K_M best quality/size ratio

### APIs (Our Budget: $0)
| Service | Free Tier | Best For |
|---------|-----------|----------|
| xAI/Grok | $175/mo credits | General + real-time |
| Together AI | $100 credits | Open-source models |
| Anthropic | $5 free (new accounts) | Best reasoning |
| Google AI Studio | Generous free | Gemini, multimodal |
| Groq | Free tier | Ultra-fast inference |
| OpenRouter | Pay-per-use | Model routing |

### Embeddings (Free)
- Sentence-Transformers: all-MiniLM-L6-v2 (local, 80MB)
- Nomic Embed: open source, good quality
- Voyage AI: free tier available

## STATE OF THE ART (Mar 2026)
### Top Models
1. Claude 4.5/4.6 (Opus/Sonnet/Haiku) — best reasoning, 200K context
2. GPT-4.5/o3 — strong general, 128K context
3. Gemini 2.0 — multimodal, 2M context
4. Grok 3 — real-time data, reasoning
5. Llama 4 — best open-source
6. DeepSeek V3 — Chinese, competitive quality

### Key Capabilities
- Tool use / function calling (all major models)
- Vision (image understanding)
- Code generation and execution
- Long context (200K+ tokens)
- Structured output (JSON mode)
- Computer use (Claude)
- Reasoning traces (chain-of-thought)

## AI FOR SECURITY AUDITING
### Static Analysis + AI
- AI-powered pattern recognition on AST/CFG
- Slither custom detectors + LLM classification
- Automated finding triage (reduce false positives)

### AI Audit Assistants
- Use Claude/GPT to review code for vulnerabilities
- Pattern: system prompt with vulnerability database + code chunk
- Limitations: hallucination risk, context window limits
- Best as augmentation (not replacement) for manual review

### Automated Exploit Generation
- Fuzz seed generation via LLM
- Invariant suggestion from NatSpec/documentation
- PoC code generation from vulnerability descriptions
- Our tool: chainlink-sentinel (basic pattern matching → evolve to AI)

## BUILDING AI PRODUCTS
### Architecture Patterns
```
User → API Gateway → LLM Router → Model (Claude/GPT/Local)
                  ↓
            Tool Registry → MCP Servers → External APIs
                  ↓
            Memory Store → Vector DB + JSON State
                  ↓
            Output → Structured Response → Action
```

### Key Design Principles
1. **Model agnostic**: abstract LLM calls behind interface
2. **Tool-first**: capabilities via tools, not prompts
3. **Memory layered**: short/long/shared (our AgentMemory pattern)
4. **Fail graceful**: fallback models, retry with backoff
5. **Observable**: log all LLM calls, tool uses, decisions

### Monetization
- SaaS subscription (our Stripe products)
- API access (token-gated)
- Marketplace (tool/agent marketplace)
- Consulting (audit + AI)
- White-label (custom deployments)

## KEY PAPERS & RESOURCES
- "Attention Is All You Need" (Vaswani 2017) — Transformer foundation
- "Scaling Laws for Neural Language Models" (Kaplan 2020)
- "LoRA: Low-Rank Adaptation" (Hu 2021) — parameter-efficient FT
- "Constitutional AI" (Bai 2022) — RLAIF
- "DPO: Direct Preference Optimization" (Rafailov 2023)
- "ReAct: Synergizing Reasoning and Acting" (Yao 2022) — agent pattern
- "Toolformer" (Schick 2023) — LLMs learning to use tools
- Anthropic MCP Spec: modelcontextprotocol.io
- LangChain docs: python.langchain.com
- HuggingFace: huggingface.co (models, datasets, spaces)

## OUR AI STACK
- **Claude Code**: primary dev environment (Opus for audit, Sonnet for tasks)
- **claw-mcp-toolkit**: 29 tools (crypto, social, finance, productivity)
- **revenue-mcp**: revenue tracking via AI
- **chainlink-sentinel**: smart contract security scanner
- **Israel/One**: autonomous X posting agent with soul/memory
- **ZionAgent framework**: tool registry + skills + child agents + network
- **AgentSoul/AgentMemory/AgentNetwork**: persistence layer at ~/israel-one/
