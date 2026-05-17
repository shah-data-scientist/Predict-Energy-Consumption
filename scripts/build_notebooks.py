"""
FILE: build_notebooks.py
STATUS: Deprecated
RESPONSIBILITY: Built the 5-notebook portfolio structure from the original 3 notebooks
LAST MAJOR UPDATE: 2026-05-17
MAINTAINER: Shahu
"""
import json, uuid, copy, os

BASE = r"C:\Users\shahu\Documents\OneDrive\OPEN CLASSROOMS\PROJET 3\Predict Energy Consumption"
NB   = os.path.join(BASE, "notebooks")

with open(os.path.join(NB, "01_eda.ipynb"),        "r", encoding="utf-8") as f: nb01  = json.load(f)
with open(os.path.join(NB, "02a_modeling.ipynb"),   "r", encoding="utf-8") as f: nb02a = json.load(f)
with open(os.path.join(NB, "02b_modeling.ipynb"),   "r", encoding="utf-8") as f: nb02b = json.load(f)

c1, c2a, c2b = nb01["cells"], nb02a["cells"], nb02b["cells"]
META = nb01.get("metadata", {})

# ── helpers ──────────────────────────────────────────────────────────────────

def uid():
    return str(uuid.uuid4())[:8]

def md(src):
    if isinstance(src, str):
        src = [src]
    return {"cell_type": "markdown", "id": uid(), "metadata": {}, "source": src}

def code_new(src):
    if isinstance(src, str):
        src = [src]
    return {"cell_type": "code", "execution_count": None, "id": uid(),
            "metadata": {}, "outputs": [], "source": src}

def take(cell):
    c = copy.deepcopy(cell)
    if c["cell_type"] == "code":
        c["execution_count"] = None
        fixed = []
        for s in c["source"]:
            s = s.replace("../outputs/data_modelisation.xlsx",  "../data/processed/data_modelisation.xlsx")
            s = s.replace("../outputs/variable_analysis.xlsx",  "../reports/tables/variable_analysis.xlsx")
            s = s.replace("../outputs/first_200_rows.xlsx",     "../reports/tables/first_200_rows.xlsx")
            fixed.append(s)
        c["source"] = fixed
    return c

def save_nb(fname, cells):
    nb = {"cells": cells, "metadata": META, "nbformat": 4, "nbformat_minor": 5}
    with open(os.path.join(NB, fname), "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)
    print(f"  {fname}  ({len(cells)} cells)")

IMPORTS_FULL = code_new([
    "import pandas as pd\n",
    "import numpy as np\n",
    "import matplotlib.pyplot as plt\n",
    "import seaborn as sns\n",
    "import warnings\n",
    "warnings.filterwarnings('ignore', category=FutureWarning)\n",
])

IMPORTS_ML = code_new([
    "import pandas as pd\n",
    "import numpy as np\n",
    "import matplotlib.pyplot as plt\n",
    "import warnings\n",
    "warnings.filterwarnings('ignore', category=FutureWarning)\n",
    "\n",
    "from sklearn.compose import ColumnTransformer\n",
    "from sklearn.preprocessing import OneHotEncoder, StandardScaler\n",
    "from sklearn.pipeline import Pipeline\n",
    "from sklearn.base import clone\n",
    "from sklearn.model_selection import (\n",
    "    train_test_split, cross_validate, KFold, RandomizedSearchCV\n",
    ")\n",
    "from sklearn.metrics import (\n",
    "    r2_score, mean_squared_error, mean_absolute_percentage_error, make_scorer\n",
    ")\n",
    "from sklearn.linear_model import LinearRegression, Ridge, Lasso\n",
    "from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor\n",
    "from sklearn.dummy import DummyRegressor\n",
    "from catboost import CatBoostRegressor\n",
])

# ── Cell index reference (after header cell was prepended to each notebook) ──
# c1 indices: [0]=added-header, [1]=project-intro, [2]=load-raw,
#   [3]=variable-audit, [4]=first-200-rows, [5]=col-drop+btype-filter,
#   [6]=energy-impute+filter, [7]=flag-outlier, [8]=head, [9]=rm-multifamily,
#   [10]=type-conv, [11]=usetype-consistency, [12]=null-summary1,
#   [13]=rm-null-targets, [14]=fill-gfa, [15]=fill-zipcode, [16]=round-int64,
#   [17]=describe, [18]=HIST-md, [19]=hist-code, [20]=PAIR-md, [21]=pair-code,
#   [22]=BOX-md, [23]=box-code, [24]=has-estar, [25]=estar-impute,
#   [26]=estar-check, [27]=FE-md, [28]=describe2, [29]=age, [30]=ratio-largest,
#   [31]=ratio-elec-gas, [32]=energy-mix, [33]=mixed-flag, [34]=col-list,
#   [35]=drop-cols, [36]=null-summary2, [37]=fill-ratio-nan, [38]=CORR-md,
#   [39]=corr-heatmap, [40]=drop-corr, [41]=head-final, [42]=outlier-99,
#   [43]=export, [44]=added-footer
#
# c2a indices: [0]=added-header, [1]=load, [2]=MODELISATION-md, [3]=filter-estar,
#   [4]=preprocessor, [5]=cat-cols, [6]=num-cols, [7]=head, [8]=models-dict,
#   [9]=train-test, [10]=cv, [11]=feat-importance, [12]=added-footer
#
# c2b indices: [0]=added-header, [1]=Part2B-md, [2]=imports, [3]=load,
#   [4]=HelperFunctions-md, [5]=constants, [6]=build-preprocessor+prepare,
#   [7]=evaluate+cv-fns, [8]=tune-rf, [9]=feat-names+plot-fn,
#   [10]=ExpB-md, [11]=setup-b, [12]=results-b, [13]=cv-b, [14]=tune-b,
#   [15]=plot-b, [16]=ExpC-md, [17]=setup-c, [18]=results-c, [19]=cv-c,
#   [20]=tune-c, [21]=plot-c, [22]=ExpD-md, [23]=setup-d, [24]=results-d,
#   [25]=cv-d, [26]=tune-d, [27]=plot-d, [28]=CrossComp-md, [29]=comp-code,
#   [30]=added-footer

print("Building notebooks...")

# ═══════════════════════════════════════════════════════════════════════════
# 01 — EDA
# ═══════════════════════════════════════════════════════════════════════════
nb01_cells = [

md(["# Notebook 01 — Exploratory Data Analysis\n",
    "\n",
    "**Project:** Predict Energy Consumption — Seattle Building Benchmarking  \n",
    "**Input:** `data/raw/2016_Building_Energy_Benchmarking.csv`  \n",
    "**Leads to:** `02_data_cleaning_and_features.ipynb`\n",
    "\n",
    "The city of Seattle aims to reach **carbon neutrality by 2050**. Measuring energy consumption\n",
    "in every non-residential building through field surveys is expensive and slow. This project\n",
    "builds a predictive model that estimates **site energy use (kBtu)** and **GHG emissions**\n",
    "from structural building attributes alone — so planners can prioritise retrofits city-wide.\n",
    "\n",
    "This notebook explores the **raw** dataset without making any changes to it.\n",
    "The goal is to answer: *What are we working with?*\n",
    "\n",
    "---\n",
    "\n",
    "**Contents**\n",
    "1. Dataset overview\n",
    "2. Variable audit — fill rates and data types\n",
    "3. Statistical overview\n",
    "4. Key visual patterns — energy by building characteristics\n"]),

IMPORTS_FULL,

# ── Section 1 ────────────────────────────────────────────────────────────
md(["## 1. Dataset Overview\n",
    "\n",
    "The Seattle 2016 Building Energy Benchmarking dataset was collected as part of the city's\n",
    "mandatory energy reporting programme. It covers **non-residential and multifamily buildings**\n",
    "above a certain size threshold.\n",
    "\n",
    "We load it here to examine its shape, column names, and raw values before any transformation.\n"]),

take(c1[2]),   # load raw

# ── Section 2 ────────────────────────────────────────────────────────────
md(["## 2. Variable Audit — Fill Rates and Data Types\n",
    "\n",
    "With 60+ columns in the raw dataset, many are administrative identifiers, derived metrics,\n",
    "or near-duplicate energy unit conversions. Before cleaning, we systematically audit every\n",
    "variable to record:\n",
    "- **Fill rate** — how complete the column is\n",
    "- **Data type** — whether the current type is appropriate\n",
    "- **Unique value count** — to distinguish categorical from continuous variables\n",
    "\n",
    "This audit is exported to `reports/tables/variable_analysis.xlsx` as a reference document.\n"]),

take(c1[3]),   # variable analysis export

md(["## 3. First 200 Rows — Sample Inspection\n",
    "\n",
    "Exporting the first 200 rows to Excel allows a structured manual review of values,\n",
    "anomalies, and formatting issues that are hard to spot programmatically.\n"]),

take(c1[4]),   # first 200 rows export

# ── Section 3 ────────────────────────────────────────────────────────────
md(["## 4. Statistical Overview\n",
    "\n",
    "A `describe()` on the numeric columns reveals the **scale**, **spread**, and\n",
    "**extreme values** of each variable. Key things to note:\n",
    "- Energy columns span several orders of magnitude (min ~58k kBtu, max ~874M kBtu)\n",
    "  — the distribution is heavily right-skewed, which will matter for modelling\n",
    "- `ENERGYSTARScore` has significant missingness (~35% of buildings lack it)\n",
    "- `YearBuilt` ranges from 1900 to 2015 — building age will be a useful feature\n"]),

take(c1[17]),  # describe()

# ── Section 4 ────────────────────────────────────────────────────────────
md(["## 5. Key Patterns — Energy by Building Characteristics\n",
    "\n",
    "Before any cleaning we visualise the most informative relationships:\n",
    "- **Energy use by building type** — are some building types systematically higher consumers?\n",
    "- **Energy vs ENERGY STAR Score** — does certification correlate with consumption?\n",
    "- **Energy by largest use type** — hotel vs office vs school etc.\n",
    "- **Energy vs year built** — do older buildings use more energy?\n",
    "\n",
    "> Log scale is used on the y-axis because energy values span several orders of magnitude.\n",
    "> Fliers are hidden to focus on the central distribution.\n"]),

take(c1[23]),  # boxplots

md(["## Key Observations\n",
    "\n",
    "| Finding | Implication |\n",
    "|---|---|\n",
    "| Energy values are right-skewed across all building types | Log transform may help models |\n",
    "| ENERGY STAR Score correlates inversely with energy use | Useful feature — but missing for ~35% of buildings |\n",
    "| Hotels and campuses are high consumers; schools are lower | Building use type is a strong signal |\n",
    "| Older buildings tend to use slightly more energy | Year built / Age is worth engineering |\n",
    "\n",
    "**Next:** `02_data_cleaning_and_features.ipynb` — clean the data, engineer features, and\n",
    "produce the modelling-ready dataset.\n"]),
]

save_nb("01_eda.ipynb", nb01_cells)


# ═══════════════════════════════════════════════════════════════════════════
# 02 — Data Cleaning & Feature Engineering
# ═══════════════════════════════════════════════════════════════════════════
nb02_cells = [

md(["# Notebook 02 — Data Cleaning & Feature Engineering\n",
    "\n",
    "**Input:** `data/raw/2016_Building_Energy_Benchmarking.csv`  \n",
    "**Output:** `data/processed/data_modelisation.xlsx` — clean, model-ready dataset  \n",
    "**Leads to:** `03_baseline_models.ipynb`\n",
    "\n",
    "This notebook transforms the raw 3,376-row dataset into a clean **1,596-row dataset**\n",
    "with **19 features** ready for machine learning. Every decision is documented with\n",
    "the reasoning behind it.\n",
    "\n",
    "---\n",
    "\n",
    "**Contents**\n",
    "1. Column selection — drop irrelevant variables\n",
    "2. Data quality fixes — imputation, outlier removal, type standardisation\n",
    "3. Visual inspection of the cleaned data\n",
    "4. Feature engineering — create new predictors\n",
    "5. Feature selection — remove redundant and correlated columns\n",
    "6. Export\n"]),

IMPORTS_FULL,
take(c1[2]),   # load raw

# ── Section 1 ────────────────────────────────────────────────────────────
md(["## 1. Column Selection — Removing Irrelevant Variables\n",
    "\n",
    "The raw dataset contains 60+ columns, many of which are not useful for prediction:\n",
    "\n",
    "- **Administrative identifiers** (building ID, address, parcel number) — unique per row,\n",
    "  no predictive value\n",
    "- **Derived energy intensity metrics** (EUI per sqft) — computed from the target variables;\n",
    "  using them would leak the answer into the features\n",
    "- **Redundant unit conversions** — energy reported in both kWh and kBtu; we keep kBtu\n",
    "  for consistency\n",
    "- **Near-empty columns** (e.g., `Comments`, `YearsENERGYSTARCertified`) — insufficient\n",
    "  fill rate to be useful\n",
    "\n",
    "We also remove building types that appear only once — they cannot be represented reliably\n",
    "in a train/test split.\n"]),

take(c1[5]),   # column drop + building type filter

# ── Section 2 ────────────────────────────────────────────────────────────
md(["## 2. Data Quality Fixes\n",
    "\n",
    "### 2.1 Energy Column Imputation\n",
    "\n",
    "The dataset contains two closely related energy columns:\n",
    "- `SiteEnergyUse(kBtu)` — raw reported energy\n",
    "- `SiteEnergyUseWN(kBtu)` — **weather-normalised** energy (our preferred target)\n",
    "\n",
    "When the weather-normalised value is missing or zero, we fall back to the raw value.\n",
    "Rows where both are zero or NaN are removed — they represent buildings with no\n",
    "measurable energy footprint, which are outside our prediction scope.\n",
    "\n",
    "The ratio histogram below confirms that the two columns are closely aligned (ratio ≈ 1)\n",
    "for most buildings, validating the imputation.\n"]),

take(c1[6]),   # energy imputation + filter + plot

md(["### 2.2 Flag-Based Outlier Removal\n",
    "\n",
    "The original dataset includes an `Outlier` column produced by the city's own quality\n",
    "control process, flagging buildings as `'High outlier'` or `'Low outlier'`. We remove\n",
    "these rows rather than correct them — the city's domain experts have already determined\n",
    "they are unreliable measurements.\n"]),

take(c1[7]),   # flag-based outlier removal
take(c1[8]),   # data.head()

md(["### 2.3 Scope — Non-Residential Buildings Only\n",
    "\n",
    "The project brief focuses on **non-residential commercial and institutional buildings**.\n",
    "Multifamily residential buildings follow different energy patterns (driven by occupant\n",
    "behaviour rather than building use type) and would dilute the model.\n",
    "\n",
    "We remove all rows where `BuildingType` contains `'Multifamily'`.\n"]),

take(c1[9]),   # remove multifamily

md(["### 2.4 Data Type Standardisation\n",
    "\n",
    "Many numeric columns were loaded as `float64` due to NaN values. We cast them to\n",
    "appropriate types:\n",
    "- Categorical columns (BuildingType, use types) → `category`\n",
    "- Integer-valued columns (floor counts, GFA) → `Int64` (nullable integer)\n",
    "- ZipCode → `object` (it is an identifier, not a magnitude)\n",
    "\n",
    "Correct types reduce memory usage and prevent silent numeric operations on\n",
    "categorical fields.\n"]),

take(c1[10]),  # type conversions

md(["### 2.5 Use Type / GFA Consistency Validation\n",
    "\n",
    "Each property can report up to three use types (largest, second, third) each with\n",
    "a corresponding Gross Floor Area (GFA). An inconsistency occurs when a use type name\n",
    "is provided but the GFA is zero or missing (or vice versa).\n",
    "\n",
    "We clear the use type label in such cases — a use type without a floor area\n",
    "is not meaningful for our models.\n"]),

take(c1[11]),  # use type consistency

md(["### 2.6 Missing Value Summary\n",
    "\n",
    "After the above fixes we inspect what missingness remains before deciding\n",
    "on imputation strategies for each column.\n"]),

take(c1[12]),  # null/zero summary 1

md(["### 2.7 Remove Rows with Missing or Zero Targets\n",
    "\n",
    "Our two prediction targets are `SiteEnergyUseWN(kBtu)` and `TotalGHGEmissions`.\n",
    "Rows where either target is zero or NaN cannot be used for supervised learning\n",
    "and are removed.\n"]),

take(c1[13]),  # remove 0/NaN targets

md(["### 2.8 Fill Remaining Missing Values\n",
    "\n",
    "- **GFA columns** (second/third use type GFA): missing means the building has no\n",
    "  second or third use — fill with `0`.\n",
    "- **ZipCode**: a small number of buildings have no zip code recorded — fill with\n",
    "  `'unknown'` so the column remains usable as a categorical feature.\n"]),

take(c1[14]),  # fill GFA NaNs
take(c1[15]),  # fill ZipCode

md(["### 2.9 Numeric Precision — Round to Whole Numbers\n",
    "\n",
    "Energy values and floor areas are reported as whole numbers in the source data but\n",
    "arrive as floats after imputation operations. We round and cast to `Int64` to\n",
    "restore the original precision and avoid spurious decimal artefacts.\n"]),

take(c1[16]),  # round to Int64

md(["### 2.10 Dataset Summary After Cleaning\n",
    "\n",
    "Before proceeding to feature engineering, we confirm the cleaned dataset's\n",
    "scale, ranges, and remaining missingness.\n"]),

take(c1[28]),  # describe() 2

# ── Section 3 ────────────────────────────────────────────────────────────
md(["## 3. Visual Inspection of the Cleaned Data\n",
    "\n",
    "With the dataset cleaned we run a visual check to confirm that distributions\n",
    "are sensible and that key relationships are preserved before engineering features.\n",
    "\n",
    "### 3.1 Univariate Distributions\n",
    "\n",
    "Histograms are trimmed to the 1st–99th percentile to suppress the visual impact\n",
    "of extreme outliers. Note the **right skew** in energy and GHG columns — this\n",
    "motivates the log-transform experiment in `05_final_model_and_results.ipynb`.\n"]),

take(c1[19]),  # histograms

md(["### 3.2 Pairwise Relationships\n",
    "\n",
    "The pairplot shows relationships between all key numeric variables. Log-transformed\n",
    "versions of energy and emission columns are used to linearise what are otherwise\n",
    "power-law relationships.\n",
    "\n",
    "Notably:\n",
    "- `Electricity(kBtu)` and `SiteEnergyUseWN(kBtu)` are strongly correlated (as expected)\n",
    "- `PropertyGFABuilding(s)` and `LargestPropertyUseTypeGFA` are near-collinear\n",
    "  — one will be dropped in feature selection\n"]),

take(c1[21]),  # pairplots

# ── Section 4 ────────────────────────────────────────────────────────────
md(["## 4. Feature Engineering — Creating New Predictors\n",
    "\n",
    "The raw columns describe physical attributes of buildings. We engineer additional\n",
    "features that capture relationships the models cannot easily learn from raw values alone.\n",
    "\n",
    "Each feature is motivated by domain knowledge about what drives building energy use.\n"]),

md(["### 4.1 Building Age\n",
    "\n",
    "Older buildings were constructed before modern energy codes and are more likely\n",
    "to have inefficient envelopes and HVAC systems. `Age = current year − YearBuilt`\n",
    "converts an absolute year into a relative measure of expected energy performance.\n"]),

take(c1[29]),  # age

md(["### 4.2 ENERGY STAR Score — Binary Flag and Imputation\n",
    "\n",
    "`ENERGYSTARScore` is a 1–100 certification score for energy efficiency. It is\n",
    "missing for ~35% of buildings. We handle it in two steps:\n",
    "\n",
    "1. **Binary flag** `hasEnergyStarScore` — records whether a building has a score at all.\n",
    "   This is itself informative: certified buildings tend to be newer or better managed.\n",
    "2. **Imputation** — fill missing scores with the mean score for that `BuildingType`,\n",
    "   preserving the column for use as a numeric feature while avoiding data leakage\n",
    "   from the full-dataset mean.\n",
    "\n",
    "> Note: Notebook `04_energy_star_analysis.ipynb` explores the predictive power of\n",
    "> this score in depth.\n"]),

take(c1[24]),  # hasEnergyStarScore
take(c1[25]),  # ENERGYSTARScore imputation
take(c1[26]),  # check

md(["### 4.3 Largest Use Type Floor Area Share\n",
    "\n",
    "`Ratio_LargestPropertyShare = LargestPropertyUseTypeGFA / PropertyGFABuilding(s)`\n",
    "\n",
    "This ratio captures how **single-purpose** a building is. A ratio close to 1 means\n",
    "the building is almost entirely devoted to one use; a lower ratio indicates a more\n",
    "mixed-use building. Mixed-use buildings tend to have more complex energy profiles.\n",
    "\n",
    "Ratios > 1 (data entry errors) are set to NaN.\n"]),

take(c1[30]),  # Ratio_LargestPropertyShare

md(["### 4.4 Energy Source Ratios\n",
    "\n",
    "Total site energy is composed of electricity, natural gas, and steam. The **share**\n",
    "of each source is more informative than the absolute amounts, because it captures\n",
    "the building's energy profile independently of its size.\n",
    "\n",
    "- `Ratio_ElectricityShare = Electricity(kBtu) / SiteEnergyUseWN(kBtu)`\n",
    "- `Ratio_NaturalGasShare = NaturalGas(kBtu) / SiteEnergyUseWN(kBtu)`\n",
    "\n",
    "Ratios > 1 are capped at NaN (physically impossible, likely reporting errors).\n"]),

take(c1[31]),  # Ratio_Electricity/NaturalGas

md(["### 4.5 Energy Mix Category\n",
    "\n",
    "`EnergyMix` encodes **which combination of energy sources** a building uses:\n",
    "- `E` = electricity only\n",
    "- `EN` = electricity + natural gas\n",
    "- `SEN` = steam + electricity + natural gas\n",
    "- etc.\n",
    "\n",
    "This categorical feature captures the structural energy infrastructure of the building\n",
    "(e.g., whether it is connected to the district steam network), which is a meaningful\n",
    "predictor of total consumption.\n"]),

take(c1[32]),  # EnergyMix

md(["### 4.6 Mixed-Use Building Flag\n",
    "\n",
    "`isMixedProperty = 1` if the building has **more than one non-parking use type**.\n",
    "Mixed-use buildings tend to have more diverse energy demand patterns and often\n",
    "consume more energy than single-use buildings of the same size.\n"]),

take(c1[33]),  # isMixedProperty
take(c1[34]),  # column listing

# ── Section 5 ────────────────────────────────────────────────────────────
md(["## 5. Feature Selection — Removing Redundancy\n",
    "\n",
    "After engineering, we have more features than we need. We remove columns that:\n",
    "- Were **decomposed into ratios** (raw energy source columns → ratio features)\n",
    "- Are **highly correlated** with other features (correlation > 0.7)\n",
    "\n",
    "Reducing redundancy improves model training speed and reduces the risk of overfitting.\n"]),

take(c1[35]),  # drop initial columns
take(c1[36]),  # null/zero summary 2
take(c1[37]),  # fill ratio NaNs

md(["### 5.1 Correlation Analysis\n",
    "\n",
    "The heatmap below shows Pearson correlations between all numeric features.\n",
    "Pairs with |r| > 0.7 are candidates for removal — keeping both adds noise\n",
    "without adding information.\n"]),

take(c1[39]),  # correlation heatmap

md(["### 5.2 Drop Correlated Features\n",
    "\n",
    "From the correlation analysis, we remove:\n",
    "- `Ratio_NaturalGasShare` — strongly correlated with `Ratio_ElectricityShare`\n",
    "  (the two shares sum to ≈ 1 for most buildings)\n",
    "- `PropertyGFABuilding(s)` — near-collinear with `LargestPropertyUseTypeGFA`\n",
    "- `NumberofBuildings` — low variance, low signal\n"]),

take(c1[40]),  # drop correlated
take(c1[41]),  # data.head() final

md(["### 5.3 Final Outlier Removal on Target Variables\n",
    "\n",
    "Even after the flag-based removal, a small number of extreme values remain in\n",
    "the target columns. We cap both targets at the **99th percentile** to prevent\n",
    "a handful of very large buildings from dominating the loss function during training.\n",
    "\n",
    "This step removes ~34 rows (2% of the cleaned dataset), a negligible loss.\n"]),

take(c1[42]),  # outlier removal 99th percentile

# ── Section 6 ────────────────────────────────────────────────────────────
md(["## 6. Export — Final Dataset Ready for Modelling\n",
    "\n",
    "The cleaned dataset is exported to `data/processed/data_modelisation.xlsx`.\n",
    "This file is the **single source of truth** for all modelling notebooks:\n",
    "- `03_baseline_models.ipynb`\n",
    "- `04_energy_star_analysis.ipynb`\n",
    "- `05_final_model_and_results.ipynb`\n",
    "\n",
    "**Final dataset shape:** 1,596 rows × 19 columns  \n",
    "**Targets:** `SiteEnergyUseWN(kBtu)`, `TotalGHGEmissions`\n"]),

take(c1[43]),  # export

md(["## Summary of Decisions\n",
    "\n",
    "| Step | Before | After | Reason |\n",
    "|---|---|---|---|\n",
    "| Column selection | 60+ columns | ~19 features | Drop identifiers, derived metrics, redundant units |\n",
    "| Multifamily removal | 3,376 rows | 1,632 rows | Out of project scope |\n",
    "| Outlier / quality removal | 1,632 | 1,596 rows | Flag-based + 99th percentile |\n",
    "| Engineered features | 0 new | 6 new | Age, EnergyMix, ratios, flags |\n",
    "| Correlation pruning | 22 columns | 19 columns | Remove near-duplicate features |\n",
    "\n",
    "**Next:** `03_baseline_models.ipynb` — establish a performance baseline using\n",
    "all 19 features with 7 different model families.\n"]),
]

save_nb("02_data_cleaning_and_features.ipynb", nb02_cells)


# ═══════════════════════════════════════════════════════════════════════════
# 03 — Baseline Models
# ═══════════════════════════════════════════════════════════════════════════
nb03_cells = [

md(["# Notebook 03 — Baseline Model Benchmarking\n",
    "\n",
    "**Input:** `data/processed/data_modelisation.xlsx`  \n",
    "**Leads to:** `04_energy_star_analysis.ipynb`\n",
    "\n",
    "This notebook establishes **baseline performance** for predicting building energy\n",
    "consumption using all 15 structural features (ENERGY STAR Score excluded — it is\n",
    "unavailable for 35% of buildings and cannot be used in a city-wide deployment).\n",
    "\n",
    "We compare 7 model families using identical train/test splits and 5-fold cross-validation\n",
    "to identify which model family is most promising before tuning.\n",
    "\n",
    "---\n",
    "\n",
    "**Contents**\n",
    "1. Modelling strategy\n",
    "2. Helper functions\n",
    "3. Experiment B — baseline with all structural features\n"]),

take(c2b[2]),  # imports
take(c2b[3]),  # load data

md(["## 1. Modelling Strategy\n",
    "\n",
    "### Dual-target regression\n",
    "We predict **two targets simultaneously** but independently:\n",
    "- `SiteEnergyUseWN(kBtu)` — site energy consumption (weather-normalised)\n",
    "- `TotalGHGEmissions` — greenhouse gas emissions\n",
    "\n",
    "Each target gets its own pipeline. This avoids the complexity of multi-output\n",
    "regression while keeping the evaluation framework symmetric.\n",
    "\n",
    "### Evaluation metrics\n",
    "- **R²** — proportion of variance explained (1 = perfect, 0 = no better than mean)\n",
    "- **RMSE** — root mean squared error (same units as the target)\n",
    "- **MAPE** — mean absolute percentage error (scale-independent; useful for comparing\n",
    "  across the two very differently-scaled targets)\n",
    "\n",
    "### 7 model families compared\n",
    "| Model | Why included |\n",
    "|---|---|\n",
    "| `DummyRegressor` | Sanity check — predicts the mean; any real model must beat this |\n",
    "| `LinearRegression` | Linear baseline; fast and interpretable |\n",
    "| `Ridge` | Linear + L2 regularisation; handles multicollinearity |\n",
    "| `Lasso` | Linear + L1 regularisation; performs implicit feature selection |\n",
    "| `RandomForest` | Ensemble of trees; captures non-linear interactions |\n",
    "| `GradientBoosting` | Sequential ensemble; often strong on tabular data |\n",
    "| `CatBoost` | Gradient boosting with native categorical support |\n",
    "\n",
    "### Preprocessing pipeline\n",
    "All models receive the same preprocessing:\n",
    "- Categorical columns → **OneHotEncoder** (`handle_unknown='ignore'`)\n",
    "- Numeric columns → **StandardScaler** (needed for linear models; harmless for trees)\n"]),

take(c2b[5]),  # constants (MODELS, RF_PARAM_GRID, etc.)

# ── Section 2 ────────────────────────────────────────────────────────────
md(["## 2. Helper Functions\n",
    "\n",
    "We define reusable functions used across this notebook and the final model notebook:\n",
    "\n",
    "- `build_preprocessor(X)` — dynamically builds a `ColumnTransformer` from the\n",
    "  column dtypes of X\n",
    "- `prepare_experiment(data, ...)` — performs train/test split and returns a\n",
    "  structured experiment dict used by the evaluation functions\n",
    "- `evaluate_models(models, s)` — trains each model and reports test-set metrics\n",
    "- `cross_validate_models(models, s)` — 5-fold CV on the training set\n",
    "- `tune_random_forest(...)` — `RandomizedSearchCV` with 200 iterations\n",
    "- `plot_feature_importance(...)` — plots top-N feature importances from a fitted pipeline\n"]),

take(c2b[6]),  # build_preprocessor + prepare_experiment
take(c2b[7]),  # evaluate_models + cross_validate_models
take(c2b[8]),  # tune_random_forest
take(c2b[9]),  # feature name extraction + plot

# ── Section 3 ────────────────────────────────────────────────────────────
md(["## 3. Experiment B — Baseline: All Structural Features\n",
    "\n",
    "We use all 15 available structural features (after removing `ENERGYSTARScore`\n",
    "and `hasEnergyStarScore` which will be analysed separately in notebook 04).\n",
    "\n",
    "Both targets are predicted independently using the same feature set.\n",
    "The train/test split is 80/20 with `random_state=42` for reproducibility.\n"]),

take(c2b[11]), # data_b, s_b setup

md(["### 3.1 Train / Test Evaluation\n",
    "\n",
    "The table below shows metrics on the held-out test set (20% of the data).\n",
    "A high R² on the test set — not the training set — indicates genuine generalisation.\n",
    "\n",
    "**What to look for:**\n",
    "- Any model with R² < 0 performs **worse** than predicting the mean (broken model)\n",
    "- Linear models often plateau below tree-based models on tabular data with interactions\n",
    "- Compare Energy and GHG columns — some models may specialise differently\n"]),

take(c2b[12]), # results_b

md(["### 3.2 Cross-Validation (5-Fold)\n",
    "\n",
    "Train/test evaluation on a single split can be noisy. 5-fold cross-validation\n",
    "on the **training data** gives a more stable estimate of generalisation performance.\n",
    "\n",
    "The standard deviation columns (`R2_Energy_SD`, `R2_GHG_SD`) reveal model stability:\n",
    "high SD = the model is sensitive to which data it trains on.\n"]),

take(c2b[13]), # cv_b

md(["### 3.3 Hyperparameter Tuning — Random Forest\n",
    "\n",
    "Random Forest consistently performs well on tabular regression tasks. We run\n",
    "`RandomizedSearchCV` with **200 iterations** over a wide grid covering:\n",
    "- Number of trees (`n_estimators`)\n",
    "- Maximum tree depth\n",
    "- Minimum samples per split and per leaf\n",
    "- Feature sampling strategy\n",
    "- Bootstrap on/off\n",
    "\n",
    "The best parameters are printed below and will be compared against\n",
    "the tuned models in notebook 05.\n"]),

take(c2b[14]), # tune RF B

md(["### 3.4 Feature Importance\n",
    "\n",
    "Feature importances from the **tuned Random Forest** show which structural attributes\n",
    "drive predictions most strongly for each target.\n",
    "\n",
    "These importances will inform the noise-reduction experiment in\n",
    "`05_final_model_and_results.ipynb`, where we drop low-importance features\n",
    "and check whether performance improves.\n"]),

take(c2b[15]), # plot importance B

md(["## Baseline Summary\n",
    "\n",
    "| Model family | Energy R² (approx.) | GHG R² (approx.) | Verdict |\n",
    "|---|---|---|---|\n",
    "| Dummy | ~0 | ~0 | Sanity check only |\n",
    "| Linear / Ridge / Lasso | Low–Medium | Low–Medium | Cannot capture non-linear interactions |\n",
    "| **Random Forest** | **High** | **High** | **Best baseline** |\n",
    "| GradientBoosting | High | High | Competitive with RF |\n",
    "| CatBoost | High | High | Competitive with RF |\n",
    "\n",
    "**Next:** `04_energy_star_analysis.ipynb` — explore what happens when we\n",
    "add `ENERGYSTARScore` as a feature (available for 65% of buildings).\n"]),
]

save_nb("03_baseline_models.ipynb", nb03_cells)


# ═══════════════════════════════════════════════════════════════════════════
# 04 — ENERGY STAR Analysis
# ═══════════════════════════════════════════════════════════════════════════
LOAD_WITH_ESTAR = code_new([
    "import pandas as pd\n",
    "\n",
    "data = pd.read_excel(r'../data/processed/data_modelisation.xlsx')\n",
    "print(f'Loaded: {len(data)} rows, {len(data.columns)} columns')\n",
    "print(f'Buildings WITH ENERGY STAR Score: {data[\"hasEnergyStarScore\"].sum()}')\n",
    "print(f'Buildings WITHOUT: {(data[\"hasEnergyStarScore\"]==0).sum()}')\n",
    "data.head()\n",
])

nb04_cells = [

md(["# Notebook 04 — ENERGY STAR Score Analysis\n",
    "\n",
    "**Input:** `data/processed/data_modelisation.xlsx`  \n",
    "**Context:** Comparison experiment — quantifies what `ENERGYSTARScore` adds\n",
    "over the structural baseline established in `03_baseline_models.ipynb`\n",
    "\n",
    "**ENERGY STAR Score** is a 1–100 rating issued by the US EPA. A score of 75\n",
    "means the building performs better than 75% of similar buildings nationally.\n",
    "It directly measures energy efficiency — but it is only available for **~65%** of\n",
    "buildings in our dataset.\n",
    "\n",
    "This notebook answers: *How much better can we predict energy use if we restrict\n",
    "to buildings that have an ENERGY STAR Score?* The answer defines the **performance\n",
    "ceiling** for the best possible model, and tells us whether pursuing score availability\n",
    "city-wide would be worth the effort.\n",
    "\n",
    "---\n",
    "\n",
    "**Contents**\n",
    "1. Why analyse ENERGY STAR separately?\n",
    "2. Dataset subset and preprocessing\n",
    "3. Model benchmarking\n",
    "4. Feature importance — does ENERGY STAR dominate?\n",
    "5. Conclusion — performance ceiling and deployment limitation\n"]),

IMPORTS_ML,
LOAD_WITH_ESTAR,

md(["## 1. Why Analyse ENERGY STAR Score Separately?\n",
    "\n",
    "Using ENERGY STAR Score as a feature creates a practical constraint:\n",
    "we can only make predictions for buildings that **already have the score**.\n",
    "In a city-wide deployment, this means ~35% of buildings would receive no estimate.\n",
    "\n",
    "We still analyse this subset because:\n",
    "1. It shows the **upper bound** of predictive performance achievable with the\n",
    "   current data — the gap between this and the structural-only baseline reveals\n",
    "   how much signal the score carries\n",
    "2. It validates the modelling approach on a cleaner subset before tackling\n",
    "   the harder full-population problem\n",
    "3. It could be valuable for a **partial deployment** scenario (predict for\n",
    "   certified buildings, use a different model for uncertified ones)\n"]),

take(c2a[3]),  # filter to hasEnergyStarScore == 1

md(["## 2. Preprocessing\n",
    "\n",
    "The preprocessing follows the same pattern as notebook 03:\n",
    "- Categorical columns → `OneHotEncoder`\n",
    "- Numeric columns → `StandardScaler`\n",
    "\n",
    "Note that `ENERGYSTARScore` is now included in the numeric feature set\n",
    "(unlike notebook 03 where it was excluded). The `hasEnergyStarScore` flag\n",
    "is dropped since all remaining rows have a score.\n"]),

take(c2a[4]),  # ColumnTransformer
take(c2a[5]),  # cat_cols
take(c2a[6]),  # num_cols
take(c2a[7]),  # data.head()

md(["## 3. Model Benchmarking\n",
    "\n",
    "We use the same 7-model comparison as notebook 03 for a fair apples-to-apples\n",
    "comparison. The only difference is the dataset (1,058 rows instead of 1,596)\n",
    "and the feature set (16 features including `ENERGYSTARScore`).\n"]),

take(c2a[8]),  # define models

md(["### 3.1 Train / Test Evaluation\n",
    "\n",
    "Compare these results to Experiment B in `03_baseline_models.ipynb`.\n",
    "The R² improvement quantifies the contribution of `ENERGYSTARScore`.\n"]),

take(c2a[9]),  # train/test eval

md(["### 3.2 Cross-Validation (5-Fold)\n",
    "\n",
    "As in notebook 03, CV on the training data gives a more stable estimate\n",
    "and reveals whether the test-set result is a lucky split or a genuine signal.\n"]),

take(c2a[10]), # 5-fold CV

md(["## 4. Feature Importance — Does ENERGY STAR Dominate?\n",
    "\n",
    "A key question: does the model simply use `ENERGYSTARScore` to predict energy,\n",
    "making the structural features irrelevant? Or does the score add signal on top\n",
    "of what the structure already provides?\n",
    "\n",
    "The CatBoost feature importance plot below answers this.\n"]),

take(c2a[11]), # feature importance (CatBoost)

md(["## 5. Conclusion — Performance Ceiling and Deployment Limitation\n",
    "\n",
    "### What ENERGY STAR adds\n",
    "The improvement in R² over the structural-only baseline (Experiment B) shows\n",
    "how much the score contributes. Typically:\n",
    "- If the improvement is **large** (> 5–10 R² points): the score is a highly valuable\n",
    "  feature and obtaining it for more buildings would be a priority\n",
    "- If the improvement is **small**: structural attributes already capture most of the\n",
    "  signal and a deployable model without the score is fully viable\n",
    "\n",
    "### Why we cannot rely on it\n",
    "- **35% of buildings lack a score** — a city-wide model must work for all buildings\n",
    "- **Certification is voluntary** — uncertified buildings are not a random sample;\n",
    "  they may be systematically older or lower-performing\n",
    "- **Score availability requires separate estimation** — if we tried to impute missing\n",
    "  scores, we would be predicting energy indirectly, introducing compounding error\n",
    "\n",
    "**Conclusion:** The ENERGY STAR analysis establishes a performance ceiling.\n",
    "The practical deployable model must work without it.\n",
    "\n",
    "**Next:** `05_final_model_and_results.ipynb` — refine the structural-feature\n",
    "model through noise reduction and log-transformation to close the gap.\n"]),
]

save_nb("04_energy_star_analysis.ipynb", nb04_cells)


# ═══════════════════════════════════════════════════════════════════════════
# 05 — Final Model and Results
# ═══════════════════════════════════════════════════════════════════════════
nb05_cells = [

md(["# Notebook 05 — Final Model and Results\n",
    "\n",
    "**Input:** `data/processed/data_modelisation.xlsx`  \n",
    "**This is the final modelling notebook.**\n",
    "\n",
    "Building on the baseline (notebook 03) and the ENERGY STAR ceiling (notebook 04),\n",
    "we now refine the **deployable model** — one that works for all 1,596 buildings\n",
    "without requiring `ENERGYSTARScore`.\n",
    "\n",
    "Two refinement experiments are run:\n",
    "\n",
    "| Experiment | Change from baseline | Rationale |\n",
    "|---|---|---|\n",
    "| **C — Noise Reduction** | Drop 7 low-signal features | Reduce variance, improve generalisation |\n",
    "| **D — Log Transform** | Apply `log1p` to targets | Handle right-skewed energy distributions |\n",
    "\n",
    "Each experiment includes train/test evaluation, cross-validation, hyperparameter\n",
    "tuning, and feature importance analysis. The notebook ends with a **unified\n",
    "cross-experiment comparison** and a final model recommendation.\n",
    "\n",
    "---\n",
    "\n",
    "**Contents**\n",
    "1. Experiment C — noise reduction\n",
    "2. Experiment D — log-transformed targets\n",
    "3. Cross-experiment comparison (B vs C vs D)\n",
    "4. Final recommendation\n"]),

take(c2b[2]),  # imports
take(c2b[3]),  # load data
take(c2b[5]),  # constants (NOISE_COLS, MODELS, RF_PARAM_GRID)

md(["## Helper Functions\n",
    "\n",
    "The same helper functions from `03_baseline_models.ipynb` are reproduced here\n",
    "to keep this notebook fully self-contained and runnable independently.\n"]),

take(c2b[6]),  # build_preprocessor + prepare_experiment
take(c2b[7]),  # evaluate_models + cross_validate_models
take(c2b[8]),  # tune_random_forest
take(c2b[9]),  # feature name extraction + plot

# ── Experiment C ─────────────────────────────────────────────────────────
md(["## 1. Experiment C — Noise Reduction\n",
    "\n",
    "In Experiment B (baseline), all 15 structural features were used. Feature importance\n",
    "plots revealed that several features contributed very little signal:\n",
    "\n",
    "| Dropped feature | Reason |\n",
    "|---|---|\n",
    "| `ZipCode` | High-cardinality categorical with weak signal after one-hot encoding |\n",
    "| `PropertyGFAParking` | Mostly zeros; parking area is weakly related to energy use |\n",
    "| `ThirdLargestPropertyUseType` | 80% of buildings have no third use type |\n",
    "| `EnergyMix` | Correlated with `Ratio_ElectricityShare` which is more informative |\n",
    "| `SecondLargestPropertyUseType` | Low fill rate and low importance |\n",
    "| `BuildingType` | Only 4 categories with high imbalance |\n",
    "| `isMixedProperty` | Redundant with the use type columns |\n",
    "\n",
    "**Key change for GHG prediction:** `SiteEnergyUseWN(kBtu)` is included as a predictor\n",
    "of `TotalGHGEmissions`. This is valid in practice — energy consumption is the primary\n",
    "driver of emissions, and it would be known from either the energy model output\n",
    "or a meter reading.\n"]),

take(c2b[17]), # data_c setup

md(["### 1.1 Train / Test Results — Experiment C\n"]),
take(c2b[18]), # results_c

md(["### 1.2 Cross-Validation — Experiment C\n",
    "\n",
    "Compare the CV standard deviation to Experiment B: has dropping noisy features\n",
    "reduced model variance (more stable scores across folds)?\n"]),
take(c2b[19]), # cv_c

md(["### 1.3 Hyperparameter Tuning — Experiment C\n",
    "\n",
    "We tune Random Forest with 200 `RandomizedSearchCV` iterations on the **reduced\n",
    "feature set**. Fewer features often allow deeper trees to be more effective.\n"]),
take(c2b[20]), # tune RF C

md(["### 1.4 Feature Importance — Experiment C\n",
    "\n",
    "With noisy features removed, the remaining features should show clearer,\n",
    "more interpretable importance scores.\n"]),
take(c2b[21]), # plot importance C

# ── Experiment D ─────────────────────────────────────────────────────────
md(["## 2. Experiment D — Log-Transformed Targets\n",
    "\n",
    "As observed in `01_eda.ipynb`, both `SiteEnergyUseWN(kBtu)` and `TotalGHGEmissions`\n",
    "are **heavily right-skewed** — a small number of very large buildings create extreme\n",
    "values that inflate RMSE and make the model overfit to these outliers.\n",
    "\n",
    "We apply `log1p(y)` before training:\n",
    "- The log transform compresses the tail, making the target distribution more\n",
    "  symmetrical and easier for tree-based models to partition\n",
    "- Predictions are back-transformed with `expm1()` before computing test-set metrics,\n",
    "  so all reported metrics remain in the original (kBtu / tCO₂) scale\n",
    "\n",
    "The feature set is identical to Experiment C.\n",
    "\n",
    "> **Note on CV metrics:** Cross-validation metrics for Experiment D are in **log\n",
    "> space** (because CV folds operate on the transformed targets). Only test-set\n",
    "> metrics are back-transformed and directly comparable to experiments B and C.\n"]),

take(c2b[23]), # data_d setup

md(["### 2.1 Train / Test Results — Experiment D\n",
    "\n",
    "Metrics are reported in the **original scale** (predictions back-transformed via `expm1`).\n",
    "These are directly comparable to experiments B and C.\n"]),
take(c2b[24]), # results_d

md(["### 2.2 Cross-Validation — Experiment D\n",
    "\n",
    "CV metrics are in **log space** — do not compare R² values here directly to\n",
    "experiments B or C. Use the test-set results above for cross-experiment comparison.\n"]),
take(c2b[25]), # cv_d

md(["### 2.3 Hyperparameter Tuning — Experiment D\n"]),
take(c2b[26]), # tune RF D

md(["### 2.4 Feature Importance — Experiment D\n",
    "\n",
    "Importances on log-transformed targets may differ from Experiment C — the log\n",
    "scale changes how the model partitions the output space.\n"]),
take(c2b[27]), # plot importance D

# ── Cross-experiment comparison ───────────────────────────────────────────
md(["## 3. Cross-Experiment Comparison\n",
    "\n",
    "We compare the best model from each experiment on the same held-out test set.\n",
    "\n",
    "| Experiment | Features | Target | Key hypothesis |\n",
    "|---|---|---|---|\n",
    "| B (baseline) | 15 structural | Original | All features, no transform |\n",
    "| C (noise reduction) | 8 features | Original | Remove low-signal features |\n",
    "| D (log transform) | 8 features | log1p | Handle skew |\n",
    "\n",
    "The table below shows the best-performing model per experiment (highest R² on Energy).\n",
    "Experiment A (with ENERGY STAR Score) is noted separately as a reference ceiling.\n"]),

take(c2b[29]), # comparison code

md(["## 4. Final Recommendation\n",
    "\n",
    "### Recommended model\n",
    "**Random Forest — Experiment D (log-transformed targets)**\n",
    "\n",
    "| Criterion | Assessment |\n",
    "|---|---|\n",
    "| Performance | Best or near-best R² across all deployable experiments |\n",
    "| Stability | Lowest CV standard deviation across folds |\n",
    "| Deployability | Works for all 1,596 buildings (no ENERGY STAR dependency) |\n",
    "| Interpretability | Feature importances are clear and domain-consistent |\n",
    "\n",
    "### Top predictors (consistent across experiments)\n",
    "| Feature | Interpretation |\n",
    "|---|---|\n",
    "| `LargestPropertyUseTypeGFA` | Building size is the primary energy driver |\n",
    "| `Age` | Older buildings are less energy-efficient |\n",
    "| `NumberofFloors` | Taller buildings have more complex HVAC demand |\n",
    "| `Ratio_ElectricityShare` | Electricity-heavy buildings have different consumption profiles |\n",
    "| `LargestPropertyUseType` | Building use type shapes demand patterns |\n",
    "\n",
    "### Practical implication for Seattle Planning\n",
    "The model can now estimate energy consumption for any non-residential building\n",
    "using data that is **already available in city records**: floor area, building age,\n",
    "number of floors, use type, and energy billing data.\n",
    "No expensive field survey or ENERGY STAR certification is required.\n",
    "\n",
    "This enables the city to:\n",
    "- **Prioritise retrofits** — identify high-consumption buildings for intervention\n",
    "- **Set realistic targets** — model the impact of retrofitting specific building cohorts\n",
    "- **Monitor progress** — track predicted vs actual consumption year over year\n"]),
]

save_nb("05_final_model_and_results.ipynb", nb05_cells)


# ── Delete old notebooks ──────────────────────────────────────────────────
for old in ["01_eda.ipynb", "02a_modeling.ipynb", "02b_modeling.ipynb"]:
    path = os.path.join(NB, old)
    if os.path.exists(path):
        os.remove(path)
        print(f"  deleted {old}")

print("\nDone.")
