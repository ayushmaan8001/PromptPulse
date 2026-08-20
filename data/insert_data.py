

import os
import sys
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values

DB_CONFIG = {
    "host":   os.environ.get("DB_HOST", "localhost"),
    "port":   int(os.environ.get("DB_PORT", 5432)),
    "dbname": os.environ.get("DB_NAME", "promptpulse"),
    "user":   os.environ.get("DB_USER", "postgres"),
    "password": os.environ.get("DB_PASSWORD", ""),
}

DATA_DIR         = os.path.dirname(__file__)
USERS_CSV        = os.path.join(DATA_DIR, "users.csv")
PROMPTS_CSV      = os.path.join(DATA_DIR, "prompt_history.csv")

def get_connection():

    try:
        conn = psycopg2.connect(**DB_CONFIG)
        print("[OK] Connected to PostgreSQL database.")
        return conn
    except psycopg2.OperationalError as e:
        print(f"âœ— Connection failed: {e}")
        print("  Check your DB_CONFIG settings in insert_data.py")
        sys.exit(1)

def check_csv_exists(path: str, name: str):

    if not os.path.exists(path):
        print(f"âœ— {name} not found at: {path}")
        print("  Run generate_data.py first.")
        sys.exit(1)

def insert_users(conn, df: pd.DataFrame):

    print(f"Inserting {len(df)} users...")
    rows = [
        (
            int(row["user_id"]),
            str(row["full_name"]),
            str(row["department"]),
            str(row["designation"]),
            str(row["experience_level"]),
        )
        for _, row in df.iterrows()
    ]
    sql =
    with conn.cursor() as cur:
        execute_values(cur, sql, rows, page_size=200)
    conn.commit()
    print(f"  [OK] {len(rows)} users inserted.")

def insert_prompt_history(conn, df: pd.DataFrame):

    print(f"Inserting {len(df)} prompt history records (this may take a moment)...")

    rows = [
        (
            int(row["prompt_id"]),
            int(row["user_id"]),
            int(row["model_id"]),
            int(row["category_id"]),
            int(row["prompt_length"]),
            int(row["token_count"]),
            int(row["response_time_ms"]),
            float(row["estimated_cost"]),
            int(row["satisfaction_rating"]),
            str(row["created_at"]),
            str(row["prompt_complexity"]),
            bool(row["task_completed"]),
            str(row["response_quality"]),
        )
        for _, row in df.iterrows()
    ]

    sql =
    with conn.cursor() as cur:
        execute_values(cur, sql, rows, page_size=500)
    conn.commit()
    print(f"  [OK] {len(rows)} prompt history records inserted.")

def verify_counts(conn):

    print("\nVerification â€“ Table Record Counts:")
    tables = ["users", "ai_models", "prompt_categories", "prompt_history"]
    with conn.cursor() as cur:
        for table in tables:
            cur.execute(f"SELECT COUNT(*) FROM {table};")
            count = cur.fetchone()[0]
            print(f"  {table:<20}: {count:>6} records")

def main():

    check_csv_exists(USERS_CSV,   "users.csv")
    check_csv_exists(PROMPTS_CSV, "prompt_history.csv")

    print("Loading CSV files...")
    users_df   = pd.read_csv(USERS_CSV)
    prompts_df = pd.read_csv(PROMPTS_CSV)
    print(f"  [OK] {len(users_df)} users loaded.")
    print(f"  [OK] {len(prompts_df)} prompt records loaded.")

    conn = get_connection()

    try:

        with conn.cursor() as cur:
            cur.execute("TRUNCATE TABLE prompt_history, users CASCADE;")
        conn.commit()

        insert_users(conn, users_df)
        insert_prompt_history(conn, prompts_df)
        verify_counts(conn)
        print("\n[OK] All data successfully inserted into PostgreSQL!")

    except Exception as e:
        conn.rollback()
        print(f"\n[FAIL] Error during insertion: {e}")
        raise
    finally:
        conn.close()
        print("[OK] Database connection closed.")

if __name__ == "__main__":
    main()
