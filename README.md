# 🦞 Skills Creator Agent

**Voice-first, dialogue-driven AI Skill creation** — turn domain expertise into production-ready Agent Skills through Socratic conversation.

Built on [OpenClaw](https://openclaw.ai/) with [BigModel (GLM-5)](https://open.bigmodel.cn/) as the default LLM.

## Three Modes

| Mode | Output | Use Case |
|------|--------|----------|
| 🔧 **Skill Mode** | One `SKILL.md` + scripts + tests | Personal automation, project-specific tools |
| 👥 **Plugin Mode** | Complete plugin: `plugin.json` + N skills + commands + MCP config | Enterprise digital employees, team distributions |
| 🏢 **Enterprise Mode** ([Plugin Studio](./enterprise/)) | Multi-tenant deployment serving an entire company | Companies that want every employee to self-serve their own AI digital coworker |

**Plugin Studio** is the deployment kit: install once on a company server, employees talk to it via Slack/Telegram/Web/voice → it either installs a ready-made plugin matching their role, or walks them through generating a new one. Admin approval gate, internal marketplace, audit trail. See [`enterprise/README.md`](./enterprise/README.md).

Plugin Mode generates **enterprise-ready digital employees** — bundles of skills wrapped as Claude Code Plugins, including Slack/Notion/Salesforce MCP integration. Inspired by [Anthropic's knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins). 10 baseline role templates included (Sales Ops, Finance Analyst, Customer Support, Recruiting, ...).

## What It Does

Domain experts describe their repetitive tasks through natural conversation. The agent:

1. **Asks** probing questions to extract tacit knowledge (IDEATION → REFINEMENT)
2. **Generates** a complete Skill with proper structure and scripts (GENERATION)
3. **Creates** behavioral test cases from the conversation examples (EVAL)
4. **Runs** tests and reports results (TEST)
5. **Iterates** fixes based on failures (ITERATE)
6. **Exports** to multiple agent frameworks (EXPORT)

The expert never needs to know any syntax — they just talk.

## 📦 See Real Examples

### Skill Example
Browse [`examples/commit-message-enhancer/`](./examples/commit-message-enhancer/) for a single-skill output (12 dialogue decisions → SKILL.md + 8 evals + 4 framework exports).

### Plugin Example (Enterprise Digital Employee)
Browse [`examples/sales-ops-plugin/`](./examples/sales-ops-plugin/) for a complete **Sales Ops Associate** digital employee:

- 4 skills (prospect-research, call-prep, pipeline-review, battlecard-update)
- 1 command (`/sales-ops:weekly-report`)
- Slack + Notion MCP server config
- Validated and packaged via `package_plugin.py` → `sales-ops.zip` + marketplace snippet

### Skill detail

Skill mode produces an end-to-end reproducible output from 12 dialogue decisions:
- [Conversation transcript](./examples/commit-message-enhancer/transcript.md) (15 turns)
- [Generated SKILL.md](./examples/commit-message-enhancer/SKILL.md) with scripts + glossary
- [Auto-generated eval suite](./examples/commit-message-enhancer/evals/eval-suite.json) (8 behavioral tests)
- [4 framework exports](./examples/commit-message-enhancer/exports/)

The generated script even catches fake API keys planted in test diffs.

## 10 Baseline Enterprise Roles

Plugin Mode ships with role templates (`workspace/skills/plugin-creator/references/role-templates/`) for instant scaffolding:

| Role | Plugin Output |
|------|---------------|
| Sales Ops Associate | `sales-ops/` — 4 skills + weekly-report command + Slack/Notion |
| Finance Analyst | `finance-analyst/` — 6 skills (journal entry, reconciliation, variance analysis, ...) |
| Customer Support Specialist | `customer-support/` — 5 skills (triage, drafting, escalation, KB) |
| Recruiting Specialist | `recruiting/` — 4 skills (JD drafting, screening, notes, offers) |
| Marketing / Product / Legal / Data / Search / Productivity | See [`enterprise-roles.md`](./workspace/skills/plugin-creator/references/enterprise-roles.md) |

## Supported Export Formats

| Format | Output | Target |
|--------|--------|--------|
| Claude Code | `SKILL.md` + scripts/ | [Claude Code](https://docs.anthropic.com/en/docs/claude-code) |
| OpenClaw | `SOUL.md` + `AGENTS.md` + skills/ | [OpenClaw](https://openclaw.ai/) |
| Cursor | `.cursorrules` | [Cursor IDE](https://cursor.sh/) |
| Hermes | `agent.yaml` + prompts/ | [Hermes Agent](https://github.com/NousResearch/hermes-agent) |
| Generic | `PROMPT.md` | Any LLM with system prompt support |

## Quick Start

### Prerequisites

- [OpenClaw](https://openclaw.ai/) 2026.3+
- Python 3.10+
- An OpenAI-compatible LLM API key

### Setup

```bash
# Clone
git clone https://github.com/xiaopingfeng/skills-creator.git
cd skills-creator

# Install Python deps
pip install -r requirements.txt

# Register as an OpenClaw agent
openclaw agents add skills-creator --workspace ./workspace

# Configure your LLM (example: BigModel)
export OPENAI_API_KEY=your-api-key
export OPENAI_BASE_URL=https://open.bigmodel.cn/api/paas/v4

# Start the gateway
openclaw gateway

# Chat via terminal
openclaw tui
```

### Or use standalone (no OpenClaw)

The skills and scripts work independently:

```bash
# Generate a skill from a session file
python3 workspace/skills/skill-generator/scripts/validate_skill.py ./my-skill/

# Export to Cursor Rules
python3 workspace/skills/skill-exporter/scripts/export_skill.py \
  --format cursor --session session.json --skill-dir ./my-skill/ --output ./exports/
```

## Architecture

```
Expert Voice/Text → OpenClaw Talk Mode
  → Brain (SOUL.md + AGENTS.md drive 7-phase dialogue)
    → skill-elicitor    (question bank, summary templates)
    → skill-generator   (SKILL.md generation + validation)
    → eval-generator    (behavioral test cases)
    → skill-tester      (automated test runner)
    → skill-exporter    (multi-framework export)
  → Response to Expert
```

### Workspace Structure

```
workspace/
├── SOUL.md                          # Agent personality
├── AGENTS.md                        # 7-phase workflow
├── TOOLS.md                         # Environment config
├── USER.md                          # Expert profile (auto-populated)
└── skills/
    ├── skill-elicitor/              # Dialogue engine
    │   ├── SKILL.md
    │   └── references/
    │       ├── question-bank.md     # CN/EN question corpus
    │       └── summary-templates.md # Phase transition summaries
    ├── skill-generator/             # SKILL.md producer
    │   ├── SKILL.md
    │   ├── scripts/
    │   │   ├── init_skill.sh        # Directory scaffolding
    │   │   └── validate_skill.py    # Format validation
    │   └── references/
    │       ├── skill-anatomy.md     # Writing guidelines
    │       └── example-skills.md    # Reference examples
    ├── eval-generator/              # Test case creator
    │   ├── SKILL.md
    │   └── scripts/
    │       └── generate_evals.py
    ├── skill-tester/                # Test runner
    │   ├── SKILL.md
    │   └── scripts/
    │       ├── run_eval.sh
    │       ├── run_suite.sh
    │       └── analyze_results.py
    └── skill-exporter/              # Multi-framework export
        ├── SKILL.md
        ├── scripts/
        │   └── export_skill.py
        └── references/
            └── export-formats.md
```

## Design Principles

- **One question per turn** — optimized for voice; multi-question turns confuse speakers
- **Verbal summaries at phase transitions** — the expert confirms understanding before proceeding
- **Behavioral tests, not string matching** — skills produce varied output; behavior matters
- **LLM-judged phase transitions** — no hard-coded gates; the agent decides when to advance
- **Framework-agnostic knowledge** — session.json captures decisions independently of any target format

## License

MIT
