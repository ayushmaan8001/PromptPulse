

import random
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
from faker import Faker

SEED            = 42
NUM_USERS       = 500
NUM_PROMPTS     = 10_000
START_DATE      = datetime(2024, 1, 1)
END_DATE        = datetime(2024, 12, 31, 23, 59, 59)

random.seed(SEED)
np.random.seed(SEED)
fake = Faker()
Faker.seed(SEED)

DEPARTMENTS = [
    "Engineering", "Marketing", "Finance",
    "Human Resources", "Operations", "Sales", "Design"
]

DESIGNATIONS = {
    "Engineering":      ["Software Engineer", "Data Engineer", "DevOps Engineer",
                         "Backend Developer", "ML Engineer"],
    "Marketing":        ["Marketing Analyst", "SEO Specialist", "Content Strategist",
                         "Growth Marketer", "Brand Manager"],
    "Finance":          ["Financial Analyst", "Accountant", "Budget Analyst",
                         "Risk Analyst", "Controller"],
    "Human Resources":  ["HR Generalist", "Recruiter", "Talent Manager",
                         "Compensation Analyst", "L&D Specialist"],
    "Operations":       ["Operations Analyst", "Supply Chain Lead", "Project Manager",
                         "Process Analyst", "Logistics Coordinator"],
    "Sales":            ["Sales Executive", "Account Manager", "Business Dev Rep",
                         "Sales Analyst", "Customer Success Manager"],
    "Design":           ["UI Designer", "UX Researcher", "Product Designer",
                         "Visual Designer", "Creative Director"],
}

EXPERIENCE_LEVELS = ["Junior", "Mid", "Senior", "Lead"]

AI_MODELS = {
    1: {"name": "GPT-4o",         "cost_per_token": 0.0000100},
    2: {"name": "Claude Sonnet",  "cost_per_token": 0.0000080},
    3: {"name": "Gemini 2.5",     "cost_per_token": 0.0000070},
    4: {"name": "GitHub Copilot", "cost_per_token": 0.0000050},
    5: {"name": "DeepSeek",       "cost_per_token": 0.0000030},
}

CATEGORIES = {
    1: "Coding",
    2: "Debugging",
    3: "Research",
    4: "Writing",
    5: "Translation",
    6: "Data Analysis",
    7: "Learning",
    8: "Planning",
    9: "Brainstorming",
}

COMPLEXITIES = ["Simple", "Medium", "Complex"]

RESPONSE_QUALITIES = ["Poor", "Fair", "Good", "Excellent"]

CATEGORY_MODEL_WEIGHTS = {
    1:  [0.30, 0.15, 0.15, 0.35, 0.05],
    2:  [0.30, 0.20, 0.15, 0.30, 0.05],
    3:  [0.25, 0.25, 0.30, 0.10, 0.10],
    4:  [0.25, 0.35, 0.20, 0.05, 0.15],
    5:  [0.20, 0.20, 0.40, 0.05, 0.15],
    6:  [0.35, 0.20, 0.20, 0.10, 0.15],
    7:  [0.25, 0.25, 0.25, 0.10, 0.15],
    8:  [0.25, 0.25, 0.25, 0.10, 0.15],
    9:  [0.25, 0.25, 0.25, 0.10, 0.15],
}

DEPT_CATEGORY_WEIGHTS = {
    "Engineering":      [0.30, 0.25, 0.10, 0.05, 0.02, 0.10, 0.08, 0.05, 0.05],
    "Marketing":        [0.05, 0.02, 0.15, 0.30, 0.10, 0.08, 0.10, 0.10, 0.10],
    "Finance":          [0.05, 0.05, 0.20, 0.10, 0.05, 0.35, 0.05, 0.10, 0.05],
    "Human Resources":  [0.03, 0.02, 0.15, 0.25, 0.10, 0.05, 0.15, 0.15, 0.10],
    "Operations":       [0.05, 0.05, 0.15, 0.10, 0.05, 0.15, 0.10, 0.25, 0.10],
    "Sales":            [0.05, 0.03, 0.15, 0.25, 0.05, 0.10, 0.10, 0.12, 0.15],
    "Design":           [0.05, 0.05, 0.15, 0.20, 0.05, 0.05, 0.10, 0.15, 0.20],
}

def random_timestamp(start: datetime, end: datetime) -> datetime:

    delta_seconds = int((end - start).total_seconds())
    random_seconds = random.randint(0, delta_seconds)
    ts = start + timedelta(seconds=random_seconds)

    if random.random() < 0.70:
        ts = ts.replace(hour=random.randint(9, 19))
    return ts

def token_to_cost(token_count: int, model_id: int) -> float:

    base_cost = AI_MODELS[model_id]["cost_per_token"]

    variance = random.uniform(0.90, 1.10)
    return round(token_count * base_cost * variance, 6)

def complexity_from_token(token_count: int) -> str:

    if token_count < 500:
        return "Simple"
    elif token_count < 2000:
        return "Medium"
    else:
        return "Complex"

def quality_from_complexity_and_model(complexity: str, model_id: int,
                                       rating: int) -> str:

    model_premium = {1: 5, 2: 4, 3: 4, 4: 3, 5: 3}
    score = model_premium[model_id] + rating

    if score >= 9:
        return "Excellent"
    elif score >= 7:
        return "Good"
    elif score >= 5:
        return "Fair"
    else:
        return "Poor"

def task_completed_from_quality(quality: str, complexity: str) -> bool:

    completion_rates = {
        ("Excellent", "Simple"):  0.99,
        ("Excellent", "Medium"):  0.96,
        ("Excellent", "Complex"): 0.88,
        ("Good",      "Simple"):  0.95,
        ("Good",      "Medium"):  0.88,
        ("Good",      "Complex"): 0.75,
        ("Fair",      "Simple"):  0.80,
        ("Fair",      "Medium"):  0.65,
        ("Fair",      "Complex"): 0.50,
        ("Poor",      "Simple"):  0.60,
        ("Poor",      "Medium"):  0.40,
        ("Poor",      "Complex"): 0.25,
    }
    rate = completion_rates.get((quality, complexity), 0.70)
    return random.random() < rate

def generate_users(n: int = NUM_USERS) -> pd.DataFrame:

    print(f"Generating {n} users...")
    records = []
    for i in range(1, n + 1):
        dept = random.choice(DEPARTMENTS)
        records.append({
            "user_id":          i,
            "full_name":        fake.name(),
            "department":       dept,
            "designation":      random.choice(DESIGNATIONS[dept]),
            "experience_level": random.choice(EXPERIENCE_LEVELS),
        })
    df = pd.DataFrame(records)
    print(f"  âœ“ {len(df)} users generated.")
    return df

def generate_prompt_history(users_df: pd.DataFrame,
                             n: int = NUM_PROMPTS) -> pd.DataFrame:

    print(f"Generating {n} prompt history records...")

    user_ids   = users_df["user_id"].tolist()
    user_depts = users_df.set_index("user_id")["department"].to_dict()

    records = []
    for i in range(1, n + 1):

        uid  = random.choice(user_ids)
        dept = user_depts[uid]

        cat_weights = DEPT_CATEGORY_WEIGHTS[dept]
        cat_ids     = list(CATEGORIES.keys())
        cat_id      = random.choices(cat_ids, weights=cat_weights, k=1)[0]

        model_weights = CATEGORY_MODEL_WEIGHTS[cat_id]
        model_ids     = list(AI_MODELS.keys())
        model_id      = random.choices(model_ids, weights=model_weights, k=1)[0]

        token_count      = int(np.random.lognormal(mean=6.5, sigma=0.8))
        token_count      = max(50, min(4000, token_count))
        prompt_length    = int(token_count * random.uniform(0.6, 1.2))
        response_time_ms = int(np.random.lognormal(mean=7.5, sigma=0.6))
        response_time_ms = max(500, min(12000, response_time_ms))
        estimated_cost   = token_to_cost(token_count, model_id)
        satisfaction_rating = random.choices(
            [1, 2, 3, 4, 5],
            weights=[0.05, 0.10, 0.20, 0.40, 0.25], k=1
        )[0]

        complexity   = complexity_from_token(token_count)
        quality      = quality_from_complexity_and_model(complexity, model_id,
                                                          satisfaction_rating)
        task_done    = task_completed_from_quality(quality, complexity)
        created_at   = random_timestamp(START_DATE, END_DATE)

        records.append({
            "prompt_id":           i,
            "user_id":             uid,
            "model_id":            model_id,
            "category_id":         cat_id,
            "prompt_length":       prompt_length,
            "token_count":         token_count,
            "response_time_ms":    response_time_ms,
            "estimated_cost":      estimated_cost,
            "satisfaction_rating": satisfaction_rating,
            "created_at":          created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "prompt_complexity":   complexity,
            "task_completed":      task_done,
            "response_quality":    quality,
        })

    df = pd.DataFrame(records)
    print(f"  âœ“ {len(df)} prompt history records generated.")
    return df

def main():
    import os
    out_dir = os.path.join(os.path.dirname(__file__))

    users_df   = generate_users()
    prompts_df = generate_prompt_history(users_df)

    users_path   = os.path.join(out_dir, "users.csv")
    prompts_path = os.path.join(out_dir, "prompt_history.csv")

    users_df.to_csv(users_path, index=False)
    prompts_df.to_csv(prompts_path, index=False)

    print(f"\nâœ“ Data saved:")
    print(f"  {users_path}")
    print(f"  {prompts_path}")
    print("\nData Summary:")
    print(f"  Users             : {len(users_df)}")
    print(f"  Prompt Records    : {len(prompts_df)}")
    print(f"  Date Range        : {prompts_df['created_at'].min()} â†’ "
          f"{prompts_df['created_at'].max()}")
    print(f"  Avg Token Count   : {prompts_df['token_count'].mean():.0f}")
    print(f"  Total Est. Cost   : ${prompts_df['estimated_cost'].sum():.4f}")
    print(f"  Avg Satisfaction  : {prompts_df['satisfaction_rating'].mean():.2f}/5")
    print(f"\n  Complexity Dist:\n"
          f"{prompts_df['prompt_complexity'].value_counts().to_string()}")
    print(f"\n  Quality Dist:\n"
          f"{prompts_df['response_quality'].value_counts().to_string()}")
    print(f"\n  Task Completion Rate: "
          f"{prompts_df['task_completed'].mean() * 100:.1f}%")

if __name__ == "__main__":
    main()
