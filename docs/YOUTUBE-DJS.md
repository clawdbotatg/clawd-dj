# The YouTube livecoding DJs — study curriculum

Census of livecoding music creators on YouTube (researched + verified via yt-dlp
2026-07-15). This is the source list for the `learn/` pipeline. Filter rule:
**narrated/tutorial videos give useful transcripts; pure performance sets give
`[Music]` garbage** — pick videos whose titles say narrated / tutorial /
beginners / from scratch / how. Code is on screen universally (TOPLAP "show us
your screens" convention), and Strudel videos often link the actual pattern
(strudel.cc URL) in the description — **check the description before OCR-ing
frames**.

## Tier 1 — narrated Strudel builds (primary corpus)

| Creator | Scale | Why | Start with |
|---|---|---|---|
| **Switch Angel** (Jade Rose — Strudel maintainer) | 152k subs, top videos 240k–1M | The single best explain-while-building source; 7-video Strudel Tutorials playlist + narrated builds | `GWXCCBsOMSg` Coding Trance (Full Narrated, 6min) · `iu5rnQkfO6M` Trance from Scratch (1M views) · `HkgV_-nJOuE` Deep Acid ✅ studied · `dcmwqqzJubA` Chopping Breaks · `3h1vM0lIrpM` Chopping Pt.2 DNB · `AifAIqHezb8` Cold Machines (narrated). Playlist: `PLY9reO_9KeE9fJIsgeYN_QkEO46QxDPPP` |
| **Glossing** | 2.6k subs but 38k on flagship | 100% tutorial channel, late-2025/2026, modern Strudel | `m7Rp46AU8dw` STRUDEL FOR BEGINNERS (house, start-to-finish) · `7NyoZkJgykQ` Euphoric Trance Start to Finish (46min) · `11frBA9L638` Modulate ANYTHING · `8ruLuZv1ju8` FM synthesis |
| **Dan Gorelick + Viola He** workshop | 107k views | The richest single transcript found: 82-min full Strudel workshop | `oqyAJ4WeKoU` (fetch with `--interval 20`) |
| **Groovin in G** | 20.5k subs | Producer-educator; music-production thinking, DnB/jungle, break chopping | `tKeJhjvTabc` Beginners (16min) · `CNJKqWRCLM8` Break Chopping & Mini Notation · `JNP-1AN1xQM` Break Processing |
| **DJ_Dave** (Sara Davis) | 32k subs | Process explainers + the crossover-star performance style | `ZCcpWzhekEY` coding dance music in strudel (166k) · `xAAbQMW0dFk` my process (short) · `W24pteoigXk` Hard Refresh process |

## Tier 2 — pattern-language depth (TidalCycles ≈ Strudel mini-notation)

- **Alex McLean (yaxu)** — Tidal's author; full free `[TidalClub]` course on his
  channel (`nBpCJcduMso` mini-notation pt 1, `_bcG2_zDjyw` patterning effects).
  Text companion: slab.org/tidal-workshops.
- **Kindohm (Mike Hodnick)** — 20-video numbered Tidal curriculum
  (`PLKgxw7RG3hcRHyBFsPr5opr1iu8wbNIgP`); `eGdL4d7_Uw4` workflow-from-scratch.
- **Eric O Meehan** — 7-part music-theory-forward Tidal series (melody,
  harmony, counterpoint): `PLEAKPxTLOpJyTPRwkHpgO1gpctIHVKko1`.

## Tier 3 — context / style / monitoring

- **eddyflux (Felix Roos — Strudel author)**: performance-heavy; `mrq8t2ZznzE`
  "pastagang live thinking #1" is his think-aloud. His real teaching is the
  interactive workshop at strudel.cc/workshop (no official Strudel YouTube course exists).
- **LearningTheWires** — 14-video Strudel session playlist incl. `JVr-RsZOXV8`
  "Live-Coding the Drop" (build/drop arrangement).
- **Lucy Cheesman (Heavy Lifting)** — chatty live coding; `QRJ0xrjLj6A` Site
  Gallery workshop (70k views).
- **Sam Aaron** (Sonic Pi author) — `G1m0aX9Lpts` ambient electro set (215k).
- **GoSuraj** — tiny but mirrors code to text blog posts (gosuraj.com/blog) — no
  frame OCR needed.
- **Eulerroom** (TOPLAP archive, 1000+ performances) + weekly "Flok WeekEndJam"
  streams — live.eulerroom.com. **kindohm** streams on Twitch. pastagang jams at
  nudel.cc. No true 24/7 livecoding stream exists as of mid-2026.
- Indexes: `github.com/terryds/awesome-strudel`,
  `github.com/toplap/awesome-livecoding`, algorave.com, club.tidalcycles.org.

## #algorave hashtag mining (2026-07-15, via `yt-dlp https://www.youtube.com/hashtag/algorave`)

The hashtag page is a live discovery feed — re-mine it periodically. New finds
beyond the census above:

- **Aviara** — `vAPX6g2eHgA` Livecoding Hard Groove Techno in Strudel from
  Scratch (16k views) — new creator, harder techno niche.
- **Switch Angel DNB pair** — `aPsq5nqvhxg` Livecoding melodic DNB (152k) ·
  `IhZeHfuDZoQ` Coding Drum and Bass like it's the year 3000.
- **LearningTheWires AlgoRave vols** — `1-cPuOlbib8` Copying Daft Punk in
  Strudel (imitating-a-known-artist is exactly the DJ-brain skill) ·
  `Ho0kW_CT2Q8` BASS KING.
- **DJ_Dave** — `LaKT3pli5EQ` GitHub Universe 2020 set · `W24pteoigXk` Hard
  Refresh process (already in census).
- **Context**: `h340aNznHnM` The Guardian "is algorave the future of dance
  music?" (65k).

## Instagram (DJ_Dave especially — user tip)

DJ_Dave posts a lot of process content on Instagram. yt-dlp can fetch public
reels but IG is auth-walled/flaky anonymously — the reliable path on this
machine is the browser-automation skill (real logged-in Chrome profile via
CDP) to enumerate reel URLs, then `yt-dlp --cookies-from-browser chrome <url>`
into the same `learn/fetch.py` corpus shape. Not yet wired up; treat as the
next learn-pipeline extension.

## Pipeline notes (verified)

- All sampled videos have English **auto**-captions (no manual subs):
  `yt-dlp --write-auto-subs --sub-langs en --skip-download <url>`.
- Strudel's REPL highlights active pattern events — helps frame reading.
- Studied so far: `knowledge/lessons/switchangel-deep-acid.md`.
