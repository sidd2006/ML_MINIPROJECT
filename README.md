# College Football Bowl Game Predictor

UE24CS352A Machine Learning, mini-project. Predict the winner (and a confidence) of college football
bowl games from regular-season results, in the style of the Stanford "Bowl Game Predictor" report.

- **Data:** 356 bowl games, 2003 to 2013 seasons
- **Features:** 7 per team (record, points for/against, capped margin, opponent-adjusted rating,
  strength of schedule, last-4-games form), all computed from regular-season games only
- **Models:** two baselines, linear regression, ridge, forward-selected linear, random forest,
  gradient boosting, logistic regression
- **Evaluation:** leave-one-season-out cross validation (11 folds), plus a bowl pick'em score
- **Best result:** ridge, 60.4% accuracy (95% CI 55% to 65%) vs 54.8% for "pick the better record"

## Setup

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Python 3.9+ is fine. No internet needed, the data is already in `data/raw`.

## Run

```bash
python run_all.py                # builds the dataset, evaluates all models, runs the leakage check
```

Or step by step (run these from inside `src/`):

```bash
cd src
python build_dataset.py          # -> data/processed/bowl_games.csv
python evaluate.py               # -> results/*.csv and results/*.png
python leakage_check.py          # -> results/leakage_check.csv (why we dropped the teamrankings stats)
```

Predict a single game (the model is trained on every other season, so the season you ask about is
never in the training data):

```bash
python src/predict.py --season 2013 --team-a "Florida State" --team-b Auburn
```

Team names are the ones in the game log ("Florida State", "Ohio State", "Michigan State", ...).

## Project layout

```
run_all.py                 runs everything
src/build_dataset.py       regular-season games + bowl results -> one row per bowl game
src/models.py              antisymmetric model wrappers (swap A/B and the prediction flips)
src/evaluate.py            leave-one-season-out CV, metrics, figures
src/predict.py             single-game demo
src/leakage_check.py       shows the teamrankings season stats already contain the bowl game
data/raw/                  input data (see below)
data/processed/            bowl_games.csv, the modelling table
deliverables/              writeup.pdf (2-page write-up), bowl_predictor_slides.pptx (review deck)
results/                   model_comparison.csv, accuracy_by_season.csv, confidence_buckets.csv,
                           ridge_coefficients.csv, leakage_check.csv, figures
```

## How it works (short version)

1. For every team and season, compute features from regular-season games only. The opponent-adjusted
   rating is a ridge regression of game margins (capped at 28) on team indicators plus a home-field term.
2. For each bowl game, take the **difference** of the two teams' features (team A minus team B).
3. Models predict the score margin (or win log-odds). Everything is antisymmetric, so the order of
   the two teams does not matter.
4. Hold out one whole season at a time, train on the other ten, predict, repeat.
5. Rank games by |predicted margin| and hand out pick'em points 1..n to measure how useful the
   confidence ranking is.

## Data sources

| File | What | Source |
|---|---|---|
| `regular_season_games_2003_2013.csv` | regular-season game scores (stops mid December, before bowls) | sportsdataverse/cfbfastR-data on GitHub |
| `bowlGames.csv`, `teamNamesMerge.csv` | historical bowl results, team-name map | geogunow/CollegeFootballBowlPredictions on GitHub (built on lebebr01/cfbFootball) |
| `stats/` | teamrankings.com season stats, **only used in `leakage_check.py`** | same repo as above |

## Known limitations

- Only 356 games, so any accuracy number has roughly +/- 5 points of uncertainty.
- The richer teamrankings stats (yards, turnovers, sacks, ...) were scraped after the bowls, so
  they leak the result. We do not use them. `leakage_check.py` shows the evidence.
- Nothing about injuries, opt-outs, coaching changes or motivation.
- "Best model" was picked by CV accuracy, so the reported best number is slightly optimistic.
- The bowl file ends with the 2013 season, so there is no 2014+ evaluation.
