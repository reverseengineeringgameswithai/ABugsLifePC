---
type: experiment
id: EXP-20261007-001
date: 2026-10-07
binary_sha256: 97c95ba5572dce637f6ea6325dbfff0c9a2d002a30d3dc88f39e0f558a27b878
environment: Fedora host; existing loopback Kev NVFP4 server on RTX 5090; Python stdlib HTTP client; no game launch or memory access
question: Can the installed local Kev model classify known PC research claims without promoting missing or inferred evidence?
result: 35 of 36 primary labels matched; 36 of 36 in each of two option permutations; 36 of 36 insufficient with evidence removed. Useful pilot for claim review, not autonomous research authority
status: complete-bounded
created: 2026-10-07
updated: 2026-10-29
evidence: [EXP-20261005-001, EXP-20261005-002, EXP-20261005-004, EXP-20261003-001, EXP-20261001-002, EXP-20261001-006]
tags: [experiment/tooling, re/workflow]
---

# EXP-20261007-001 - Local Kev evidence classification probe

## Question and scope

The user asked whether `~/AI/Kev` could help this project using facts already
known. The installed path is `/home/dev/AI/kev` (lowercase). This experiment
evaluates classification of supplied research text. It does not produce new
PC behavior evidence, resolve the underlying unknowns, or assess disassembly
reasoning, retrieval, code generation or game control.

## Provenance

- ABLPC entry commit: `06c27c3d8ca6dd14cf3c6208bdf780b89c61f0f6` (clean).
- Kev source: `84847f0a883d900f7de5b7a57eaa341ca7f9a6b4`.
- Installation-reported model: `SVPG-Labs/kev-27b-NVFP4`, revision
  `ba00fe3c9b43fa59ab3e76199f2292d5ca47e0c7`, based on official revision
  `af0e6d551bdc2cc724f3e9d7a8bee1cd4fb8f7bf`. Pins come from
  `local/provenance.json`; weights were not independently re-hashed here.
- Live `/v1/models` identifies
  `kev27b-af0e6d55-lh2048-w4a4-cutlass-20261003`, temperature 1.3195079,
  CUDA/torch, 32,768-token maximum, truncation disabled, one cached state
  with an 8,192-token budget. The API's `bfloat16` field does not describe
  the packed weights; the installed loader and model name identify NVFP4.
- Existing server PID 18221 and browser PID 18245 were observed, not started
  or stopped by this work. Endpoint: `http://127.0.0.1:8021/v1/systemone`.
  No hosted inference or cloud compute was used.
- Working-copy retail EXE independently re-hashed as the frontmatter hash;
  a derived EXE independently re-hashed as
  `c3d8b207267b416679e963254dff837b7c8e6060136627e8c991c62120ad9027`.
- `reports/kev/EXP-20261007-001/frozen.json` records source paths, complete
  source hashes, selected verbatim sections with line spans, binary hashes,
  source/runner pins, labels and their rationales. Freeze SHA-256:
  `2151d8c043e78bf783858b16dc45ca22d1faf24eff69d7f3d9f9b475a8d7672d`.
  Frozen at 2026-10-08 02:09:47 UTC (October 7 in Toronto), before inference;
  completed at 02:10:07 UTC.

## Method

`research/kev-evaluation/claims.json` fixes six groups of six claims: Thumper,
the other bosses, collision in a derived level, the camera guard, Flik
animations and a derived build's pickup crash. There are 12 supported, 12 contradicted and 12 insufficient
labels, authored from the cited notes before reading any model result.

The client sends source excerpts and six claim questions per request. Labels
and annotation rationales are never sent. Each question has three described
choices. Supported means established within the evidence's scope;
contradicted includes an explicit overstatement of what an experiment
established; insufficient means the factual question remains unsettled.

Four variants were frozen: primary choice order, rotated order, reversed
order, and no evidence. The latter replaces all excerpts with a sentence
saying none were supplied and expects insufficient for every claim. Each
variant explicitly instructs the model to use only the supplied evidence.
No prompt adjustment, label revision, training, threshold fitting or retry
followed the results. The 0.9 top-probability diagnostic was set before the run.

## Results

Raw requests and responses, HTTP timing, request IDs, model metadata and
per-question distributions are in `reports/kev/EXP-20261007-001/`.
`results.json` is the machine-readable summary.

| Arm | Matched labels | False supported answers | Median wall time per six claims |
|---|---:|---:|---:|
| Primary | 35/36 | 0 | 953 ms |
| Rotated choices | 36/36 | 0 | 665 ms |
| Reversed choices | 36/36 | 0 | 669 ms |
| No evidence | 36/36 insufficient | 0 | 280 ms |

The primary arm matched all 12 supported and all 12 insufficient labels,
and 11/12 contradicted labels. There were 32 primary answers with top
probability at least 0.9, all matching their labels. This small selected set
does not establish calibration or validate that threshold for future use.

**Mismatch q09:** “The experiment established that the centipede is immune
to purple-berry damage.” Frozen label: contradicted, because EXP-20261005-002
explicitly reports the damage test as inconclusive. Kev chose insufficient
(0.6257), with contradicted 0.3708 and supported 0.0035. This is a conservative
distinction between an unsupported immunity claim and a false claim about
what was demonstrated; it did not promote immunity to fact. Preserve the
original scoring rather than relabel this case after seeing the output.

q09 changed to contradicted under both other choice orders. Across all
questions the maximum probability movement was 0.2585. The other 35 choices
were stable. Choice order therefore affects this installation's output.

24 requests returned 144 decisions in 15.53 s of summed HTTP wall time.
These are **warm-model** measurements: the model was already loaded. The
evidence requests report 2,082–3,092 input tokens including questions;
reordered requests reused state caches (12 additional cache hits overall).
There were no additional OOM retries. This is not a model-startup, throughput,
32k-context, or large-vault benchmark.

## Interpretation

**Confirmed by this probe:** the installed service can batch bounded PC
research claims, reject these false assertions, and retain these unknowns.
Examples include keeping homing lock-on unknown, separating static animation
cataloguing from live validation, recognizing Thud's respawn, and rejecting
all-rooms hardware acceptance for a one-room camera test.

**Inferred practical use:** a second pass over a proposed research note or
handoff could flag unsupported statements and suggest claims for human/agent
review. Provide retrieved evidence explicitly and retain its source locator.
Use deterministic scripts for hashes, counts, offsets and literal wording;
Kev can help with semantic scope differences that exact text search misses.
It cannot retrieve the evidence or supply textual reasoning through this API.

**Unknown:** performance on unseen notes, stale/conflicting documents,
retrieval errors, raw x86, numerical reasoning, long contexts and genuinely
novel hypotheses. The cases and excerpts were selected by one agent, some
notes explicitly state the correct status, and no independent reviewer or
holdout was used. Model scores are not probabilities that a game hypothesis
is true. This result does not justify automated confirmation, semantic
renaming, patch acceptance, publication or memory-write authorization.

## Recommendation and next experiment

Try Kev as an optional advisory claim-review step beside `claim-sweep.py`.
Keep the authority in the cited PC evidence and existing checks. No pipeline
integration was installed by this experiment.

Before wider use, freeze an independently labelled set from different
experiments, include raw evidence and deliberately stale competing notes,
and measure false supported answers, abstentions and order sensitivity.
That measures whether it adds value beyond this curated reading test.

## Reproduction and closure

With the existing local API running, choose a fresh output directory:

```bash
python3 research/kev-evaluation/evaluate.py freeze --out work/experiments/kev-rerun
python3 research/kev-evaluation/evaluate.py run --out work/experiments/kev-rerun
```

The runner refuses to overwrite a packet, validates distributions, and saves
the exact request before sending. A new freeze binds the then-current notes;
the recorded frozen packet remains the authority for this experiment.
No game files, original material, Kev source or model weights were changed.
`session-audit.txt` reports no game processes, sinks or open sessions and
`clean: true`; it does not count the pre-existing Kev service as a game.
Session validation is recorded in
[[2026-10-07 - Codex - Evaluate local Kev against known PC facts]].
