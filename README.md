# NBA True Shooting Calculator

A Python command-line application that calculates a basketball player's **True Shooting Percentage (TS%)** and evaluates their scoring efficiency against NBA benchmarks.

## Features

- **Accurate TS% Formula:** Computes shooting efficiency factoring in field goal attempts (FGA) and free throw attempts (FTA):
  $$\text{TS\%} = \frac{\text{PTS}}{2 \times (\text{FGA} + 0.44 \times \text{FTA})} \times 100$$
- **Automated Efficiency Verdicts:** Categorizes player performance into tiers (Elite/All-Star, Above NBA Average, Below Average, or Low Efficiency).
- **Input Validation & Error Handling:** Prevents crashes from non-numeric inputs (`try/except`) and handles zero-attempt edge cases safely.
- **Continuous Analysis Loop:** Allows evaluating multiple players in a single session with strict input validation.

## How to Run

1. Clone this repository:
   ```bash
   git clone https://github.com/zubrode/nba_stats_calculator.git
   ```
2. Navigate to the project folder and run the script:
   ```bash
   python main.py
   ```

## Roadmap

- [x] Core TS% calculation and efficiency tiers
- [x] Modular function design and error handling
- [x] Interactive multi-player loop
- [ ] Integration with `nba_api` for automatic live player stats retrieval