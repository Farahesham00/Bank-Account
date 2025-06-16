import csv
import tkinter as tk
from tkinter import messagebox





class Transaction:
    def __init__(self, trans_type, amount, prev_balance, new_balance):
        self.trans_type = trans_type
        self.amount = amount
        self.prev_balance = prev_balance
        self.new_balance = new_balance

    def __str__(self):
        return (f"{self.trans_type}: {self.amount} EGP | "
                f"Previous Balance: {self.prev_balance} EGP"
                f" → New Balance: {self.new_balance} EGP")


class Account:
    def __init__(self, account_number , account_holder_name, initial_balance = 0):
        if initial_balance < 0:
            raise ValueError("Initial balance cannot be negative.")
        self.account_number = account_number
        self.account_holder_name = account_holder_name
        self.initial_balance = initial_balance
        self.transactions = []



    def deposit(self, amount, show_message=True):
        if amount > 0:
            prev_balance = self.initial_balance
            self.initial_balance += amount
            trans = Transaction("Deposit", amount, prev_balance, self.initial_balance)
            self.transactions.append(trans)
            if show_message:
                print("Deposit successful.")
                print(trans)

    def  withdraw(self, amount, show_message=True):
        if amount > 0 and self.initial_balance >= amount:
            prev_balance = self.initial_balance
            self.initial_balance -= amount
            trans = Transaction("withdraw", amount, prev_balance, self.initial_balance)
            self.transactions.append(trans)
            if show_message:
                print(" withdraw successful.")
                print(trans)
        else:
            print('Error: Your Current Balance is less than Fund     ')

    def get_balance(self):
        return f'Your Current Balance is {self.initial_balance}'

    def display_account_info(self):
        print(f'Account Number: {self.account_number} ,'
              f' Account Holder: {self.account_holder_name}, '
              f'Current Balance: {self.initial_balance}')

    def show_transaction_history(self):
        if not self.transactions:
            print("No transactions yet.")
        else:
            print("\n--- Transaction History ---")
            for t in self.transactions:
                print(t)


class SavingsAccount(Account):
    def __init__(self, account_number, account_holder_name, initial_balance=0, interest_rate=0.03):
        super().__init__(account_number, account_holder_name, initial_balance)
        self.interest_rate = interest_rate

    def deposit(self, amount):
        if amount > 0:
            interest = amount * self.interest_rate
            total = amount + interest
            prev_balance = self.initial_balance
            self.initial_balance += total
            trans = Transaction("Deposit (with Interest)", total, prev_balance, self.initial_balance)
            self.transactions.append(trans)
        else:
            raise ValueError("Deposit amount must be positive.")





class CheckingAccount(Account):
    def __init__(self, account_number, account_holder_name, initial_balance=0, overdraft_limit=500):
        super().__init__(account_number, account_holder_name, initial_balance)
        self.overdraft_limit = overdraft_limit

    def withdraw(self, amount):
        if amount > 0 and self.initial_balance + self.overdraft_limit >= amount:
            prev_balance = self.initial_balance
            self.initial_balance -= amount
            trans = Transaction("Withdrawal", amount, prev_balance, self.initial_balance)
            self.transactions.append(trans)
            print(" Withdrawal successful.")
            print(trans)
        else:
            print(" Error: Exceeded overdraft limit or invalid amount.")

def save_accounts_to_csv(accounts, filename='accounts.csv'):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['account_number', 'account_holder_name', 'balance', 'account_type'])
        for acc in accounts.values():
            writer.writerow([acc.account_number, acc.account_holder_name, acc.initial_balance, acc.__class__.__name__])


def load_accounts_from_csv(filename='accounts.csv'):
    accounts = {}
    try:
        with open(filename, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                acc_number = row['account_number']
                name = row['account_holder_name']
                balance = float(row['balance'])
                acc_type = row['account_type']

                if acc_type == 'SavingsAccount':
                    acc = SavingsAccount(acc_number, name, balance)
                elif acc_type == 'CheckingAccount':
                    acc = CheckingAccount(acc_number, name, balance)
                else:
                    acc = Account(acc_number, name, balance)

                accounts[acc_number] = acc
    except FileNotFoundError:
        pass
    return accounts


accounts = load_accounts_from_csv()
save_accounts_to_csv(accounts)


class BankGUI:
    def __init__(self, accounts):
        self.accounts = accounts
        self.current_account = None

        self.window = tk.Tk()
        self.window.title("Banking System")

        self.create_login_screen()

    def create_login_screen(self):
        self.clear_window()
        tk.Label(self.window, text="Welcome to the Bank!", font=('Arial', 16)).pack(pady=10)
        tk.Button(self.window, text="Sign Up", width=20, command=self.choose_account_type_screen).pack(pady=5)
        tk.Button(self.window, text="Sign In", width=20, command=self.sign_in_screen).pack(pady=5)

    def choose_account_type_screen(self):
        self.clear_window()
        tk.Label(self.window, text="Choose Account Type", font=('Arial', 14)).pack(pady=10)
        tk.Button(self.window, text="Normal Account", width=20, command=lambda: self.sign_up_screen("normal")).pack(pady=5)
        tk.Button(self.window, text="Savings Account", width=20, command=lambda: self.sign_up_screen("savings")).pack(pady=5)
        tk.Button(self.window, text="Checking Account", width=20, command=lambda: self.sign_up_screen("checking")).pack(pady=5)
        tk.Button(self.window, text="Back", width=20, command=self.create_login_screen).pack(pady=20)

    def sign_up_screen(self, acc_type):
        self.clear_window()
        tk.Label(self.window, text=f"Sign Up - {acc_type.capitalize()} Account", font=('Arial', 14)).pack(pady=10)

        tk.Label(self.window, text="Account Number:").pack()
        acc_entry = tk.Entry(self.window)
        acc_entry.pack()

        tk.Label(self.window, text="Name:").pack()
        name_entry = tk.Entry(self.window)
        name_entry.pack()

        tk.Label(self.window, text="Initial Balance:").pack()
        balance_entry = tk.Entry(self.window)
        balance_entry.pack()
        tk.Button(self.window, text="Back", width=10, command=self.choose_account_type_screen).pack(pady=20)


        def create_account():
            acc_num = acc_entry.get()
            name = name_entry.get()
            try:
                balance = float(balance_entry.get())
                if not name.replace(" ", "").isalpha():
                    raise ValueError("Name must contain letters only.")

                if acc_type == "savings":
                    account = SavingsAccount(acc_num, name, balance)
                elif acc_type == "checking":
                    account = CheckingAccount(acc_num, name, balance)
                else:
                    account = Account(acc_num, name, balance)

                self.accounts[acc_num] = account
                self.current_account = account
                messagebox.showinfo("Success", f"{acc_type.capitalize()} account created successfully!")
                self.create_main_menu()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(self.window, text="Create Account", command=create_account).pack(pady=10)

    def sign_in_screen(self):
        self.clear_window()
        tk.Label(self.window, text="Sign In", font=('Arial', 14)).pack(pady=10)

        tk.Label(self.window, text="Account Number:").pack()
        acc_entry = tk.Entry(self.window)
        acc_entry.pack()

        tk.Label(self.window, text="Name:").pack()
        name_entry = tk.Entry(self.window)
        name_entry.pack()

        def login():
            acc_num = acc_entry.get()
            name = name_entry.get()
            if acc_num in self.accounts and self.accounts[acc_num].account_holder_name == name:
                self.current_account = self.accounts[acc_num]
                messagebox.showinfo("Success", "Logged in successfully!")
                self.create_main_menu()
            else:
                messagebox.showerror("Error", "Account not found or incorrect name.")

        tk.Button(self.window, text="Login", command=login).pack(pady=10)

    def create_main_menu(self):
        self.clear_window()
        tk.Label(self.window, text=f"Welcome {self.current_account.account_holder_name}!", font=('Arial', 14)).pack(pady=10)

        tk.Button(self.window, text="1. Deposit", command=self.deposit_screen).pack(pady=5)
        tk.Button(self.window, text="2. Withdraw", command=self.withdraw_screen).pack(pady=5)
        tk.Button(self.window, text="3. Check Balance", command=self.show_balance).pack(pady=5)
        tk.Button(self.window, text="4. Account Information", command=self.show_info).pack(pady=5)
        tk.Button(self.window, text="5. View Transaction History", command=self.show_transactions).pack(pady=5)
        tk.Button(self.window, text="Log Out", command=self.create_login_screen).pack(pady=10)

    def deposit_screen(self):
        self.clear_window()
        tk.Label(self.window, text="Enter amount to deposit:").pack()
        amount_entry = tk.Entry(self.window)
        amount_entry.pack()

        def deposit_action():
            try:
                amount = float(amount_entry.get())
                self.current_account.deposit(amount)  # Will auto-apply interest if it's a SavingsAccount
                messagebox.showinfo("Success", "Deposit successful.")
                self.create_main_menu()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(self.window, text="Deposit", command=deposit_action).pack(pady=10)

    def withdraw_screen(self):
        self.clear_window()
        tk.Label(self.window, text="Enter amount to withdraw:").pack()
        amount_entry = tk.Entry(self.window)
        amount_entry.pack()

        def withdraw_action():
            try:
                amount = float(amount_entry.get())
                self.current_account.withdraw(amount)
                self.create_main_menu()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(self.window, text="Withdraw", command=withdraw_action).pack(pady=10)

    def show_balance(self):
        messagebox.showinfo("Balance", self.current_account.get_balance())

    def show_info(self):
        info = (f"Account Number: {self.current_account.account_number}\n"
                f"Name: {self.current_account.account_holder_name}\n"
                f"Balance: {self.current_account.initial_balance}")
        messagebox.showinfo("Account Info", info)

    def show_transactions(self):
        if not self.current_account.transactions:
            messagebox.showinfo("Transactions", "No transactions yet.")
        else:
            history = "\n".join(str(t) for t in self.current_account.transactions)
            messagebox.showinfo("Transaction History", history)

    def clear_window(self):
        for widget in self.window.winfo_children():
            widget.destroy()

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    accounts = load_accounts_from_csv()  # Load saved accounts first
    app = BankGUI(accounts)


    # Optional: Save accounts when app closes
    def on_closing():
        save_accounts_to_csv(app.accounts)
        app.window.destroy()


    app.window.protocol("WM_DELETE_WINDOW", on_closing)
    app.run()

print("Welcome to Bank Account")
filter_account = input("Do you want to Sign in or Sign up? ").strip().lower()
if filter_account == 'sign up':
    account_type = input("Choose account type (savings/checking/normal): ").strip().lower()
    if account_type == 'normal':
        while True:
            try:
                account_number = int(input("Create a new account number: "))  # numbers only

                name = input("Enter your name: ")  # letters only
                if not name.replace(" ", "").isalpha():
                    raise ValueError("Name must contain letters only.")

                balance = int(input("Enter initial balance: "))  # numbers only
                break
            except ValueError as e:
                print("Invalid input:", e)
        account = Account(account_number, name, balance)
        accounts[account_number] = account
        print("\nAccount created successfully!\n")
        account.display_account_info()
        save_accounts_to_csv(accounts)
    elif account_type == 'savings':
        account_number = input("Create a new account number: ")
        name = input("Enter your name: ")
        balance = int(input("Enter initial balance: "))
        account = SavingsAccount(account_number, name, balance)
        accounts[account_number] = account
        print("\nSavings Account created successfully!\n")
        account.display_account_info()
        save_accounts_to_csv(accounts)
    elif account_type == 'checking':
        account_number = input("Create a new account number: ")
        name = input("Enter your name: ")
        balance = int(input("Enter initial balance: "))
        account = CheckingAccount(account_number, name, balance)
        accounts[account_number] = account
        print("\nChecking Account created successfully!\n")
        account.display_account_info()
        save_accounts_to_csv(accounts)
    else:
        print("Invalid account type.")
        exit()



elif filter_account == 'sign in':
    account_number = input("Enter your account number: ")
    name = input("Enter your name: ")
    if account_number in accounts and accounts[account_number].account_holder_name == name:
        account = accounts[account_number]
        print("\nLogged in successfully!\n")
        account.display_account_info()
    else:
        print("Account not found or incorrect name.")
        exit()


else:
    print("Invalid choice. Please restart and choose Sign in or Sign up.")
    exit()




while True:
    print("\nBank Account Menu:")
    print("1. Deposit")
    print("2. Withdraw")
    print("3. Check Balance")
    print("4. Account Information")
    print("5. View Transaction History")
    print("6. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        amount = float(input("Enter amount to deposit: "))
        account.deposit(amount)
        if isinstance(account, SavingsAccount):
            account.apply_interest()
        save_accounts_to_csv(accounts)


    elif choice == "2":
        amount = float(input("Enter amount to withdraw: "))
        account.withdraw(amount)
        save_accounts_to_csv(accounts)

    elif choice == "3":
        print(account.get_balance())

    elif choice == "4":
        account.display_account_info()

    elif choice == "5":
        account.show_transaction_history()

    elif choice == "6":
        print("Exit!")
        break

    else:
        print(" Invalid option.")

