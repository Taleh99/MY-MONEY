import customtkinter as ctk
from tkinter import ttk, messagebox
import calendar
from datetime import datetime
import json
import os

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "transactions.json")

class FinanceApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("My Money")
        self.geometry("1400x760")
        self.minsize(1200, 700)

        self.bg_color = "#071120"
        self.configure(fg_color=self.bg_color)

        self.transactions = []

        self.categories = [
            "Bills", "Shopping", "Transport",
            "Entertainment", "Food", "Other"
        ]

        self.months = {
            "January": 1, "February": 2, "March": 3,
            "April": 4, "May": 5, "June": 6,
            "July": 7, "August": 8, "September": 9,
            "October": 10, "November": 11, "December": 12
        }

        self.years = [str(i) for i in range(2025, 2031)]

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.create_sidebar()
        self.create_main_area()

        # Məlumatları yüklə
        self.load_data()

        # Bağlananda saxla
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        self.save_data()
        self.destroy()

    def save_data(self):
        data = []
        for tx in self.transactions:
            data.append({
                "id": tx["id"],
                "sort_date": tx["sort_date"].strftime("%Y-%m-%d"),
                "date": tx["date"],
                "type": tx["type"],
                "category": tx["category"],
                "amount": tx["amount"]
            })
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load_data(self):
        if not os.path.exists(DATA_FILE):
            return
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            for tx in data:
                tx["sort_date"] = datetime.strptime(tx["sort_date"], "%Y-%m-%d")
                self.transactions.append(tx)
            self.refresh_table()
            self.update_cards()
        except Exception:
            pass

    def update_days(self, event=None):
        month_name = self.month_combo.get()
        year = int(self.year_combo.get())
        month_number = self.months[month_name]
        total_days = calendar.monthrange(year, month_number)[1]
        days = [str(i).zfill(2) for i in range(1, total_days + 1)]
        current_day = self.day_combo.get()
        self.day_combo.configure(values=days)
        if current_day in days:
            self.day_combo.set(current_day)
        else:
            self.day_combo.set(days[-1])

    def create_sidebar(self):

        self.sidebar = ctk.CTkFrame(
            self, width=340, corner_radius=25,
            fg_color="#18263D", border_width=2, border_color="#4DFFB8"
        )
        self.sidebar.grid(row=0, column=0, padx=20, pady=20, sticky="ns")

        ctk.CTkLabel(self.sidebar, text="New Transaction",
                     font=("Arial", 32, "bold"), text_color="white").pack(pady=(30, 20))

        ctk.CTkLabel(self.sidebar, text="Transaction Type:",
                     font=("Arial", 20), text_color="#FFFFFF").pack(anchor="w", padx=25)

        type_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        type_frame.pack(fill="x", padx=25, pady=(10, 20))

        self.transaction_type = ctk.StringVar(value="Expense")

        ctk.CTkRadioButton(type_frame, text="Expense", variable=self.transaction_type,
                           value="Expense", font=("Arial", 16), text_color="white",
                           fg_color="#FF5C5C", border_color="#FF5C5C",
                           command=self.on_type_change).pack(side="left", padx=(0, 20))

        ctk.CTkRadioButton(type_frame, text="Income", variable=self.transaction_type,
                           value="Income", font=("Arial", 16), text_color="white",
                           fg_color="#52F2BE", border_color="#52F2BE",
                           command=self.on_type_change).pack(side="left")

        ctk.CTkLabel(self.sidebar, text="Amount ($):",
                     font=("Arial", 20), text_color="#FFFFFF").pack(anchor="w", padx=25)

        self.amount_entry = ctk.CTkEntry(
            self.sidebar, height=52, corner_radius=16,
            border_width=3, border_color="#63FFD1",
            fg_color="#2B2B2B", font=("Arial", 18)
        )
        self.amount_entry.pack(fill="x", padx=25, pady=(12, 20))

        ctk.CTkLabel(self.sidebar, text="Category:",
                     font=("Arial", 20), text_color="#FFFFFF").pack(anchor="w", padx=25)

        self.category_combo = ctk.CTkComboBox(
            self.sidebar, values=self.categories, height=45,
            corner_radius=12, font=("Arial", 16),
            button_color="#65779B", border_color="#63FFD1", border_width=2
        )
        self.category_combo.pack(fill="x", padx=25, pady=(12, 20))
        self.category_combo.set("Bills")

        ctk.CTkLabel(self.sidebar, text="Select Date:",
                     font=("Arial", 22, "bold"), text_color="white").pack(anchor="w", padx=25)

        date_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        date_frame.pack(fill="x", padx=20, pady=20)

        self.day_combo = ctk.CTkComboBox(
            date_frame, values=[str(i).zfill(2) for i in range(1, 32)], width=75, height=42)
        self.day_combo.grid(row=0, column=0, padx=5)

        self.month_combo = ctk.CTkComboBox(
            date_frame, values=list(self.months.keys()), width=125, height=42,
            command=self.update_days)
        self.month_combo.grid(row=0, column=1, padx=5)

        self.year_combo = ctk.CTkComboBox(
            date_frame, values=self.years, width=90, height=42, command=self.update_days)
        self.year_combo.grid(row=0, column=2, padx=5)

        self.day_combo.set("01")
        self.month_combo.set("January")
        self.year_combo.set("2025")

        ctk.CTkButton(
            self.sidebar, text="Save Transaction ✦", height=58, corner_radius=18,
            fg_color="#52F2BE", hover_color="#8CFFE0", text_color="black",
            font=("Arial", 22, "bold"), border_width=2, border_color="#CFFFF1",
            command=self.add_transaction
        ).pack(fill="x", padx=25, pady=25)

    def on_type_change(self):
        t = self.transaction_type.get()
        if t == "Income":
            self.category_combo.configure(values=["Salary", "Freelance", "Investment", "Other Income"])
            self.category_combo.set("Salary")
        else:
            self.category_combo.configure(values=self.categories)
            self.category_combo.set("Bills")

    def create_main_area(self):

        self.main_frame = ctk.CTkFrame(
            self, fg_color="#0C182B", corner_radius=25,
            border_width=1, border_color="#2AF5C2"
        )
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=(0, 20), pady=20)
        self.main_frame.grid_rowconfigure(0, weight=0)
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#071120", foreground="white",
                        fieldbackground="#071120", rowheight=42, font=("Arial", 15))
        style.configure("Treeview.Heading", background="#D7B58A",
                        foreground="black", font=("Arial", 17, "bold"))
        style.map("Treeview", background=[("selected", "#1a3a5c")])

        # FILTER FRAME
        filter_frame = ctk.CTkFrame(self.main_frame, fg_color="#18263D",
                                    corner_radius=14, border_width=1, border_color="#4DFFB8")
        filter_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(15, 0))

        ctk.CTkLabel(filter_frame, text="📅  Date Range Filter",
                     font=("Arial", 17, "bold"), text_color="white").grid(
            row=0, column=0, columnspan=10, padx=15, pady=(10, 6), sticky="w")

        ctk.CTkLabel(filter_frame, text="From:", font=("Arial", 15),
                     text_color="#AAFFDD").grid(row=1, column=0, padx=(15, 5), pady=(0, 12))

        self.filter_from_day = ctk.CTkComboBox(
            filter_frame, values=[str(i).zfill(2) for i in range(1, 32)], width=65, height=36)
        self.filter_from_day.grid(row=1, column=1, padx=4)
        self.filter_from_day.set("01")

        self.filter_from_month = ctk.CTkComboBox(
            filter_frame, values=list(self.months.keys()), width=115, height=36)
        self.filter_from_month.grid(row=1, column=2, padx=4)
        self.filter_from_month.set("January")

        self.filter_from_year = ctk.CTkComboBox(
            filter_frame, values=self.years, width=85, height=36)
        self.filter_from_year.grid(row=1, column=3, padx=4)
        self.filter_from_year.set("2025")

        ctk.CTkLabel(filter_frame, text="To:", font=("Arial", 15),
                     text_color="#AAFFDD").grid(row=1, column=4, padx=(18, 5))

        self.filter_to_day = ctk.CTkComboBox(
            filter_frame, values=[str(i).zfill(2) for i in range(1, 32)], width=65, height=36)
        self.filter_to_day.grid(row=1, column=5, padx=4)
        self.filter_to_day.set("31")

        self.filter_to_month = ctk.CTkComboBox(
            filter_frame, values=list(self.months.keys()), width=115, height=36)
        self.filter_to_month.grid(row=1, column=6, padx=4)
        self.filter_to_month.set("December")

        self.filter_to_year = ctk.CTkComboBox(
            filter_frame, values=self.years, width=85, height=36)
        self.filter_to_year.grid(row=1, column=7, padx=4)
        self.filter_to_year.set("2030")

        ctk.CTkButton(filter_frame, text="Apply ✔", width=100, height=36,
                      fg_color="#52F2BE", hover_color="#8CFFE0", text_color="black",
                      font=("Arial", 14, "bold"), corner_radius=10,
                      command=self.apply_filter).grid(row=1, column=8, padx=(14, 4))

        ctk.CTkButton(filter_frame, text="Reset ✕", width=90, height=36,
                      fg_color="#3a3a5c", hover_color="#5a5a8c", text_color="white",
                      font=("Arial", 14, "bold"), corner_radius=10,
                      command=self.reset_filter).grid(row=1, column=9, padx=(4, 15))

        # TABLE FRAME
        table_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        table_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(10, 0))
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        self.table = ttk.Treeview(
            table_frame,
            columns=("ID", "Date", "Type", "Category", "Amount"),
            show="headings"
        )
        self.table.heading("ID", text="ID")
        self.table.heading("Date", text="Date")
        self.table.heading("Type", text="Type")
        self.table.heading("Category", text="Category")
        self.table.heading("Amount", text="Amount ($)")
        self.table.column("ID", width=60, anchor="center")
        self.table.column("Date", width=200, anchor="center")
        self.table.column("Type", width=120, anchor="center")
        self.table.column("Category", width=220, anchor="center")
        self.table.column("Amount", width=220, anchor="center")
        self.table.grid(row=0, column=0, sticky="nsew")

        self.table.tag_configure("income", foreground="#52F2BE")
        self.table.tag_configure("expense", foreground="#FF7C7C")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.table.yview)
        self.table.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="ns")

        button_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        button_frame.grid(row=2, column=0, sticky="w", padx=20, pady=(0, 10))

        ctk.CTkButton(
            button_frame, text="Delete Selected 🗑", width=210, height=50,
            fg_color="#FF5C5C", hover_color="#FF8B8B", font=("Arial", 18, "bold"),
            corner_radius=14, border_width=2, border_color="#FFD0D0",
            command=self.delete_transaction
        ).pack(side="left", padx=10)

        cards_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        cards_frame.grid(row=3, column=0, sticky="ew", padx=20, pady=(0, 20))
        cards_frame.grid_columnconfigure((0, 1, 2), weight=1)

        self.income_card = self.create_card(cards_frame, "Total Income", "0.00 $", "#52F2BE")
        self.income_card.grid(row=0, column=0, padx=12, sticky="ew")

        self.expense_card = self.create_card(cards_frame, "Total Expense", "0.00 $", "#FF5C5C")
        self.expense_card.grid(row=0, column=1, padx=12, sticky="ew")

        self.balance_card = self.create_card(cards_frame, "Total Balance", "0.00 $", "#52F2BE")
        self.balance_card.grid(row=0, column=2, padx=12, sticky="ew")

    def create_card(self, parent, title, amount, color):
        frame = ctk.CTkFrame(parent, height=135, corner_radius=22,
                             fg_color="#18263D", border_width=2, border_color=color)
        frame.grid_propagate(False)
        ctk.CTkLabel(frame, text=title, font=("Arial", 22), text_color="#FFFFFF").pack(pady=(20, 10))
        amount_label = ctk.CTkLabel(frame, text=amount, font=("Arial", 38, "bold"), text_color=color)
        amount_label.pack()
        frame.amount_label = amount_label
        return frame

    def add_transaction(self):
        amount_str = self.amount_entry.get().strip()

        if amount_str == "":
            messagebox.showwarning("Error", "Please enter amount.")
            return
        try:
            amount = float(amount_str)
        except ValueError:
            messagebox.showerror("Error", "Amount must be a number.")
            return
        if amount <= 0:
            messagebox.showerror("Error", "Amount must be greater than zero.")
            return

        category = self.category_combo.get().strip()
        transaction_type = self.transaction_type.get()

        if category == "":
            messagebox.showwarning("Error", "Please select a category.")
            return

        day = self.day_combo.get()
        month_name = self.month_combo.get()
        year = self.year_combo.get()

        month_num = self.months[month_name]
        sort_date = datetime(int(year), month_num, int(day))
        date_display = f"{day} {month_name[:3]} {year}"

        self.transactions.append({
            "id": len(self.transactions) + 1,
            "sort_date": sort_date,
            "date": date_display,
            "type": transaction_type,
            "category": category,
            "amount": amount
        })

        self.save_data()
        self.refresh_table()
        self.update_cards()
        self.amount_entry.delete(0, "end")

    def get_filter_dates(self):
        try:
            from_date = datetime(
                int(self.filter_from_year.get()),
                self.months[self.filter_from_month.get()],
                int(self.filter_from_day.get())
            )
            to_date = datetime(
                int(self.filter_to_year.get()),
                self.months[self.filter_to_month.get()],
                int(self.filter_to_day.get())
            )
            return from_date, to_date
        except Exception:
            return None, None

    def apply_filter(self):
        self.refresh_table()
        self.update_cards()

    def reset_filter(self):
        self.filter_from_day.set("01")
        self.filter_from_month.set("January")
        self.filter_from_year.set("2025")
        self.filter_to_day.set("31")
        self.filter_to_month.set("December")
        self.filter_to_year.set("2030")
        self.refresh_table()
        self.update_cards()

    def filtered_transactions(self):
        from_date, to_date = self.get_filter_dates()
        if from_date is None or to_date is None:
            return self.transactions
        return [t for t in self.transactions if from_date <= t["sort_date"] <= to_date]

    def refresh_table(self):
        for item in self.table.get_children():
            self.table.delete(item)

        groups = {}
        for tx in self.filtered_transactions():
            key = (tx["sort_date"], tx["type"], tx["category"])
            if key not in groups:
                groups[key] = {"sort_date": tx["sort_date"], "date": tx["date"],
                               "type": tx["type"], "category": tx["category"], "amount": 0.0}
            groups[key]["amount"] += tx["amount"]

        sorted_groups = sorted(groups.values(), key=lambda x: x["sort_date"])

        for i, grp in enumerate(sorted_groups, start=1):
            tag = "income" if grp["type"] == "Income" else "expense"
            self.table.insert("", "end", iid=f"row_{i}",
                              values=(i, grp["date"], grp["type"],
                                      grp["category"], f"{grp['amount']:.2f} $"),
                              tags=(tag,))

    def delete_transaction(self):
        selected = self.table.selection()
        if not selected:
            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete {len(selected)} transaction(s)?\nThis cannot be undone."
        )
        if not confirm:
            return

        groups = {}
        for tx in self.transactions:
            key = (tx["sort_date"], tx["type"], tx["category"])
            if key not in groups:
                groups[key] = {"sort_date": tx["sort_date"], "date": tx["date"],
                               "type": tx["type"], "category": tx["category"], "amount": 0.0}
            groups[key]["amount"] += tx["amount"]

        sorted_groups = sorted(groups.values(), key=lambda x: x["sort_date"])

        keys_to_delete = set()
        for item in selected:
            idx = int(item.split("_")[1]) - 1
            grp = sorted_groups[idx]
            keys_to_delete.add((grp["sort_date"], grp["type"], grp["category"]))

        self.transactions = [
            t for t in self.transactions
            if (t["sort_date"], t["type"], t["category"]) not in keys_to_delete
        ]

        self.save_data()
        self.refresh_table()
        self.update_cards()

    def update_cards(self):
        total_income = 0.0
        total_expense = 0.0

        for tx in self.filtered_transactions():
            if tx["type"] == "Income":
                total_income += tx["amount"]
            else:
                total_expense += tx["amount"]

        balance = total_income - total_expense

        self.income_card.amount_label.configure(text=f"{total_income:.2f} $")
        self.expense_card.amount_label.configure(text=f"{total_expense:.2f} $")

        balance_color = "#52F2BE" if balance >= 0 else "#FF5C5C"
        self.balance_card.amount_label.configure(
            text=f"{balance:.2f} $",
            text_color=balance_color
        )

if __name__ == "__main__":
    app = FinanceApp()
    app.mainloop()