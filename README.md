# AI T20 Cricket Player Scout

Data-driven scouting reports and auction valuations for T20 cricket — powered by ball-by-ball analytics and LLM-generated intelligence

**Live Demo:** Coming in Phase 4 — Hugging Face Spaces

Franchises keep breaking records signing players in the IPL every season. But is there a cheaper option in terms of an Indian player so that franchises don't burn their overseas spots? Does the team need an all-rounder or can a specialist pacer do the job? The ball-by-ball data for these players exist publicly but are never synthesized to give the best choices. This tool changes that.

1. Input your franchise and current squad situation
2. System identifies gaps based on released and retained players
3. Pulls ball-by-ball records across IPL, SMAT, and T20Is for candidate players
4. Computes performance profiles across phases, roles, and match situations
5. Generates an LLM-powered scouting report with ranked recommendations and auction targets

## Architecture

Data Layer - Collects ball-by-ball match data from Cricsheet, converts the source JSON into a usable format, and stores it in DuckDB as the shared data source for the rest of the system.

ML Layer - Uses the DuckDB data to build features including phase-based strike rates and player vulnerability scores. XGBoost and LightGBM models then learn to estimate player value and identify performance trends.

AI Layer - Combines the statistical analysis with the model predictions and passes the results to the Claude API, which produces a readable scouting report and auction guidance.

API Layer - Provides FastAPI endpoints for accessing the scouting workflow. Given a player name, a client can retrieve the player’s statistics and generated report as JSON.

UI Layer - Presents the API through a Streamlit dashboard designed for franchise analysts. The application is hosted on Hugging Face Spaces.

## Techstack

| Layer | Tool | Phase |
|----------|----------|----------|
| Database | DuckDB | Phase 1 |
| Data Processing | Pandas | Phase 1 |
| API | FastAPI + Uvicorn | Phase 1 |
| Testing | Pytest | Phase 1 |
| ML Models | XGBoost, LightGBM | Phase 2 |
| Explainability | SHAP | Phase 2 |
| LLM | Claude API (Anthropic) | Phase 3 |
| Frontend | Streamlit | Phase 4 |
| Deployment | Hugging Face Spaces | Phase 4 |


## Roadmap

- [x] Phase 1 — Data Foundation
- [ ] Phase 2 — ML Models
- [ ] Phase 3 — AI Layer
- [ ] Phase 4 — Deployment


## Setup

1. Clone the repo
```bash
git clone https://github.com/Nilud7/ai-t20-cricket-scout.git
cd ai-t20-cricket-scout
```

2. Create and activate the conda environment
```bash
conda create -n cricket-scout python=3.11
conda activate cricket-scout
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Run the API
```bash
uvicorn api.main:app --reload
```
## Author

Niladri Deb - https://www.linkedin.com/in/niladri-deb