import sqlite3
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

# ---------------- DATABASE SETUP ----------------
conn = sqlite3.connect("expenses.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amount REAL,
    category TEXT,
    date TEXT,
    note TEXT
)
""")
conn.commit()

# ---------------- FUNCTIONS ----------------
def add_expense(amount, category, note=""):
    date = datetime.now().strftime("%Y-%m-%d")
    cursor.execute("INSERT INTO expenses (amount, category, date, note) VALUES (?, ?, ?, ?)",
                   (amount, category, date, note))
    conn.commit()
    print("✅ Expense Added Successfully!")

def view_expenses():
    df = pd.read_sql("SELECT * FROM expenses", conn)
    if df.empty:
        print("⚠️ No expenses recorded yet.")
    else:
        print(df)

def monthly_summary():
    df = pd.read_sql("SELECT * FROM expenses", conn)
    if df.empty:
        print("⚠️ No expenses recorded yet.")
        return
    df["date"] = pd.to_datetime(df["date"])
    df["month"] = df["date"].dt.to_period("M")
    summary = df.groupby(["month", "category"])["amount"].sum().unstack(fill_value=0)
    print(summary)

    # Plot pie chart for last month
    last_month = df["month"].max()
    month_data = df[df["month"] == last_month].groupby("category")["amount"].sum()
    if not month_data.empty:
        month_data.plot(kind="pie", autopct="%1.1f%%", figsize=(6, 6))
        plt.title(f"Expenses Breakdown - {last_month}")
        plt.ylabel("")
        plt.show()

# ---------------- MENU ----------------
def main():
    while True:
        print("\n📌 Smart Expense Tracker")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Monthly Summary & Chart")
        print("4. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            try:
                amount = float(input("Enter amount: "))
                category = input("Enter category (Food, Travel, Bills, etc.): ")
                note = input("Enter note (optional): ")
                add_expense(amount, category, note)
            except ValueError:
                print("⚠️ Please enter a valid number for amount.")
        
        elif choice == "2":
            view_expenses()

        elif choice == "3":
            monthly_summary()

        elif choice == "4":
            print("👋 Exiting... Have a great day!")
            break
        else:
            print("⚠️ Invalid choice. Try again.")

# ---------------- RUN APP ----------------
if __name__ == "__main__":
    main()
