# NBA Stats Explorer & Analytics CLI

A modular Python command-line application that fetches live and historical NBA player statistics via `nba_api` to compute full box scores, advanced efficiency/impact metrics, and era-aware comparative benchmarks against league averages.

## Features

- **Modular Architecture**: Clean separation between data retrieval and caching (`api_client.py`), statistical formulas and classification tiers (`metrics.py`), and the interactive CLI (`main.py`).
- **Player Search & Historical Seasons (Mode 1)**: Retrieves full per-game box scores (`PTS`, `REB`, `AST`, `STL`, `BLK`, `TOV`, `PF`, shooting splits, and `PRA`) alongside advanced metrics for any season in a player's career.
- **Advanced Basketball Metrics**:
  - **True Shooting Percentage (`TS%`)**: Measures overall scoring efficiency accounting for two-pointers, three-pointers, and free throws.
  - **Effective Field Goal Percentage (`eFG%`)**: Adjusts field goal percentage for the added value of three-point shots.
  - **Free Throw Rate (`FTr`)**: Measures how frequently a player gets to the free-throw line relative to field goal attempts.
  - **Assist-to-Turnover Ratio (`AST/TOV`)**: Evaluates playmaking efficiency and ball security.
  - **Game Score (`GmSc`)**: John Hollinger's all-in-one single-game productivity metric.
- **League Benchmark Analysis (Mode 2)**: Compares any player's selected season against rotation-player league averages (`GP >= 10`, `MIN >= 10.0`) with a 5-tier evaluation verdict, supporting both same-era comparisons (from 1996-97 onward) and modern-era benchmarks with pace/era context notices.
- **In-Memory Session Caching**: Caches league-wide `LeagueDashPlayerStats` queries by season to minimize API calls and speed up multi-stat evaluations.

## Project Structure

```text
nba_stats_calculator/
├── api_client.py      # NBA API integration, season selection, and league-average caching
├── metrics.py         # Advanced metric formulas, stat catalog, and 5-tier verdict logic
├── main.py            # Interactive CLI entry point and user workflow
├── requirements.txt   # Project dependencies
├── .gitignore         # Excludes .venv/ and __pycache__/
└── README.md          # Project documentation

## How to Run

1. Clone this repository:
   ```bash
   git clone https://github.com/zubrode/nba_stats_calculator.git
   ```
2. Navigate to the folder:
   ```bash
   cd nba_stats_calculator
   ```
3. Create and activate a virtual environment (recommended):
   - Windows (PowerShell):
      ```bash
      python -m venv .venv
      .\.venv\Scripts\Activate.ps1
      ```
   - macOS/Linux:
      ```bash
      python3 -m venv .venv
      source .venv/bin/activate
      ```
4. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Run the script:
   ```bash
   python main.py
   ```

## Roadmap

- [x] Core TS% calculation and efficiency tiers
- [x] Modular function design and error handling
- [x] Interactive multi-player loop
- [x] Integration with nba_api for automatic live player stats retrieval
- [x] Modular codebase (api_client.py, metrics.py, main.py) with full box score and advanced metrics (eFG%, FTr, AST/TOV, PRA, GmSc)
- [x] Historical season selection and 5-tier comparative analysis against NBA league averages
- [ ] Head-to-head 1v1 player comparison mode
- [ ] Interactive "Higher or Lower" NBA stats mini-game
- [ ] Web interface with Streamlit