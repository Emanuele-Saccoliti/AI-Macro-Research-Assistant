# AI-powered Macro Research Assistant

This repository provides an AI research harness that constrains LLM-based interpretation within a deterministic, transparent, and traceable framework.

Starting from a macro question, the system expands it into fixed research perspectives, retrieves relevant news, uses an LLM to normalize heterogeneous evidence into structured events, discovers emergent themes through embeddings and clustering, maps those themes into a five-dimensional macro state, infers a macro regime through explicit rules, and derives conditional cross-asset implications using inspectable research weights.

The LLM is used for bounded semantic tasks, primarily event normalization and final report narration. Query planning, retrieval, schemas, clustering, theme aggregation, macro scoring, regime classification, and cross-asset mapping are implemented as explicit, inspectable Python logic.


## Pipeline

```text
User query
        ↓
Deterministic query expansion, retrieval, and deduplication
        ↓
Web search and RSS feeds
        ↓
LLM event normalization
        ↓
Embeddings, semantic clustering, and dynamic theme discovery
        ↓
Semantic macro mapping and theme aggregation
        ↓
Aggregate macro state
        ↓
Deterministic regime inference and cross-asset mapping
        ↓
Cross-asset research report
```

## Semantic theme and macro mapping

Each normalized event is embedded into a numeric semantic representation. `AgglomerativeClustering` groups related event embeddings without requiring a predefined set of themes.

```text
Normalized events
        ↓
Event embeddings
        ↓
Semantic clustering
        ↓
Emergent themes
        ↓
Theme centroid embedding
        ↓
Comparison with ten semantic anchor prototypes
(five macro axes × two opposing poles)
        ↓
Five macro scores per theme
        ↓
One MacroAxisVector per theme
```

The five macro axes are growth, inflation, policy, liquidity, and risk sentiment. For each axis, the theme centroid is compared with positive and negative textual anchors using cosine similarity. The relative similarity and strength of the evidence produce a continuous score between -1 and +1.

Visually:

```text
Growth:         contraction -1 ←→ +1 expansion
Inflation:      disinflation -1 ←→ +1 inflation
Policy:         easing -1 ←→ +1 tightening
Liquidity:      contraction -1 ←→ +1 expansion
Risk sentiment: risk-off -1 ←→ +1 risk-on
```

The anchor prototypes are transparent research priors, not trained classifier parameters. This makes their assumptions directly inspectable and replaceable with supervised models when reviewed labelled data becomes available.

The default implementation uses semantic anchor prototypes. It is intentionally replaceable with a supervised multi-label classifier once a reviewed training set is available.


## Macro-state aggregation and regime inference

Theme-level macro vectors are aggregated using transparent weights informed by attention, breadth, mapping confidence, and momentum.

```text
Theme-level macro vectors
        ↓
Weighted aggregation
        ↓
Aggregate five-dimensional macro state
        ↓
Explicit threshold and rule evaluation
        ↓
One inferred macro regime
        ↓
Cross-asset implication scores
```

The current regime taxonomy includes:

* `goldilocks`: positive growth and falling inflation. A scenario that is generally supportive of risk assets and duration.
* `reflation`: positive growth and positive inflation. The economy is accelerating, but inflationary pressure is also increasing.
* `stagflation_pressure`: weak or negative growth combined with elevated inflation. This is an unfavourable macroeconomic combination.
* `recession_disinflation`: weak or negative growth and falling inflation. It indicates an economic slowdown or recession alongside disinflation.
* `policy_tightening`: growth and inflation do not produce one of the four core regimes, but the policy component indicates materially tighter monetary conditions.
* `policy_easing`: analogous to `policy_tightening`, but with a strong indication of monetary easing.
* `risk_off`: no preceding regime dominates, but risk sentiment is clearly negative.
* `mixed_transition`: an ambiguous, neutral, or transitional state, without signals strong enough to satisfy the other rules.


## Project Structure

```text
.
├── src/ai_macro_research_v2/
│   ├── clustering.py               # dynamic event clustering
│   ├── embeddings.py               # hashing or transformer embeddings
│   ├── history.py                  # theme matching and temporal metrics
│   ├── llm.py                      # event normalization and report narration
│   ├── mapping.py                  # transparent cross-asset mapping
│   ├── regimes.py                  # macro-axis and regime inference
│   ├── reporting.py                # Markdown and JSON reports
│   ├── retrievers.py               # DuckDuckGo and RSS retrieval
│   ├── schemas.py                  # Pydantic contracts
│   └── workflow.py                 # end-to-end orchestration
├── tests/
└── pyproject.toml
```

## Setup

Run the following commands from the `v2/` directory.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env
```

Add `OPENAI_API_KEY` to `.env`.

The lightweight default uses `HashingVectorizer` embeddings. For transformer embeddings:

```bash
pip install -e ".[dev,transformers]"
```

Then set:

```text
EMBEDDING_PROVIDER=sentence-transformer
```

## Usage

```bash
python -m ai_macro_research_v2 \
  "US inflation, Fed policy and cross-asset implications" \
  --max-articles 30
```

Add RSS sources:

```bash
python -m ai_macro_research_v2 \
  "global monetary policy divergence" \
  --feed-url "https://www.federalreserve.gov/feeds/press_all.xml"
```

Theme history is stored in `data/theme_history.json`. To run without reading or updating it:

```bash
python -m ai_macro_research_v2 "China growth and commodities" --no-history
```

## Outputs

- Normalized events with entities, regions, key facts, and LLM confidence.
- Dynamic themes with interpretable narrative metrics.
- Continuous macro state vector and inferred regime.
- Conditional cross-asset implications for equities, government bonds, USD, commodities, and credit.
- Markdown and machine-readable JSON reports.

## Validation

```bash
python -m compileall src tests
ruff check .
pytest
```

## Limitations

This is a research prototype rather than a production-grade forecasting or investment system. Several deterministic components, including semantic anchors, thresholds, and asset weights, are intentionally transparent research heuristics that remain open to historical calibration and validation.


## Disclaimer

This project is intended for research and educational purposes only. It does not constitute investment advice, financial advice, trading advice, or a recommendation to buy, sell, or hold any asset. Model outputs should not be used for live trading or investment decisions without independent verification and professional judgment.
