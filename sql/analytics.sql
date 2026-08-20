
SELECT
    am.model_name,
    am.provider,
    COUNT(ph.prompt_id)                                     AS total_prompts,
    ROUND(COUNT(ph.prompt_id) * 100.0 / SUM(COUNT(ph.prompt_id))
          OVER (), 2)                                       AS usage_share_pct
FROM prompt_history ph
INNER JOIN ai_models am ON ph.model_id = am.model_id
GROUP BY am.model_id, am.model_name, am.provider
ORDER BY total_prompts DESC
LIMIT 5;
SELECT
    u.department,
    COUNT(ph.prompt_id)                                     AS total_prompts,
    COUNT(DISTINCT ph.user_id)                              AS active_users,
    ROUND(AVG(ph.satisfaction_rating), 2)                   AS avg_rating,
    ROUND(SUM(ph.estimated_cost), 4)                        AS total_cost_usd,
    DENSE_RANK() OVER (ORDER BY COUNT(ph.prompt_id) DESC)   AS dept_rank
FROM prompt_history ph
INNER JOIN users u ON ph.user_id = u.user_id
GROUP BY u.department
ORDER BY total_prompts DESC;
SELECT
    pc.category_name,
    ROUND(AVG(ph.prompt_length), 0)                         AS avg_prompt_length,
    ROUND(AVG(ph.token_count), 0)                           AS avg_token_count,
    COUNT(ph.prompt_id)                                     AS total_prompts
FROM prompt_history ph
INNER JOIN prompt_categories pc ON ph.category_id = pc.category_id
GROUP BY pc.category_id, pc.category_name
ORDER BY avg_prompt_length DESC;
SELECT
    am.model_name,
    am.provider,
    ROUND(AVG(ph.response_time_ms), 0)                      AS avg_response_ms,
    MIN(ph.response_time_ms)                                AS min_response_ms,
    MAX(ph.response_time_ms)                                AS max_response_ms,
    ROUND((PERCENTILE_CONT(0.95) WITHIN GROUP
          (ORDER BY ph.response_time_ms))::NUMERIC, 0)        AS p95_response_ms
FROM prompt_history ph
INNER JOIN ai_models am ON ph.model_id = am.model_id
GROUP BY am.model_id, am.model_name, am.provider
ORDER BY avg_response_ms ASC;
SELECT
    TO_CHAR(DATE_TRUNC('month', ph.created_at), 'YYYY-Mon') AS month,
    SUM(ph.token_count)                                     AS total_tokens,
    COUNT(ph.prompt_id)                                     AS total_prompts,
    ROUND(AVG(ph.token_count), 0)                           AS avg_tokens_per_prompt
FROM prompt_history ph
GROUP BY DATE_TRUNC('month', ph.created_at)
ORDER BY DATE_TRUNC('month', ph.created_at);
SELECT
    TO_CHAR(DATE_TRUNC('month', ph.created_at), 'YYYY-Mon') AS month,
    ROUND(SUM(ph.estimated_cost), 4)                        AS total_cost_usd,
    ROUND(AVG(ph.estimated_cost), 6)                        AS avg_cost_per_prompt,
    COUNT(ph.prompt_id)                                     AS total_prompts
FROM prompt_history ph
GROUP BY DATE_TRUNC('month', ph.created_at)
ORDER BY DATE_TRUNC('month', ph.created_at);
SELECT
    DATE(ph.created_at)                                     AS prompt_date,
    TO_CHAR(DATE(ph.created_at), 'Day')                     AS day_of_week,
    COUNT(ph.prompt_id)                                     AS total_prompts
FROM prompt_history ph
WHERE ph.created_at >= (
    SELECT MAX(created_at) - INTERVAL '30 days' FROM prompt_history
)
GROUP BY DATE(ph.created_at)
ORDER BY prompt_date;
SELECT
    EXTRACT(HOUR FROM ph.created_at)::INT                   AS hour_of_day,
    COUNT(ph.prompt_id)                                     AS total_prompts,
    ROUND(AVG(ph.satisfaction_rating), 2)                   AS avg_rating,
    ROUND(COUNT(ph.prompt_id) * 100.0 / SUM(COUNT(ph.prompt_id))
          OVER (), 2)                                       AS pct_of_total
FROM prompt_history ph
GROUP BY EXTRACT(HOUR FROM ph.created_at)
ORDER BY hour_of_day;
SELECT
    pc.category_name,
    ROUND(AVG(ph.satisfaction_rating), 3)                   AS avg_rating,
    COUNT(ph.prompt_id)                                     AS total_prompts,
    RANK() OVER (ORDER BY AVG(ph.satisfaction_rating) DESC) AS rating_rank
FROM prompt_history ph
INNER JOIN prompt_categories pc ON ph.category_id = pc.category_id
GROUP BY pc.category_id, pc.category_name
ORDER BY avg_rating DESC;
SELECT
    pc.category_name,
    ROUND(AVG(ph.satisfaction_rating), 3)                   AS avg_rating,
    COUNT(ph.prompt_id)                                     AS total_prompts,
    RANK() OVER (ORDER BY AVG(ph.satisfaction_rating) ASC)  AS poor_rank
FROM prompt_history ph
INNER JOIN prompt_categories pc ON ph.category_id = pc.category_id
GROUP BY pc.category_id, pc.category_name
ORDER BY avg_rating ASC;
SELECT
    ph.user_id,
    u.full_name,
    u.department,
    u.designation,
    COUNT(ph.prompt_id)                                     AS total_prompts,
    SUM(ph.token_count)                                     AS total_tokens,
    ROUND(SUM(ph.estimated_cost), 4)                        AS total_cost_usd,
    ROW_NUMBER() OVER (ORDER BY COUNT(ph.prompt_id) DESC)   AS usage_rank
FROM prompt_history ph
INNER JOIN users u ON ph.user_id = u.user_id
GROUP BY ph.user_id, u.full_name, u.department, u.designation
ORDER BY total_prompts DESC
LIMIT 10;
SELECT
    u.department,
    ROUND(AVG(ph.token_count), 0)                           AS avg_token_count,
    ROUND(AVG(ph.prompt_length), 0)                         AS avg_prompt_length,
    SUM(ph.token_count)                                     AS total_tokens,
    DENSE_RANK() OVER (ORDER BY AVG(ph.token_count) DESC)   AS token_rank
FROM prompt_history ph
INNER JOIN users u ON ph.user_id = u.user_id
GROUP BY u.department
ORDER BY avg_token_count DESC;
SELECT
    u.department,
    COUNT(ph.prompt_id)                                     AS total_prompts,
    ROUND(AVG(ph.estimated_cost), 6)                        AS avg_cost_per_prompt,
    ROUND(SUM(ph.estimated_cost), 4)                        AS total_cost_usd,
    RANK() OVER (ORDER BY SUM(ph.estimated_cost) DESC)      AS cost_rank
FROM prompt_history ph
INNER JOIN users u ON ph.user_id = u.user_id
GROUP BY u.department
ORDER BY total_cost_usd DESC;
SELECT
    ph.prompt_id,
    u.full_name,
    u.department,
    am.model_name,
    pc.category_name,
    ph.token_count,
    ph.prompt_complexity,
    ROUND(ph.estimated_cost, 6)                             AS cost_usd,
    ph.response_quality,
    ph.created_at
FROM prompt_history ph
INNER JOIN users u   ON ph.user_id      = u.user_id
INNER JOIN ai_models am ON ph.model_id  = am.model_id
INNER JOIN prompt_categories pc ON ph.category_id = pc.category_id
ORDER BY ph.estimated_cost DESC
LIMIT 10;
WITH monthly_counts AS (
    SELECT
        DATE_TRUNC('month', created_at)                     AS month,
        COUNT(prompt_id)                                    AS total_prompts
    FROM prompt_history
    GROUP BY DATE_TRUNC('month', created_at)
)
SELECT
    TO_CHAR(month, 'YYYY-Mon')                              AS month,
    total_prompts,
    LAG(total_prompts) OVER (ORDER BY month)                AS prev_month_prompts,
    ROUND(
        (total_prompts - LAG(total_prompts) OVER (ORDER BY month))
        * 100.0
        / NULLIF(LAG(total_prompts) OVER (ORDER BY month), 0),
        2
    )                                                       AS mom_growth_pct
FROM monthly_counts
ORDER BY month;
SELECT
    TO_CHAR(DATE_TRUNC('month', ph.created_at), 'YYYY-Mon') AS month,
    COUNT(DISTINCT ph.user_id)                              AS monthly_active_users,
    COUNT(ph.prompt_id)                                     AS total_prompts,
    ROUND(COUNT(ph.prompt_id) * 1.0 /
          COUNT(DISTINCT ph.user_id), 1)                    AS prompts_per_active_user
FROM prompt_history ph
GROUP BY DATE_TRUNC('month', ph.created_at)
ORDER BY DATE_TRUNC('month', ph.created_at);
WITH daily_counts AS (
    SELECT
        DATE(created_at)                                    AS prompt_date,
        COUNT(prompt_id)                                    AS daily_prompts
    FROM prompt_history
    GROUP BY DATE(created_at)
)
SELECT
    prompt_date,
    daily_prompts,
    ROUND(
        AVG(daily_prompts) OVER (
            ORDER BY prompt_date
            ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
        ), 1
    )                                                       AS rolling_7day_avg
FROM daily_counts
ORDER BY prompt_date;
SELECT
    u.user_id,
    u.full_name,
    u.department,
    u.experience_level,
    SUM(ph.token_count)                                     AS total_tokens,
    COUNT(ph.prompt_id)                                     AS total_prompts,
    RANK() OVER (ORDER BY SUM(ph.token_count) DESC)         AS token_rank
FROM prompt_history ph
INNER JOIN users u ON ph.user_id = u.user_id
GROUP BY u.user_id, u.full_name, u.department, u.experience_level
ORDER BY token_rank
LIMIT 20;
WITH model_monthly AS (
    SELECT
        am.model_name,
        DATE_TRUNC('month', ph.created_at)                  AS month,
        COUNT(ph.prompt_id)                                 AS monthly_prompts
    FROM prompt_history ph
    INNER JOIN ai_models am ON ph.model_id = am.model_id
    GROUP BY am.model_name, DATE_TRUNC('month', ph.created_at)
)
SELECT
    model_name,
    TO_CHAR(month, 'YYYY-Mon')                              AS month,
    monthly_prompts,
    LAG(monthly_prompts)  OVER (PARTITION BY model_name ORDER BY month) AS prev_month,
    LEAD(monthly_prompts) OVER (PARTITION BY model_name ORDER BY month) AS next_month,
    ROUND(
        (monthly_prompts - LAG(monthly_prompts) OVER
            (PARTITION BY model_name ORDER BY month)) * 100.0
        / NULLIF(LAG(monthly_prompts) OVER
            (PARTITION BY model_name ORDER BY month), 0),
        2
    )                                                       AS mom_change_pct
FROM model_monthly
ORDER BY model_name, month;
SELECT
    ph.prompt_complexity,
    ph.response_quality,
    COUNT(ph.prompt_id)                                     AS total_prompts,
    ROUND(AVG(ph.satisfaction_rating), 3)                   AS avg_satisfaction,
    ROUND(AVG(ph.token_count), 0)                           AS avg_tokens,
    ROUND(AVG(ph.response_time_ms), 0)                      AS avg_response_ms
FROM prompt_history ph
GROUP BY ph.prompt_complexity, ph.response_quality
ORDER BY
    CASE ph.prompt_complexity
        WHEN 'Simple'  THEN 1
        WHEN 'Medium'  THEN 2
        WHEN 'Complex' THEN 3
    END,
    CASE ph.response_quality
        WHEN 'Poor'      THEN 1
        WHEN 'Fair'      THEN 2
        WHEN 'Good'      THEN 3
        WHEN 'Excellent' THEN 4
    END;
SELECT
    am.model_name,
    am.provider,
    COUNT(ph.prompt_id)                                     AS total_prompts,
    SUM(CASE WHEN ph.task_completed THEN 1 ELSE 0 END)      AS tasks_completed,
    ROUND(
        SUM(CASE WHEN ph.task_completed THEN 1 ELSE 0 END)
        * 100.0 / COUNT(ph.prompt_id), 2
    )                                                       AS completion_rate_pct,
    ROUND(AVG(ph.satisfaction_rating), 2)                   AS avg_rating
FROM prompt_history ph
INNER JOIN ai_models am ON ph.model_id = am.model_id
GROUP BY am.model_id, am.model_name, am.provider
ORDER BY completion_rate_pct DESC;
WITH dept_complexity AS (
    SELECT
        u.department,
        ph.prompt_complexity,
        COUNT(ph.prompt_id)                                 AS prompt_count
    FROM prompt_history ph
    INNER JOIN users u ON ph.user_id = u.user_id
    GROUP BY u.department, ph.prompt_complexity
),
dept_totals AS (
    SELECT department, SUM(prompt_count) AS total
    FROM dept_complexity
    GROUP BY department
)
SELECT
    dc.department,
    dc.prompt_complexity,
    dc.prompt_count,
    ROUND(dc.prompt_count * 100.0 / dt.total, 2)            AS complexity_share_pct,
    DENSE_RANK() OVER (
        PARTITION BY dc.prompt_complexity
        ORDER BY dc.prompt_count DESC
    )                                                       AS complexity_rank
FROM dept_complexity dc
INNER JOIN dept_totals dt ON dc.department = dt.department
ORDER BY dc.department,
    CASE dc.prompt_complexity
        WHEN 'Simple' THEN 1 WHEN 'Medium' THEN 2 WHEN 'Complex' THEN 3
    END;
WITH quarterly_cat AS (
    SELECT
        pc.category_name,
        DATE_TRUNC('quarter', ph.created_at)                AS quarter,
        COUNT(ph.prompt_id)                                 AS quarterly_prompts
    FROM prompt_history ph
    INNER JOIN prompt_categories pc ON ph.category_id = pc.category_id
    GROUP BY pc.category_name, DATE_TRUNC('quarter', ph.created_at)
)
SELECT
    category_name,
    TO_CHAR(quarter, '"Q"Q YYYY')                           AS quarter,
    quarterly_prompts,
    LAG(quarterly_prompts) OVER (PARTITION BY category_name ORDER BY quarter)
                                                            AS prev_quarter,
    ROUND(
        (quarterly_prompts - LAG(quarterly_prompts) OVER
            (PARTITION BY category_name ORDER BY quarter)) * 100.0
        / NULLIF(LAG(quarterly_prompts) OVER
            (PARTITION BY category_name ORDER BY quarter), 0),
        2
    )                                                       AS qoq_growth_pct
FROM quarterly_cat
ORDER BY category_name, quarter;
