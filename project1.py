import json
import os
from datetime import datetime

DATA_FILE = os.path.join(os.path.dirname(__file__), "budget_data.json")


def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE) as f:
            return json.load(f)
    return {"transactions": [], "balance": 0.0}


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


def add_transaction(data, amount, description, t_type):
    data["transactions"].append({
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "type": t_type,
        "amount": amount,
        "description": description,
    })
    if t_type == "income":
        data["balance"] += amount
    else:
        data["balance"] -= amount


def show_summary(data):
    print("\n" + "=" * 40)
    print(f"  BALANCE: ${data['balance']:.2f}")
    print("=" * 40)
    if not data["transactions"]:
        print("  No transactions yet.")
    else:
        print(f"  {'Date':<17} {'Type':<8} {'Amount':>8}  Description")
        print("  " + "-" * 55)
        for t in data["transactions"][-10:]:
            sign = "+" if t["type"] == "income" else "-"
            print(f"  {t['date']:<17} {t['type']:<8} {sign}${t['amount']:>7.2f}  {t['description']}")
    print()


def main():
    print("\n=== Budget Tracker ===")
    data = load_data()

    while True:
        print("1) Add income")
        print("2) Add expense")
        print("3) View summary")
        print("4) Quit")
        choice = input("\nChoice: ").strip()

        if choice == "1":
            try:
                amount = float(input("Amount: $"))
                desc = input("Description: ").strip() or "Income"
                add_transaction(data, amount, desc, "income")
                save_data(data)
                print(f"  Added income: +${amount:.2f}")
            except ValueError:
                print("  Invalid amount.")

        elif choice == "2":
            try:
                amount = float(input("Amount: $"))
                desc = input("Description: ").strip() or "Expense"
                add_transaction(data, amount, desc, "expense")
                save_data(data)
                print(f"  Added expense: -${amount:.2f}")
            except ValueError:
                print("  Invalid amount.")

        elif choice == "3":
            show_summary(data)

        elif choice == "4":
            print("Goodbye!")
            break

        else:
            print("  Invalid choice.")

        print()


if __name__ == "__main__":
    main()