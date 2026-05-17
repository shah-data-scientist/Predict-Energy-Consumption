# Predict Energy Consumption — Seattle Building Benchmarking

**OpenClassrooms — Projet 3 | Data Science & Machine Learning**
**Author:** Shahul Shaik

---

## Project Goal

The City of Seattle aims to reach carbon neutrality by 2050. Non-residential buildings
represent a major share of municipal energy use and CO₂ emissions. Measuring their
consumption through field surveys is expensive and slow.

This project builds **regression models that estimate site energy use (kBtu) and GHG
emissions from structural building attributes alone** — floor area, age, use type,
energy mix — so city planners can prioritise retrofit candidates without costly surveys.

**Dataset:** Seattle 2016 Building Energy Benchmarking — 3,376 entries, 60+ variables.
Source: [City of Seattle Open Data Portal](https://data.seattle.gov).

---

## Notebook Map

Run in order. Each notebook is self-contained and fully executed.

| # | Notebook | Purpose |
|---|---|---|
| 01 | [`01_eda.ipynb`](notebooks/01_eda.ipynb) | Raw dataset overview — shape, types, distributions, key visual patterns |
| 02 | [`02_data_cleaning_and_features.ipynb`](notebooks/02_data_cleaning_and_features.ipynb) | Full cleaning pipeline and feature engineering → exports `data_modelisation.xlsx` |
| 03 | [`03_baseline_models.ipynb`](notebooks/03_baseline_models.ipynb) | Experiment B — benchmark all 7 models on 15 structural features |
| 04 | [`04_energy_star_analysis.ipynb`](notebooks/04_energy_star_analysis.ipynb) | Experiment A — performance ceiling when ENERGY STAR Score is available |
| 05 | [`05_final_model_and_results.ipynb`](notebooks/05_final_model_and_results.ipynb) | Experiments C & D — noise reduction, log transform, final recommendation |

---

## Key Results

### Dataset after cleaning

| Step | Count |
|---|---|
| Raw dataset | 3,376 buildings |
| After multifamily removal | 1,632 buildings |
| After flag-based outlier removal | 1,630 buildings |
| After target outlier capping (99th pct) | **1,596 buildings** |
| Final feature set | **15 structural features** |

### Features engineered

| Feature | Description |
|---|---|
| `Age` | `current year − YearBuilt` |
| `hasEnergyStarScore` | Binary flag — building has a certification score |
| `Ratio_LargestPropertyShare` | Share of GFA devoted to primary use type |
| `Ratio_ElectricityShare` | Electricity as share of total site energy |
| `EnergyMix` | Categorical — which energy sources a building uses (E / EN / SEN …) |
| `isMixedProperty` | Binary flag — more than one non-parking use type |

### Model performance — cross-experiment comparison (test set)

| Experiment | Features | Target transform | Best R² Energy | Best Model | Best R² GHG | Best Model |
|---|---|---|---|---|---|---|
| **A** — With ENERGY STAR Score | 16 (incl. score) | None | **0.888** | CatBoost | 0.811 | CatBoost |
| **B** — Full structural features | 15 | None | 0.783 | CatBoost | 0.695 | RandomForest |
| **C** — Noise reduction | 8 | None | 0.778 | RandomForest | **0.965** | RandomForest |
| **D** — Log-transformed targets | 8 | log1p | **0.844** | CatBoost | 0.957 | CatBoost |

> Experiment A is a performance ceiling — the ENERGY STAR Score is only available for
> ~66% of buildings and cannot be used in a city-wide deployable model.

### Deployable model recommendation

**Random Forest or CatBoost — Experiment D (log-transformed targets, 8 features)**

- Best energy R² among deployable experiments: **0.844** (CatBoost)
- Best GHG R² among deployable experiments: **0.965** (RandomForest, Exp C)
- Log transform reduces the effect of extreme-value buildings on the loss function
- 8-feature model is simpler, faster, and more robust than the 15-feature baseline

### Top predictors (feature importance — tuned Random Forest)

`LargestPropertyUseTypeGFA` · `Age` · `Ratio_ElectricityShare` · `NumberofFloors` ·
`LargestPropertyUseType` · `Ratio_LargestPropertyShare`

---

## Project Structure

```
Predict Energy Consumption/
├── data/
│   ├── raw/
│   │   ├── 2016_Building_Energy_Benchmarking.csv   # Source data (immutable)
│   │   └── Variable_Description.xlsx               # Field-level metadata
│   └── processed/
│       └── data_modelisation.xlsx                  # Cleaned dataset (output of 02)
├── notebooks/
│   ├── 01_eda.ipynb
│   ├── 02_data_cleaning_and_features.ipynb
│   ├── 03_baseline_models.ipynb
│   ├── 04_energy_star_analysis.ipynb
│   └── 05_final_model_and_results.ipynb
├── reports/
│   └── Seattle_Energy_Emissions_Modeling.pptx
├── models/                                         # Model artefacts (CatBoost info)
├── scripts/                                        # Build and validation scripts
├── pyproject.toml                                  # Python dependencies (Poetry)
└── README.md
```

---

## How to Run

**Option 1 — Poetry (recommended)**
```bash
cd "Predict Energy Consumption"
poetry install
poetry run jupyter notebook
```
Then open notebooks in order: `01_eda` → `02_data_cleaning_and_features` → `03_baseline_models` → `04_energy_star_analysis` → `05_final_model_and_results`.

**Option 2 — pip / venv**
```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements.txt
jupyter notebook
```

---

## Data

| File | Description |
|---|---|
| `data/raw/2016_Building_Energy_Benchmarking.csv` | Seattle 2016 benchmarking survey — 3,376 rows, 60+ columns |
| `data/raw/Variable_Description.xlsx` | Field-level metadata for all source columns |
| `data/processed/data_modelisation.xlsx` | Clean 1,596-row dataset exported by `02_data_cleaning_and_features.ipynb` |

---

## Modelling Details

### Models benchmarked

| Model | Type |
|---|---|
| `DummyRegressor` | Baseline (predict mean) |
| `LinearRegression` | OLS |
| `Ridge` | L2-regularised linear |
| `Lasso` | L1-regularised linear |
| `RandomForestRegressor` | Ensemble (bagging) |
| `GradientBoostingRegressor` | Ensemble (boosting) |
| `CatBoostRegressor` | Gradient boosting with categorical support |

### Pipeline

- Categorical columns → `OneHotEncoder(handle_unknown='ignore')`
- Numeric columns → `StandardScaler`
- Preprocessor built dynamically from column dtypes via `build_preprocessor(X)`
- Each target (energy, GHG) trained independently
- Hyperparameter tuning: `RandomizedSearchCV` (10 iterations, 3-fold CV) on Random Forest

### Experiments

| Label | Description |
|---|---|
| **Exp A** | 1,058 buildings that have an ENERGY STAR Score — upper performance bound |
| **Exp B** | All 1,596 buildings, 15 structural features, no transform |
| **Exp C** | 7 noisy/low-importance features dropped; energy added as GHG predictor |
| **Exp D** | Same as C but targets log1p-transformed; back-transformed for reporting |

---

## Dependencies

| Package | Purpose |
|---|---|
| `pandas`, `numpy` | Data manipulation |
| `scikit-learn` | Preprocessing, models, evaluation |
| `catboost` | Gradient boosting with native categorical support |
| `matplotlib`, `seaborn` | Visualisation |
| `openpyxl` | Excel I/O |
| `jupyter` | Notebook execution |

See [`pyproject.toml`](pyproject.toml) for pinned versions.
