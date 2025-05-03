import sqlite3
import csv
import matplotlib.pyplot as plt
import os

# Ensure static/ folder exists
os.makedirs("static", exist_ok=True)

# Step 1: Connect and Create Table
conn = sqlite3.connect('fashion.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS fashion (
        product_id INTEGER,
        product_name TEXT,
        gender TEXT,
        category TEXT,
        pattern TEXT,
        color TEXT,
        age_group TEXT,
        season TEXT,
        price REAL,
        material TEXT,
        sales_count INTEGER,
        reviews_count INTEGER,
        average_rating REAL,
        out_of_stock_times INTEGER,
        brand TEXT,
        discount TEXT,
        last_stock_date TEXT,
        wish_list_count INTEGER,
        month_of_sale INTEGER,
        year_of_sale INTEGER
    )
''')

# Step 2: Load and Insert CSV Data
with open('fashionData.csv', 'r', encoding='utf-8-sig') as file:
    reader = csv.DictReader(file, delimiter='\t')
    for row in reader:
        cursor.execute('''
            INSERT INTO fashion (
                product_id, product_name, gender, category, pattern, color,
                age_group, season, price, material, sales_count, reviews_count,
                average_rating, out_of_stock_times, brand, discount,
                last_stock_date, wish_list_count, month_of_sale, year_of_sale
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            int(row['product_id']),
            row['product_name'],
            row['gender'],
            row['category'],
            row['pattern'],
            row['color'],
            row['age_group'],
            row['season'],
            float(row['price']),
            row['material'],
            int(row['sales_count']),
            int(row['reviews_count']),
            float(row['average_rating']),
            int(row['out_of_stock_times']),
            row['brand'],
            row['discount'],
            row['last_stock_date'],
            int(row['wish_list_count']),
            int(row['month_of_sale']),
            int(row['year_of_sale'])
        ))

conn.commit()

# Step 3: Graphs (Saved to static/)
def save_plot(filename):
    plt.tight_layout()
    plt.savefig(f'static/{filename}', facecolor='white')
    plt.clf()  # Clear for next plot

PINK = '#f4a1c2'

# 1. Top 5 Best-Selling Items
cursor.execute('''
    SELECT product_name, SUM(sales_count)
    FROM fashion
    GROUP BY product_name
    ORDER BY SUM(sales_count) DESC
    LIMIT 5
''')
data = cursor.fetchall()
names = [row[0] for row in data]
sales = [row[1] for row in data]
plt.barh(names, sales, color=PINK)
plt.xlabel("Sales Count")
plt.title("Top 5 Best-Selling Fashion Items")
plt.gca().invert_yaxis()
save_plot("top5_sales.png")

# 2. Top 5 Rated Items
cursor.execute('''
    SELECT product_name, average_rating
    FROM fashion
    ORDER BY average_rating DESC
    LIMIT 5
''')
data = cursor.fetchall()
names = [row[0] for row in data]
ratings = [row[1] for row in data]
plt.barh(names, ratings, color=PINK)
plt.xlabel("Average Rating")
plt.title("Top 5 Highest Rated Fashion Items")
plt.gca().invert_yaxis()
save_plot("top5_ratings.png")

# 3. Sales by Season
cursor.execute('''
    SELECT season, SUM(sales_count)
    FROM fashion
    GROUP BY season
''')
data = cursor.fetchall()
seasons = [row[0] for row in data]
season_sales = [row[1] for row in data]
plt.bar(seasons, season_sales, color=PINK)
plt.title("Total Sales by Season")
plt.ylabel("Sales Count")
save_plot("sales_by_season.png")

# 4. Top 5 Popular Colors
cursor.execute('''
    SELECT color, COUNT(*)
    FROM fashion
    GROUP BY color
    ORDER BY COUNT(*) DESC
    LIMIT 5
''')
data = cursor.fetchall()
colors = [row[0] for row in data]
counts = [row[1] for row in data]
plt.bar(colors, counts, color=PINK)
plt.title("Top 5 Most Frequent Colors")
save_plot("popular_colors.png")

# 5. Reviews vs Ratings
cursor.execute('''
    SELECT reviews_count, average_rating
    FROM fashion
''')
data = cursor.fetchall()
reviews = [row[0] for row in data]
ratings = [row[1] for row in data]
plt.scatter(reviews, ratings, color=PINK)
plt.title("Reviews Count vs Average Rating")
plt.xlabel("Reviews Count")
plt.ylabel("Average Rating")
plt.grid(True)
save_plot("reviews_vs_rating.png")

# 6. Price Distribution
cursor.execute('SELECT price FROM fashion')
prices = [row[0] for row in cursor.fetchall()]
plt.hist(prices, bins=10, color=PINK, edgecolor='white')
plt.title("Price Distribution of Fashion Items")
plt.xlabel("Price")
plt.ylabel("Number of Products")
save_plot("price_distribution.png")

# 7. Monthly Sales Trends
cursor.execute('''
    SELECT month_of_sale, SUM(sales_count)
    FROM fashion
    GROUP BY month_of_sale
    ORDER BY month_of_sale
''')
data = cursor.fetchall()
months = [row[0] for row in data]
monthly_sales = [row[1] for row in data]
plt.plot(months, monthly_sales, marker='o', color=PINK)
plt.title("Sales Trend by Month")
plt.xlabel("Month")
plt.ylabel("Total Sales")
plt.xticks(range(1, 13))
plt.grid(True)
save_plot("monthly_sales_trend.png")

# Final print
print("🌸 All pink-themed graphs saved in the 'static/' folder!")

# Close connection
conn.close()
