<div align="center">

# PromptPulse

**A SQL-based analytics engine for Generative AI prompt usage intelligence**

[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-18-336791?style=flat-square&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Power BI](https://img.shields.io/badge/Power_BI-Dashboard-F2C811?style=flat-square&logo=powerbi&logoColor=black)](https://powerbi.microsoft.com/)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

</div>

---

## The Problem

Organisations run GPT-4o, Claude, Gemini, Copilot, and DeepSeek across every team but have zero visibility into:

- Which model actually delivers the best task completion per dollar spent?
- Which department is burning the most tokens?
- Are longer, more complex prompts producing better outputs?
- Is AI adoption growing or plateauing month-over-month?

Most teams make six-figure AI subscription decisions based on gut feel.

**PromptPulse fixes that.**

---

## How It Works

Every AI interaction gets logged into a normalised PostgreSQL schema. A suite of 23 advanced SQL queries then extracts actionable intelligence model benchmarks, department spend, adoption trends, latency profiles, and quality correlations, all surfaced through a live Power BI dashboard.

```
Python simulation  →  PostgreSQL (3NF schema)  →  SQL analytics  →  Power BI dashboard
     10,000 rows         4 tables + indexes         23 queries         live KPI cards
```

---

## Stack

| Layer | Technology |
|:---|:---|
| **Database** | PostgreSQL 18 |
| **Data Pipeline** | Python 3.12 · Faker · NumPy · Pandas |
| **DB Connector** | psycopg2-binary |
| **Analytics** | SQL CTEs · Window Functions · Ordered-Set Aggregates |
| **Dashboard** | Power BI Desktop |

---

## Project Structure

```
PromptPulse/
├── database/
│   └── schema.sql                  4-table 3NF schema with B-Tree indexes
├── data/
│   ├── generate_data.py            Synthetic data generator (500 users, 10K records)
│   ├── insert_data.py              Batch PostgreSQL loader via psycopg2
│   └── generate_example_pairs.py  Generates 4 dataset scenario variations
├── sql/
│   └── analytics.sql              23 production-grade analytical queries
├── example_datasets/              4 ready-to-load scenario datasets
│   ├── pair1_small_scale/
│   ├── pair2_large_scale/
│   ├── pair3_tech_heavy/
│   └── pair4_q4_surge/
├── dashboard/
│   ├── PromptPulse.pbix           Power BI dashboard (live PostgreSQL connection)
│   └── POWERBI_SETUP.md           Power BI connection setup guide
├── .env.example                   Credential config template
└── requirements.txt
```

---

## Quickstart

### Prerequisites
- PostgreSQL 16+
- Python 3.12+
- Power BI Desktop (Windows)

### Setup

```bash
# 1. Clone
git clone https://github.com/ayushmaan8001/PromptPulse.git
cd PromptPulse

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Configure credentials
cp .env.example .env          # Mac/Linux
copy .env.example .env        # Windows CMD
# Open .env and set DB_PASSWORD to your PostgreSQL password
```

```sql
-- 4. In pgAdmin: create the database and run the schema
CREATE DATABASE promptpulse;
-- Then open database/schema.sql and execute it
```

```bash
# 5. Generate synthetic data and load it
python data/generate_data.py
python data/insert_data.py
```

```
# 6. Run analytics
# Open sql/analytics.sql in pgAdmin → F5

# 7. Open dashboard
# Open dashboard/PromptPulse.pbix in Power BI Desktop
# Connect to: localhost / promptpulse / load all 4 tables
```

---

## Database Schema

```
┌─────────────────┐     ┌──────────────────────┐     ┌────────────────────┐
│     users       │     │    prompt_history    │     │    ai_models       │
│─────────────────│     │──────────────────────│     │────────────────────│
│ user_id (PK)    │──┐  │ prompt_id (PK)       │  ┌──│ model_id (PK)      │
│ full_name       │  └──│ user_id (FK)         │  │  │ model_name         │
│ department      │     │ model_id (FK)        │──┘  │ provider           │
│ designation     │     │ category_id (FK)     │──┐  └────────────────────┘
│ experience_level│     │ token_count          │  │  ┌────────────────────┐
└─────────────────┘     │ response_time_ms     │  │  │ prompt_categories  │
                        │ estimated_cost       │  └──│────────────────────│
                        │ satisfaction_rating  │     │ category_id (PK)   │
                        │ prompt_complexity    │     │ category_name      │
                        │ task_completed       │     └────────────────────┘
                        │ response_quality     │
                        └──────────────────────┘
```

5 B-Tree indexes on high-frequency filter columns (`created_at`, `user_id`, `model_id`, `category_id`, and a composite index on `(model_id, created_at)`).

---

## Analytics Coverage

The 23 queries in `sql/analytics.sql` cover:

| Category | Queries |
|:---|:---|
| **Platform KPIs** | Total prompts · active users · avg satisfaction · total cost · completion rate |
| **Model Benchmarking** | Performance rank via `DENSE_RANK()` · cost per token · P95 latency via `PERCENTILE_CONT` |
| **Department Analysis** | Spend by department · adoption rank · tokens per user |
| **Temporal Trends** | Month-over-month growth via `LAG()` · peak usage hours · weekly patterns |
| **Quality Intelligence** | Prompt complexity vs response quality matrix · satisfaction tier distribution |
| **Cost Efficiency** | Cost per successful task by model · budget allocation analysis |

---

## Example Datasets

Four pre-built scenario datasets for testing without running the generator:

| Scenario | Users | Records | Use Case |
|:---|:---:|:---:|:---|
| `pair1_small_scale` | 100 | 2,000 | Baseline small team |
| `pair2_large_scale` | 1,000 | 25,000 | Large enterprise load |
| `pair3_tech_heavy` | 500 | 10,000 | Engineering-dominant usage pattern |
| `pair4_q4_surge` | 300 | 5,000 | Q4 adoption spike simulation |

Load any pair by replacing CSVs in `data/` and re-running `insert_data.py`.

---

## Performance

| Metric | Without Index | With B-Tree Index | Improvement |
|:---|:---:|:---:|:---:|
| Query execution time | 43.7 ms | 5.6 ms | **87% faster** |
| Rows scanned (monthly query) | 10,000 | ~833 | **91% fewer** |

Verified via `EXPLAIN ANALYZE` on the month-over-month growth query at 10,000 records.

---

## License

[MIT](LICENSE)
