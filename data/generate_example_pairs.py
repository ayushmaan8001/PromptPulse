import os
import random
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
from faker import Faker

DEPARTMENTS = [
    "Engineering", "Marketing", "Finance",
    "Human Resources", "Operations", "Sales", "Design"
]

DESIGNATIONS = {
    "Engineering":      ["Software Engineer", "Data Engineer", "DevOps Engineer", "Backend Developer", "ML Engineer"],
    "Marketing":        ["Marketing Analyst", "SEO Specialist", "Content Strategist", "Growth Marketer", "Brand Manager"],
    "Finance":          ["Financial Analyst", "Accountant", "Budget Analyst", "Risk Analyst", "Controller"],
    "Human Resources":  ["HR Generalist", "Recruiter", "Talent Manager", "Compensation Analyst", "L&D Specialist"],
    "Operations":       ["Operations Analyst", "Supply Chain Lead", "Project Manager", "Process Analyst", "Logistics Coordinator"],
    "Sales":            ["Sales Executive", "Account Manager", "Business Dev Rep", "Sales Analyst", "Customer Success Manager"],
    "Design":           ["UI Designer", "UX Researcher", "Product Designer", "Visual Designer", "Creative Director"],
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

def generate_dataset_pair(pair_name, seed, num_users, num_prompts, start_date, end_date, tech_heavy=False):
    random.seed(seed)
    np.random.seed(seed)
    fake = Faker()
    Faker.seed(seed)

    user_records = []
    for i in range(1, num_users + 1):
        dept = "Engineering" if (tech_heavy and random.random() < 0.50) else random.choice(DEPARTMENTS)
        user_records.append({
            "user_id":          i,
            "full_name":        fake.name(),
            "department":       dept,
            "designation":      random.choice(DESIGNATIONS[dept]),
            "experience_level": random.choice(EXPERIENCE_LEVELS),
        })
    users_df = pd.DataFrame(user_records)

    user_ids   = users_df["user_id"].tolist()
    user_depts = users_df.set_index("user_id")["department"].to_dict()

    prompt_records = []
    for i in range(1, num_prompts + 1):
        uid  = random.choice(user_ids)
        dept = user_depts[uid]

        if tech_heavy and dept == "Engineering":
            cat_id = random.choices([1, 2, 6, 3, 7], weights=[0.40, 0.30, 0.15, 0.10, 0.05], k=1)[0]
        else:
            cat_id = random.randint(1, 9)

        if tech_heavy:
            model_id = random.choices([1, 4, 2, 3, 5], weights=[0.35, 0.35, 0.15, 0.10, 0.05], k=1)[0]
        else:
            model_id = random.randint(1, 5)

        token_count      = int(np.random.lognormal(mean=6.8 if tech_heavy else 6.4, sigma=0.7))
        token_count      = max(50, min(4000, token_count))
        prompt_length    = int(token_count * random.uniform(0.6, 1.2))
        response_time_ms = int(np.random.lognormal(mean=7.5, sigma=0.6))
        response_time_ms = max(500, min(12000, response_time_ms))

        base_cost      = AI_MODELS[model_id]["cost_per_token"]
        estimated_cost = round(token_count * base_cost * random.uniform(0.9, 1.1), 6)

        rating = random.choices([1, 2, 3, 4, 5], weights=[0.05, 0.10, 0.20, 0.40, 0.25], k=1)[0]

        complexity = "Complex" if token_count >= 2000 else "Medium" if token_count >= 500 else "Simple"
        quality    = "Excellent" if rating >= 4 and model_id in [1, 2] else "Good" if rating >= 3 else "Fair"
        task_done  = random.random() < (0.90 if quality == "Excellent" else 0.75)

        delta_sec = int((end_date - start_date).total_seconds())
        ts = start_date + timedelta(seconds=random.randint(0, delta_sec))

        prompt_records.append({
            "prompt_id":           i,
            "user_id":             uid,
            "model_id":            model_id,
            "category_id":         cat_id,
            "prompt_length":       prompt_length,
            "token_count":         token_count,
            "response_time_ms":    response_time_ms,
            "estimated_cost":      estimated_cost,
            "satisfaction_rating": rating,
            "created_at":          ts.strftime("%Y-%m-%d %H:%M:%S"),
            "prompt_complexity":   complexity,
            "task_completed":      task_done,
            "response_quality":    quality,
        })

    prompts_df = pd.DataFrame(prompt_records)

    out_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "example_datasets", pair_name)
    os.makedirs(out_dir, exist_ok=True)

    users_path   = os.path.join(out_dir, f"{pair_name}_users.csv")
    prompts_path = os.path.join(out_dir, f"{pair_name}_prompt_history.csv")

    users_df.to_csv(users_path, index=False)
    prompts_df.to_csv(prompts_path, index=False)

    print(f"[OK] Generated {pair_name}:")
    print(f"   - Users         : {len(users_df)} ({users_path})")
    print(f"   - Prompt History: {len(prompts_df)} ({prompts_path})")

def main():
    print("Generating 4 dataset variation pairs...\n")

    generate_dataset_pair(
        pair_name="pair1_small_scale",
        seed=101,
        num_users=100,
        num_prompts=2000,
        start_date=datetime(2024, 1, 1),
        end_date=datetime(2024, 12, 31),
    )

    generate_dataset_pair(
        pair_name="pair2_large_scale",
        seed=202,
        num_users=1000,
        num_prompts=25000,
        start_date=datetime(2024, 1, 1),
        end_date=datetime(2024, 12, 31),
    )

    generate_dataset_pair(
        pair_name="pair3_tech_heavy",
        seed=303,
        num_users=500,
        num_prompts=10000,
        start_date=datetime(2024, 1, 1),
        end_date=datetime(2024, 12, 31),
        tech_heavy=True,
    )

    generate_dataset_pair(
        pair_name="pair4_q4_surge",
        seed=404,
        num_users=300,
        num_prompts=5000,
        start_date=datetime(2024, 10, 1),
        end_date=datetime(2024, 12, 31),
    )

    print("\n[OK] All 4 dataset pairs successfully created under 'example_datasets/'!")

if __name__ == "__main__":
    main()
