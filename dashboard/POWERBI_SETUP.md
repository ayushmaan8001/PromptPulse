# Power BI Dashboard Setup ## PromptPulse: SQL-Based Analytics of Generative AI Prompt Usage

---

## Prerequisites
- Power BI Desktop (free download: https://powerbi.microsoft.com/desktop)
- PostgreSQL ODBC Driver (https://www.postgresql.org/ftp/odbc/versions/)
- PromptPulse database running locally with data inserted

---

## Step 1: Connect Power BI to PostgreSQL

1. Open **Power BI Desktop**.
2. Click **Home â†’ Get Data â†’ More â†’ Database â†’ PostgreSQL database**.
3. Enter:
   - **Server:** `localhost`
   - **Database:** `promptpulse`
4. Click **OK** and enter credentials (`postgres` / `postgres`).
5. In the Navigator, select all four tables:
   - `users`
   - `ai_models`
   - `prompt_categories`
   - `prompt_history`
6. Click **Load**.

---

## Step 2: Create Relationships (Model View)

Go to **Model View** (left sidebar, middle icon).

Verify these relationships exist (Power BI should auto-detect them):

| From Table       | Column      | To Table           | Column      | Cardinality |
|---|---|---|---|---|
| `prompt_history` | `user_id`      | `users`            | `user_id`      | Many â†’ One  |
| `prompt_history` | `model_id`     | `ai_models`        | `model_id`     | Many â†’ One  |
| `prompt_history` | `category_id`  | `prompt_categories`| `category_id`  | Many â†’ One  |

---

## Step 3: Create Calculated Measures (DAX)

In the **Data View**, click **New Measure** and add the following DAX measures:

```dax
Total Prompts = COUNTROWS(prompt_history)

Total Users = DISTINCTCOUNT(prompt_history[user_id])

Average Rating = AVERAGE(prompt_history[satisfaction_rating])

Total Cost (USD) = SUM(prompt_history[estimated_cost])

Task Completion Rate = 
DIVIDE(
    COUNTROWS(FILTER(prompt_history, prompt_history[task_completed] = TRUE())),
    COUNTROWS(prompt_history)
) * 100

Avg Response Time (ms) = AVERAGE(prompt_history[response_time_ms])

Avg Token Count = AVERAGE(prompt_history[token_count])
```

---

## Step 4: Build the Dashboard (Report View)

Switch to **Report View**. Create the following pages:

---

### Page 1: Overview

**4 KPI Cards** (top row):
- Card â†’ Field: `Total Prompts`
- Card â†’ Field: `Total Users`
- Card â†’ Field: `Average Rating`
- Card â†’ Field: `Total Cost (USD)` (format as $ with 4 decimals)

**Clustered Bar Chart** â€“ AI Model Usage:
- Axis: `ai_models[model_name]`
- Values: `Total Prompts`
- Sort: Descending by Total Prompts

**Donut Chart** â€“ Prompt Category Distribution:
- Legend: `prompt_categories[category_name]`
- Values: `Total Prompts`

**Clustered Column Chart** â€“ Department-wise Usage:
- Axis: `users[department]`
- Values: `Total Prompts`

---

### Page 2: Time Trends

**Line Chart** â€“ Monthly Prompt Trend:
- X-Axis: `prompt_history[created_at]` (set hierarchy to Month)
- Y-Axis: `Total Prompts`

**Line Chart** â€“ Monthly Active Users:
- X-Axis: `prompt_history[created_at]` (Month)
- Y-Axis: `Total Users`

**Clustered Column Chart** â€“ Monthly Cost:
- X-Axis: Month
- Y-Axis: `Total Cost (USD)`

**Area Chart** â€“ Token Consumption Trend:
- X-Axis: Month
- Y-Axis: SUM of `token_count`

---

### Page 3: Performance & Quality

**Stacked Bar Chart** â€“ Response Quality by Model:
- Axis: `ai_models[model_name]`
- Legend: `prompt_history[response_quality]`
- Values: `Total Prompts`

**Matrix** â€“ Complexity vs Quality Heatmap:
- Rows: `prompt_history[prompt_complexity]`
- Columns: `prompt_history[response_quality]`
- Values: `Total Prompts`

**Bar Chart** â€“ Task Completion Rate by Model:
- Axis: `ai_models[model_name]`
- Values: `Task Completion Rate`

**Line Chart** â€“ Hourly Usage Pattern:
- X-Axis: Hour of Day (HOUR(`created_at`))
- Y-Axis: `Total Prompts`

---

### Page 4: Cost & Tokens

**Scatter Chart** â€“ Token Count vs Cost:
- X-Axis: `token_count`
- Y-Axis: `estimated_cost`
- Legend: `ai_models[model_name]`

**Bar Chart** â€“ Average Cost per Department:
- Axis: `users[department]`
- Values: AVERAGE(`estimated_cost`)

**Bar Chart** â€“ Top 10 Users by Token Usage:
- Axis: `users[full_name]`
- Values: SUM(`token_count`)
- Filter Top N: 10

---

## Step 5: Add Interactive Slicers (Filters)

Add the following **Slicer** visuals to each page:

| Slicer | Field |
|---|---|
| Department | `users[department]` |
| AI Model | `ai_models[model_name]` |
| Prompt Category | `prompt_categories[category_name]` |
| Date Range | `prompt_history[created_at]` (Date Range slicer) |
| Complexity | `prompt_history[prompt_complexity]` |

---

## Step 6: Formatting (Professional Look)

1. **Theme:** Go to **View â†’ Themes â†’ Executive** or apply a dark custom theme.
2. **Color Palette:** Use a consistent blue/slate color palette.
3. **Canvas Background:** Set to `#0f172a` for a dark professional look.
4. **Font:** Use Segoe UI throughout.
5. **Titles:** Every visual should have a clear, descriptive title.
6. **Grid Lines:** Minimize or remove for cleaner charts.

---

## Step 7: Save

Save the file as `dashboard/PromptPulse.pbix`.

---

## Expected Dashboard Output

Your final dashboard should show:
- **Total Prompts:** ~10,000
- **Total Users:** ~500
- **Avg Rating:** ~3.8/5
- **Total Cost:** ~$0.50â€“$0.60 USD
- **Task Completion Rate:** ~80â€“85%
- **Peak Hour:** 9amâ€“6pm
- **Top Model:** GPT-4o or GitHub Copilot
- **Top Department:** Engineering

