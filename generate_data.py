"""
Synthetic Data Generator - Footwear Retail Store (Claza-style)
Generates: customers.csv, products.csv, transactions.csv

Design goals (so the 8 business questions have real signal, not noise):
- Q2 Seasonality      -> category-specific monthly demand multipliers
- Q3 Repeat customers -> ~55% of customers get only 1 order, ~45% get 2+ orders
- Q4 Purchase gap     -> repeat customers' 2nd order is spaced realistically (15-120 days later)
- Q5/Q6 Revenue trend -> gentle month-over-month growth + occasional festive spikes
- Q7 Discounts        -> discounts cluster around sale periods (higher %, higher volume)
- Q8 Gender behavior  -> male vs female customers skew toward different categories
                          and have different average basket sizes
"""

import csv
import random
from datetime import date, timedelta
from faker import Faker

fake = Faker("en_IN")
random.seed(42)
Faker.seed(42)

# ---------------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------------
NUM_CUSTOMERS = 800
NUM_PRODUCTS = 60
START_DATE = date(2024, 4, 1)   # 2 years of data
END_DATE = date(2026, 3, 31)

CATEGORIES = ["Sandals", "Sneakers", "Formal", "Sports", "Kids"]

# Relative popularity of each category by gender (used to bias product choice)
# Values are weights, not percentages.
GENDER_CATEGORY_WEIGHTS = {
    "Male":   {"Sandals": 3, "Sneakers": 5, "Formal": 4, "Sports": 5, "Kids": 1},
    "Female": {"Sandals": 5, "Sneakers": 4, "Formal": 2, "Sports": 2, "Kids": 2},
}

# Seasonality multiplier per category per month (1 = baseline demand)
# April/May: summer -> Sandals up. Oct/Nov: festive/wedding season -> Formal, Sneakers up.
# Dec/Jan: winter/New Year -> Sports, Sneakers slightly up. June: monsoon -> Sandals dip.
SEASONALITY = {
    "Sandals":  {4: 1.6, 5: 1.7, 6: 0.7, 7: 0.8, 8: 0.9, 9: 1.0, 10: 1.1, 11: 1.0, 12: 0.8, 1: 0.8, 2: 1.0, 3: 1.2},
    "Sneakers": {4: 1.0, 5: 1.0, 6: 1.0, 7: 1.0, 8: 1.0, 9: 1.1, 10: 1.3, 11: 1.4, 12: 1.2, 1: 1.1, 2: 1.0, 3: 1.0},
    "Formal":   {4: 0.9, 5: 0.9, 6: 0.9, 7: 0.9, 8: 1.0, 9: 1.2, 10: 1.6, 11: 1.8, 12: 1.3, 1: 1.0, 2: 0.9, 3: 1.0},
    "Sports":   {4: 1.1, 5: 1.1, 6: 1.0, 7: 1.0, 8: 1.0, 9: 1.0, 10: 1.0, 11: 1.0, 12: 1.2, 1: 1.3, 2: 1.1, 3: 1.0},
    "Kids":     {4: 1.0, 5: 1.0, 6: 0.9, 7: 0.9, 8: 0.9, 9: 1.1, 10: 1.3, 11: 1.3, 12: 1.1, 1: 1.0, 2: 1.0, 3: 1.0},
}

PRODUCT_NAME_TEMPLATES = {
    "Sandals":  ["Casual Slide", "Comfort Flip Flop", "Strap Sandal", "Walking Sandal"],
    "Sneakers": ["Running Sneaker", "Casual Sneaker", "Canvas Shoe", "Trainer"],
    "Formal":   ["Oxford Shoe", "Derby Shoe", "Loafer", "Formal Slip-on"],
    "Sports":   ["Training Shoe", "Cricket Shoe", "Badminton Shoe", "Gym Shoe"],
    "Kids":     ["Kids School Shoe", "Kids Sandal", "Kids Sneaker", "Kids Sports Shoe"],
}

SIZES = list(range(6, 12))  # UK sizes 6-11

# ---------------------------------------------------------------------------
# 1. CUSTOMERS
# ---------------------------------------------------------------------------
customers = []
for cid in range(1, NUM_CUSTOMERS + 1):
    gender = random.choice(["Male", "Female"])
    name = fake.name_male() if gender == "Male" else fake.name_female()
    join_date = fake.date_between(start_date=START_DATE, end_date=END_DATE)
    customers.append({
        "customer_id": cid,
        "name": name,
        "gender": gender,
        "join_date": join_date.isoformat(),
    })

with open("customers.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["customer_id", "name", "gender", "join_date"])
    writer.writeheader()
    writer.writerows(customers)

# ---------------------------------------------------------------------------
# 2. PRODUCTS
# ---------------------------------------------------------------------------
products = []
pid = 1
for category in CATEGORIES:
    per_category = NUM_PRODUCTS // len(CATEGORIES)
    for _ in range(per_category):
        base_name = random.choice(PRODUCT_NAME_TEMPLATES[category])
        cost_price = round(random.uniform(400, 1800), 2)
        markup = random.uniform(1.4, 2.2)
        selling_price = round(cost_price * markup, 2)
        products.append({
            "product_id": pid,
            "product_name": f"{base_name} #{pid}",
            "category": category,
            "size": random.choice(SIZES),
            "cost_price": cost_price,
            "selling_price": selling_price,
        })
        pid += 1

with open("products.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["product_id", "product_name", "category", "size", "cost_price", "selling_price"])
    writer.writeheader()
    writer.writerows(products)

products_by_category = {}
for p in products:
    products_by_category.setdefault(p["category"], []).append(p)


def weighted_category_choice(gender):
    weights = GENDER_CATEGORY_WEIGHTS[gender]
    categories = list(weights.keys())
    wts = list(weights.values())
    return random.choices(categories, weights=wts, k=1)[0]


def random_date_with_seasonality():
    """Pick a random date, weighting months by an average seasonality factor."""
    total_days = (END_DATE - START_DATE).days
    while True:
        offset = random.randint(0, total_days)
        d = START_DATE + timedelta(days=offset)
        avg_seasonal_weight = sum(SEASONALITY[c][d.month] for c in CATEGORIES) / len(CATEGORIES)
        # Accept/reject sampling so higher-demand months get more transactions overall
        if random.random() < avg_seasonal_weight / 1.8:
            return d


def pick_product_for(gender, on_date):
    """Pick a category using gender weights adjusted by that category's seasonality for the month,
    then pick a random product within it."""
    weights = GENDER_CATEGORY_WEIGHTS[gender]
    categories = list(weights.keys())
    adj_weights = [weights[c] * SEASONALITY[c][on_date.month] for c in categories]
    category = random.choices(categories, weights=adj_weights, k=1)[0]
    return random.choice(products_by_category[category])


def discount_for(on_date):
    """Higher discounts and higher chance of discount during festive sale months (Oct-Nov) and Jan."""
    sale_months = {10, 11, 1}
    if on_date.month in sale_months:
        return round(random.choice([0, 0, 0.1, 0.15, 0.2, 0.25]), 2)
    return round(random.choice([0, 0, 0, 0, 0.05, 0.1]), 2)


# ---------------------------------------------------------------------------
# 3. TRANSACTIONS
# ---------------------------------------------------------------------------
transactions = []
tid = 1

# Decide, per customer, whether they are a repeat buyer (~45% repeat)
customer_order_counts = {}
for c in customers:
    if random.random() < 0.45:
        customer_order_counts[c["customer_id"]] = random.randint(2, 8)
    else:
        customer_order_counts[c["customer_id"]] = 1

for c in customers:
    gender = c["gender"]
    join_dt = date.fromisoformat(c["join_date"])
    num_orders = customer_order_counts[c["customer_id"]]

    order_dates = []
    first_order_date = fake.date_between(start_date=join_dt, end_date=END_DATE)
    order_dates.append(first_order_date)

    current_date = first_order_date
    for _ in range(num_orders - 1):
        gap = random.randint(15, 120)  # realistic repeat-purchase gap in days
        next_date = current_date + timedelta(days=gap)
        if next_date > END_DATE:
            break
        order_dates.append(next_date)
        current_date = next_date

    for od in order_dates:
        product = pick_product_for(gender, od)
        quantity = random.choices([1, 2, 3], weights=[75, 20, 5], k=1)[0]
        discount_pct = discount_for(od)
        transactions.append({
            "transaction_id": tid,
            "customer_id": c["customer_id"],
            "product_id": product["product_id"],
            "quantity": quantity,
            "discount_pct": discount_pct,
            "transaction_date": od.isoformat(),
        })
        tid += 1

with open("transactions.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["transaction_id", "customer_id", "product_id", "quantity", "discount_pct", "transaction_date"])
    writer.writeheader()
    writer.writerows(transactions)

print(f"Generated {len(customers)} customers, {len(products)} products, {len(transactions)} transactions.")
