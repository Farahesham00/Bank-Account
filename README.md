# 🏦 Banking System GUI in Python

This is a **Graphical User Interface (GUI)** based banking system built with **Python** and **Tkinter**, supporting **Normal**, **Savings**, and **Checking** accounts. It allows users to sign up, log in, deposit/withdraw money, and view account info and transaction history. Data is saved using a **CSV file** to ensure persistence between sessions.

---

## 📌 Features

- ✅ Sign Up with account type (Normal, Savings, Checking)
- ✅ Sign In using account number and name
- ✅ Deposit and Withdraw with validation
- ✅ Interest applied automatically for Savings accounts
- ✅ Transaction history logging
- ✅ Persistent storage using CSV files
- ✅ GUI-based using Tkinter
- ✅ Logout and return to welcome screen

---

## 🧠 Account Types

- **Normal Account**: Basic account with deposit/withdrawal features.
- **Savings Account**: Adds **3% interest** automatically on each deposit.
- **Checking Account**: Allows overdraft functionality.

---

## 🗂️ File Structure
banking_system/
│
├── BankAccount.py # Contains all class definitions
├── GUI.py # Contains the GUI logic
├── accounts.csv # Stores accounts data persistently
├── README.md # Project documentation
└── main.py # Main entry point



---

## 🛠️ How It Works

1. On launch, existing accounts are **loaded from `accounts.csv`**.
2. User chooses to either **Sign In** or **Sign Up**.
3. For Sign Up:
   - Enters account number, name, and initial balance.
   - Chooses account type (normal/savings/checking).
   - Account is saved and accessible later.
4. For Sign In:
   - Enters existing account number and name.
   - If correct, accesses main banking menu.
5. In the main menu, users can:
   - Deposit / Withdraw
   - View balance and account info
   - View transaction history
   - Apply interest (for savings)
   - Log out or exit
6. On exit, **accounts are saved again to the CSV file**.

---

## 💾 Data Persistence

- Accounts are stored in a CSV file named `accounts.csv`.
- When the program closes, the file is updated automatically.

---

## 📥 Requirements

- Python 3.x
- Tkinter (comes with Python)

---

## ▶️ How to Run

```bash
python main.py



