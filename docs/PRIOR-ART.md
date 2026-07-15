# AI livecoding DJ — prior art (researched 2026-07-15)

## The landscape in one paragraph

The dominant 2025–26 architecture is an **MCP server bridging an LLM to a
browser Strudel REPL** (4+ independent implementations). The differentiator
between them is the **error loop**: nothing → eval-before-commit →
retry-until-valid → audio analysis of actual output → learned code↔audio
embedding ranking (NeurIPS 2025). Top failure modes everywhere: hallucinated
sample/synth names, and musically-flat-but-valid code. **Musical transitions
are unsolved in every project** — all do turn-based pattern replacement,
nothing beat-matched. And **no 24/7 autonomous LLM livecoding DJ stream
exists** as of mid-2026. Those two gaps are this project's opportunity (and
`ref()`-based crossfading — see STRUDEL-API.md — is the transition primitive
nobody is using).

## LLM era

- **StrudelLM** (Tambo team) — chat agent beside a Strudel REPL;
  `validateAndUpdateRepl` tool retries until the pattern evaluates (clearest
  documented error loop). AGPL-3.0. strudellm.com / github.com/tambo-ai/strudellm
- **apfelstrudel** (Rui Carmo) — Strudel fork + agentic tool loop over WS
  (read/write pattern, play/stop, tempo, docs lookup, `strudel_evaluate` for
  testing without touching the editor). github.com/rcarmo/apfelstrudel
- **strudel-mcp-bridge** (Phil Dougherty) — minimal 336-line MCP + browser
  extension; exec success/failure fed back. github.com/phildougherty/strudel-mcp-bridge
- **live-coding-music-mcp** (William Zujkowski) — 27-tool MCP incl. audio
  analysis of actual output; drives visible Chromium on strudel.cc.
- **calvinw/strudel-llm-docs** — LLM-oriented Strudel docs + hosted remote MCP
  (play_code/stop_play/get_currently_playing_code).
- **strands-strudel** (AWS Strands) — Python agent → WS broadcast to browser
  players, 13 preset styles.
- **etbars/strudel-claude-music-generator**, **bohara2000/strudel-llm-integration**
  — simpler NL→code→embedded REPL, no error loop.
- **Okuda & Jo, JSSA 2022** — earliest systematic study (GPT-3/Codex/fine-tuned
  Davinci → TidalCycles): syntax mostly valid, musical intent poorly followed,
  hallucinated sample names; coins the AI "code jockey (CJ)". data.jssa.info/paper/2022v14n03/1.Okuda.pdf
- **Kouteili et al., NeurIPS 2025 AI4Music** — code↔audio embedding alignment to
  rank candidate patterns by predicted sound ("LLMs can't hear what they
  wrote"). arxiv.org/abs/2508.05473

## Pre-LLM autonomous performers (the deep prior art)

- **Cibo / Cibo v2** (Stewart & Lawson, ICLC 2019/20) — seq2seq/VAE trained on
  human Tidal performances; fully autonomous on stage. The canonical machine DJ.
- **Autopia** (Lorway, Powley, Wilson) — genetic programming writes
  SuperCollider; audience phone votes = fitness function.
- **tidal-fuzz → Tidal-MerzA** (Elizabeth Wilson, McLean; then RL + affective
  model, arxiv.org/abs/2409.07918) — type-checked generation, only valid Tidal.
- **Ai.step** — deep-learning Tidal generation, human curates/executes.
- **tidal-autocode** (Kindohm) — rule-based auto-generator on a hotkey.
- **Twitch-chat AI radio** (Adrian Chrysanthou) — chat writes lyrics, ACE-Step
  generates songs in a loop; nearest thing to a 24/7 AI music stream (audio
  model, not livecoding).

## Design lessons for clawd-dj

1. **Validate before committing audio** — eval in a shadow context, retry on
   error (StrudelLM's loop); never let a syntax error hit the dancefloor.
2. **Pin the vocabulary** — hallucinated sample names are the #1 failure; the
   `knowledge/` lessons + a whitelist of loaded banks are the guard.
3. **Transitions are the open problem** — nobody beat-matches; `xfade`/`ref` +
   cycle-aligned cuts (verified in STRUDEL-API.md) can leapfrog every project above.
4. **The 24/7 stream doesn't exist yet.**
