***Claza Retail Sales Analysis***

**Project Overview:**

This project analyzes two years of synthetic transaction data modeled on Claza, a footwear retail store in Chennai, drawing on firsthand experience working there as a Sales Associate (2021–2025). The goal was to answer 10 real business questions a retail analyst would be asked to investigate, using SQL for data extraction and analysis, and Python for visualization.

**Tools used:** MySQL, Python (pandas, matplotlib, seaborn), Jupyter Notebook

**Dataset:**
        800 customers, 60 products across 5 categories (Sandals, Sneakers, Formal, Sports, Kids), ~1,385 transactions spanning April 2024–March 2026. Synthetic data was generated with realistic seasonality, gender-based category tendencies, and repeat-purchase patterns to mirror how a real footwear store actually behaves.

**Key Findings:**

**Product & Revenue:**
Sneakers and Sandals are the top-performing categories; Kids products consistently underperform.
Revenue is accelerating — cumulative revenue reached ₹3.86M by the end of the period, with growth speeding up in later months rather than slowing down.

**Customer Retention:**
69.5% of customers never return after their first purchase — a significant retention gap.
Repeat customers return anywhere from 15–120 days after their first purchase, with no single dominant window, suggesting multiple touchpoints (30/60/90-day reminders) would be more effective than a single follow-up.

**Discounting Strategy:**
Discounts do not drive additional volume — full-price purchases account for the highest share of units sold.
Deeper discounts significantly erode profit margin (45.2% at no discount vs. 30.9% at heavy discount), suggesting discounting should be reserved for inventory clearance rather than used as a general sales driver.

**Gender-Based Behavior:**
Average spend and purchase frequency are nearly identical between male and female customers — gender doesn't predict customer value.
However, category preference differs sharply: female customers favor Sandals and Kids' footwear, while male customers favor Sports and Formal — a clear signal for gender-informed marketing and inventory planning.

**Business Recommendations:**

**1.** Invest in a structured retention campaign (multi-stage reminders) to convert more of the 69.5% one-time buyers into repeat customers.

**2.** Reassess discount strategy — use discounts for clearance rather than as a volume driver, given the clear margin cost with no offsetting volume gain.

**3.** Tailor category-level marketing by gender rather than a one-size-fits-all approach, while keeping retention/engagement messaging gender-neutral.

**4.** Expand seasonal inventory planning for Formal and Sports categories ahead of Q4 demand.
