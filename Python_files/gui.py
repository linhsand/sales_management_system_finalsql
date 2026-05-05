import tkinter as tk
from tkinter import ttk, messagebox, font
from db_connection import get_connection

# ─── THEME ────────────────────────────────────────────────────────────────────
BG        = "#0f1117"
PANEL     = "#1a1d27"
CARD      = "#22263a"
ACCENT    = "#4f8ef7"
ACCENT2   = "#7c3aed"
SUCCESS   = "#22c55e"
WARNING   = "#f59e0b"
DANGER    = "#ef4444"
TEXT      = "#e8eaf0"
SUBTEXT   = "#8891a8"
BORDER    = "#2e3250"
ENTRY_BG  = "#181c2e"

NAV_W = 200

# ─── HELPERS ──────────────────────────────────────────────────────────────────
def db():
    return get_connection()

def run(query, params=(), fetch=False):
    conn = db()
    cur = conn.cursor()
    cur.execute(query, params)
    result = cur.fetchall() if fetch else None
    conn.commit()
    conn.close()
    return result

def proc(name, args):
    conn = db()
    cur = conn.cursor()
    cur.callproc(name, args)
    conn.commit()
    conn.close()

# ─── WIDGETS ──────────────────────────────────────────────────────────────────
def styled_btn(parent, text, cmd, color=ACCENT, width=14):
    b = tk.Button(parent, text=text, command=cmd,
                  bg=color, fg="white", relief="flat",
                  font=("Consolas", 10, "bold"), cursor="hand2",
                  padx=12, pady=6, width=width,
                  activebackground=color, activeforeground="white",
                  bd=0)
    b.bind("<Enter>", lambda e: b.config(bg=_lighten(color)))
    b.bind("<Leave>", lambda e: b.config(bg=color))
    return b

def _lighten(hex_color):
    mapping = {ACCENT: "#6ba3ff", ACCENT2: "#9d5cff",
               SUCCESS: "#4ade80", WARNING: "#fbbf24",
               DANGER: "#f87171", "#555": "#777"}
    return mapping.get(hex_color, hex_color)

def styled_entry(parent, width=22, show=None):
    e = tk.Entry(parent, bg=ENTRY_BG, fg=TEXT, insertbackground=TEXT,
                 relief="flat", font=("Consolas", 11),
                 highlightthickness=1, highlightbackground=BORDER,
                 highlightcolor=ACCENT, width=width)
    if show:
        e.config(show=show)
    return e

def label(parent, text, size=11, color=TEXT, bold=False):
    f = ("Consolas", size, "bold") if bold else ("Consolas", size)
    return tk.Label(parent, text=text, bg=PANEL, fg=color, font=f)

def card_label(parent, text, size=11, color=TEXT, bold=False):
    f = ("Consolas", size, "bold") if bold else ("Consolas", size)
    return tk.Label(parent, text=text, bg=CARD, fg=color, font=f)

def make_table(parent, columns, height=12):
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Dark.Treeview",
                    background=CARD, fieldbackground=CARD,
                    foreground=TEXT, rowheight=28,
                    font=("Consolas", 10))
    style.configure("Dark.Treeview.Heading",
                    background=PANEL, foreground=ACCENT,
                    font=("Consolas", 10, "bold"), relief="flat")
    style.map("Dark.Treeview",
              background=[("selected", ACCENT)],
              foreground=[("selected", "white")])

    frame = tk.Frame(parent, bg=CARD)
    sv = ttk.Scrollbar(frame, orient="vertical")
    sh = ttk.Scrollbar(frame, orient="horizontal")
    tree = ttk.Treeview(frame, columns=columns, show="headings",
                        style="Dark.Treeview", height=height,
                        yscrollcommand=sv.set, xscrollcommand=sh.set)
    sv.config(command=tree.yview)
    sh.config(command=tree.xview)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120, anchor="center")

    sv.pack(side="right", fill="y")
    sh.pack(side="bottom", fill="x")
    tree.pack(fill="both", expand=True)
    return frame, tree

def clear_tree(tree):
    for i in tree.get_children():
        tree.delete(i)

def section_title(parent, text):
    f = tk.Frame(parent, bg=PANEL)
    tk.Label(f, text=text, bg=PANEL, fg=ACCENT,
             font=("Consolas", 15, "bold")).pack(side="left")
    tk.Frame(f, bg=BORDER, height=2).pack(side="left", fill="x",
                                          expand=True, padx=(12, 0), pady=8)
    return f

# ─── PAGES ────────────────────────────────────────────────────────────────────

class DashboardPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=BG)
        self.build()

    def build(self):
        tk.Label(self, text="SALES MANAGEMENT", bg=BG, fg=ACCENT,
                 font=("Consolas", 22, "bold")).pack(pady=(30, 4))
        tk.Label(self, text="NEU · College of Technology", bg=BG, fg=SUBTEXT,
                 font=("Consolas", 11)).pack(pady=(0, 30))

        row = tk.Frame(self, bg=BG)
        row.pack(pady=10)

        stats = [
            ("Customers", "#SELECT COUNT(*) FROM Customers", ACCENT),
            ("Products",  "#SELECT COUNT(*) FROM Products",  ACCENT2),
            ("Orders",    "#SELECT COUNT(*) FROM Orders",    SUCCESS),
            ("Revenue",   "#SELECT SUM(Quantity*SalePrice) FROM OrderDetails", WARNING),
        ]
        for title, q, color in stats:
            self._stat_card(row, title, q, color)

        tk.Label(self, text="Click a section in the sidebar to get started.",
                 bg=BG, fg=SUBTEXT, font=("Consolas", 11)).pack(pady=30)

    def _stat_card(self, parent, title, q, color):
        c = tk.Frame(parent, bg=CARD, padx=24, pady=18,
                     highlightbackground=color, highlightthickness=1)
        c.pack(side="left", padx=10)

        # fetch real value
        try:
            real_q = q.lstrip("#")
            val = run(real_q, fetch=True)[0][0]
            val = f"{val:,.0f}" if val else "0"
        except:
            val = "—"

        tk.Label(c, text=val, bg=CARD, fg=color,
                 font=("Consolas", 24, "bold")).pack()
        tk.Label(c, text=title, bg=CARD, fg=SUBTEXT,
                 font=("Consolas", 10)).pack()


class CustomerPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=PANEL)
        self.build()

    def build(self):
        section_title(self, "👤  Customer Management").pack(fill="x", padx=20, pady=(20, 10))

        # Form
        form = tk.Frame(self, bg=CARD, padx=20, pady=16)
        form.pack(fill="x", padx=20, pady=(0, 12))

        fields = [("Name", 0), ("Address", 1), ("Phone", 2)]
        self.entries = {}
        for lbl, col in fields:
            tk.Label(form, text=lbl, bg=CARD, fg=SUBTEXT,
                     font=("Consolas", 10)).grid(row=0, column=col*2, sticky="w", padx=(0,4))
            e = styled_entry(form)
            e.grid(row=1, column=col*2, padx=(0, 16), pady=4)
            self.entries[lbl] = e

        # Search
        tk.Label(form, text="Search", bg=CARD, fg=SUBTEXT,
                 font=("Consolas", 10)).grid(row=0, column=6, sticky="w", padx=(0,4))
        self.search_e = styled_entry(form, width=16)
        self.search_e.grid(row=1, column=6, padx=(0, 8))

        btn_row = tk.Frame(form, bg=CARD)
        btn_row.grid(row=2, column=0, columnspan=8, pady=(10, 0), sticky="w")
        styled_btn(btn_row, "Add",    self.add,    SUCCESS).pack(side="left", padx=(0,8))
        styled_btn(btn_row, "Update", self.update, ACCENT).pack(side="left", padx=(0,8))
        styled_btn(btn_row, "Search", self.search, WARNING).pack(side="left", padx=(0,8))
        styled_btn(btn_row, "Refresh",self.load,   "#555").pack(side="left")

        # Table
        cols = ("ID", "Name", "Address", "Phone")
        tf, self.tree = make_table(self, cols)
        tf.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        self.tree.bind("<<TreeviewSelect>>", self.on_select)
        self.load()

    def load(self):
        clear_tree(self.tree)
        for r in run("SELECT * FROM Customers", fetch=True):
            self.tree.insert("", "end", values=r)

    def add(self):
        n, a, p = self.entries["Name"].get(), self.entries["Address"].get(), self.entries["Phone"].get()
        if not n or not p:
            messagebox.showwarning("Missing", "Name and Phone are required.")
            return
        run("INSERT INTO Customers (CustomerName,Address,PhoneNumber) VALUES (%s,%s,%s)", (n,a,p))
        self.load()
        messagebox.showinfo("Success", "Customer added!")

    def update(self):
        sel = self.tree.focus()
        if not sel:
            messagebox.showwarning("Select", "Select a customer first.")
            return
        cid = self.tree.item(sel)["values"][0]
        n, a, p = self.entries["Name"].get(), self.entries["Address"].get(), self.entries["Phone"].get()
        run("UPDATE Customers SET CustomerName=%s,Address=%s,PhoneNumber=%s WHERE CustomerID=%s", (n,a,p,cid))
        self.load()
        messagebox.showinfo("Success", "Customer updated!")

    def search(self):
        kw = self.search_e.get()
        clear_tree(self.tree)
        for r in run("SELECT * FROM Customers WHERE CustomerName LIKE %s OR PhoneNumber LIKE %s",
                     (f"%{kw}%", f"%{kw}%"), fetch=True):
            self.tree.insert("", "end", values=r)

    def on_select(self, _):
        sel = self.tree.focus()
        if not sel: return
        vals = self.tree.item(sel)["values"]
        for key, val in zip(["Name", "Address", "Phone"], vals[1:]):
            self.entries[key].delete(0, "end")
            self.entries[key].insert(0, val)


class ProductPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=PANEL)
        self.build()

    def build(self):
        section_title(self, "📦  Product Management").pack(fill="x", padx=20, pady=(20, 10))

        form = tk.Frame(self, bg=CARD, padx=20, pady=16)
        form.pack(fill="x", padx=20, pady=(0, 12))

        fields = [("Product Name", 0), ("Price", 1), ("Stock", 2)]
        self.entries = {}
        for lbl, col in fields:
            tk.Label(form, text=lbl, bg=CARD, fg=SUBTEXT,
                     font=("Consolas", 10)).grid(row=0, column=col*2, sticky="w", padx=(0,4))
            e = styled_entry(form, width=18)
            e.grid(row=1, column=col*2, padx=(0,16), pady=4)
            self.entries[lbl] = e

        btn_row = tk.Frame(form, bg=CARD)
        btn_row.grid(row=2, column=0, columnspan=8, pady=(10,0), sticky="w")
        styled_btn(btn_row, "Add",     self.add,    SUCCESS).pack(side="left", padx=(0,8))
        styled_btn(btn_row, "Update",  self.update, ACCENT).pack(side="left", padx=(0,8))
        styled_btn(btn_row, "Delete",  self.delete, DANGER).pack(side="left", padx=(0,8))
        styled_btn(btn_row, "Refresh", self.load,   "#555").pack(side="left")

        cols = ("ID", "Product Name", "Price", "Stock")
        tf, self.tree = make_table(self, cols)
        tf.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        self.tree.bind("<<TreeviewSelect>>", self.on_select)
        self.load()

    def load(self):
        clear_tree(self.tree)
        for r in run("SELECT * FROM Products", fetch=True):
            self.tree.insert("", "end", values=r)

    def add(self):
        n = self.entries["Product Name"].get()
        try:
            p, s = float(self.entries["Price"].get()), int(self.entries["Stock"].get())
        except:
            messagebox.showerror("Error", "Price and Stock must be numbers."); return
        run("INSERT INTO Products (ProductName,Price,StockQuantity) VALUES (%s,%s,%s)", (n,p,s))
        self.load()
        messagebox.showinfo("Success", "Product added!")

    def update(self):
        sel = self.tree.focus()
        if not sel:
            messagebox.showwarning("Select", "Select a product first."); return
        pid = self.tree.item(sel)["values"][0]
        n = self.entries["Product Name"].get()
        try:
            p, s = float(self.entries["Price"].get()), int(self.entries["Stock"].get())
        except:
            messagebox.showerror("Error", "Price and Stock must be numbers."); return
        run("UPDATE Products SET ProductName=%s,Price=%s,StockQuantity=%s WHERE ProductID=%s", (n,p,s,pid))
        self.load()
        messagebox.showinfo("Success", "Product updated!")

    def delete(self):
        sel = self.tree.focus()
        if not sel:
            messagebox.showwarning("Select", "Select a product first."); return
        pid = self.tree.item(sel)["values"][0]
        if messagebox.askyesno("Confirm", f"Delete product ID {pid}?"):
            run("DELETE FROM Products WHERE ProductID=%s", (pid,))
            self.load()

    def on_select(self, _):
        sel = self.tree.focus()
        if not sel: return
        vals = self.tree.item(sel)["values"]
        for key, val in zip(["Product Name", "Price", "Stock"], vals[1:]):
            self.entries[key].delete(0, "end")
            self.entries[key].insert(0, val)


class OrderPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=PANEL)
        self.build()

    def build(self):
        section_title(self, "🛒  Order Management").pack(fill="x", padx=20, pady=(20, 10))

        form = tk.Frame(self, bg=CARD, padx=20, pady=16)
        form.pack(fill="x", padx=20, pady=(0, 12))

        labels = ["Customer ID", "Employee ID", "Product ID", "Quantity", "Sale Price"]
        self.entries = {}
        for i, lbl in enumerate(labels):
            tk.Label(form, text=lbl, bg=CARD, fg=SUBTEXT,
                     font=("Consolas", 10)).grid(row=0, column=i*2, sticky="w", padx=(0,4))
            e = styled_entry(form, width=12)
            e.grid(row=1, column=i*2, padx=(0,12), pady=4)
            self.entries[lbl] = e

        tk.Label(form, text="Order ID (for update)", bg=CARD, fg=SUBTEXT,
                 font=("Consolas", 10)).grid(row=0, column=10, sticky="w")
        self.oid_e = styled_entry(form, width=10)
        self.oid_e.grid(row=1, column=10, padx=(0,8))

        tk.Label(form, text="New Status", bg=CARD, fg=SUBTEXT,
                 font=("Consolas", 10)).grid(row=0, column=11, sticky="w")
        self.status_var = tk.StringVar(value="Pending")
        cb = ttk.Combobox(form, textvariable=self.status_var,
                          values=["Pending", "Completed", "Cancelled"],
                          width=12, state="readonly",
                          font=("Consolas", 10))
        cb.grid(row=1, column=11, padx=(0,8))

        btn_row = tk.Frame(form, bg=CARD)
        btn_row.grid(row=2, column=0, columnspan=12, pady=(10,0), sticky="w")
        styled_btn(btn_row, "Create Order",  self.create, SUCCESS).pack(side="left", padx=(0,8))
        styled_btn(btn_row, "Update Status", self.update, ACCENT).pack(side="left", padx=(0,8))
        styled_btn(btn_row, "Refresh",       self.load,   "#555").pack(side="left")

        cols = ("OrderID", "Customer", "Employee", "Date", "Status")
        tf, self.tree = make_table(self, cols)
        tf.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        self.tree.bind("<<TreeviewSelect>>", self.on_select)
        self.load()

    def load(self):
        clear_tree(self.tree)
        rows = run("""SELECT o.OrderID, c.CustomerName, e.EmployeeName, o.OrderDate, o.Status
                      FROM Orders o
                      JOIN Customers c ON o.CustomerID=c.CustomerID
                      JOIN Employees e ON o.EmployeeID=e.EmployeeID
                      ORDER BY o.OrderID DESC""", fetch=True)
        for r in rows:
            self.tree.insert("", "end", values=r)

    def create(self):
        try:
            c = int(self.entries["Customer ID"].get())
            e = int(self.entries["Employee ID"].get())
            p = int(self.entries["Product ID"].get())
            q = int(self.entries["Quantity"].get())
            pr = float(self.entries["Sale Price"].get())
        except:
            messagebox.showerror("Error", "All fields must be valid numbers."); return
        try:
            proc("create_order", [c, e, p, q, pr])
            self.load()
            messagebox.showinfo("Success", "Order created!")
        except Exception as ex:
            messagebox.showerror("DB Error", str(ex))

    def update(self):
        try:
            oid = int(self.oid_e.get())
        except:
            messagebox.showerror("Error", "Enter a valid Order ID."); return
        run("UPDATE Orders SET Status=%s WHERE OrderID=%s", (self.status_var.get(), oid))
        self.load()
        messagebox.showinfo("Success", "Status updated!")

    def on_select(self, _):
        sel = self.tree.focus()
        if not sel: return
        vals = self.tree.item(sel)["values"]
        self.oid_e.delete(0, "end")
        self.oid_e.insert(0, vals[0])
        self.status_var.set(vals[4])


class EmployeePage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=PANEL)
        self.build()

    def build(self):
        section_title(self, "👔  Employee Management").pack(fill="x", padx=20, pady=(20, 10))

        form = tk.Frame(self, bg=CARD, padx=20, pady=16)
        form.pack(fill="x", padx=20, pady=(0, 12))

        for i, lbl in enumerate(["Name", "Job Title"]):
            tk.Label(form, text=lbl, bg=CARD, fg=SUBTEXT,
                     font=("Consolas", 10)).grid(row=0, column=i*2, sticky="w", padx=(0,4))
        self.name_e = styled_entry(form)
        self.name_e.grid(row=1, column=0, padx=(0,16))
        self.job_e = styled_entry(form)
        self.job_e.grid(row=1, column=2, padx=(0,16))

        btn_row = tk.Frame(form, bg=CARD)
        btn_row.grid(row=2, column=0, columnspan=6, pady=(10,0), sticky="w")
        styled_btn(btn_row, "Add",     self.add,    SUCCESS).pack(side="left", padx=(0,8))
        styled_btn(btn_row, "Update",  self.update, ACCENT).pack(side="left", padx=(0,8))
        styled_btn(btn_row, "Refresh", self.load,   "#555").pack(side="left")

        cols = ("ID", "Name", "Job Title")
        tf, self.tree = make_table(self, cols, height=14)
        tf.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        self.tree.bind("<<TreeviewSelect>>", self.on_select)
        self.load()

    def load(self):
        clear_tree(self.tree)
        for r in run("SELECT * FROM Employees", fetch=True):
            self.tree.insert("", "end", values=r)

    def add(self):
        n, j = self.name_e.get(), self.job_e.get()
        if not n:
            messagebox.showwarning("Missing", "Name is required."); return
        run("INSERT INTO Employees (EmployeeName,JobTitle) VALUES (%s,%s)", (n,j))
        self.load()
        messagebox.showinfo("Success", "Employee added!")

    def update(self):
        sel = self.tree.focus()
        if not sel:
            messagebox.showwarning("Select", "Select an employee first."); return
        eid = self.tree.item(sel)["values"][0]
        run("UPDATE Employees SET EmployeeName=%s,JobTitle=%s WHERE EmployeeID=%s",
            (self.name_e.get(), self.job_e.get(), eid))
        self.load()
        messagebox.showinfo("Success", "Employee updated!")

    def on_select(self, _):
        sel = self.tree.focus()
        if not sel: return
        vals = self.tree.item(sel)["values"]
        self.name_e.delete(0, "end"); self.name_e.insert(0, vals[1])
        self.job_e.delete(0, "end");  self.job_e.insert(0, vals[2])


class ReportPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=PANEL)
        self.build()

    def build(self):
        section_title(self, "📊  Reports & Analytics").pack(fill="x", padx=20, pady=(20, 10))

        btn_row = tk.Frame(self, bg=PANEL)
        btn_row.pack(fill="x", padx=20, pady=(0, 12))
        styled_btn(btn_row, "Sales Detail",   lambda: self.show("detail"),    ACCENT,  16).pack(side="left", padx=(0,8))
        styled_btn(btn_row, "By Employee",    lambda: self.show("employee"),  ACCENT2, 16).pack(side="left", padx=(0,8))
        styled_btn(btn_row, "Inventory",      lambda: self.show("inventory"), SUCCESS, 16).pack(side="left", padx=(0,8))
        styled_btn(btn_row, "Revenue",        self.show_revenue,              WARNING, 16).pack(side="left", padx=(0,8))

        self.table_frame = tk.Frame(self, bg=PANEL)
        self.table_frame.pack(fill="both", expand=True, padx=20)

        self.rev_label = tk.Label(self, text="", bg=PANEL, fg=WARNING,
                                  font=("Consolas", 18, "bold"))

        self.show("detail")

    def clear(self):
        for w in self.table_frame.winfo_children():
            w.destroy()
        self.rev_label.pack_forget()

    def show(self, mode):
        self.clear()
        if mode == "detail":
            cols = ("OrderID","Customer","Employee","Product","Qty","Price","Total")
            tf, tree = make_table(self.table_frame, cols, height=16)
            tf.pack(fill="both", expand=True)
            for r in run("SELECT * FROM SalesReport", fetch=True):
                tree.insert("", "end", values=r)

        elif mode == "employee":
            cols = ("Employee","Total Orders","Total Revenue")
            tf, tree = make_table(self.table_frame, cols, height=16)
            tf.pack(fill="both", expand=True)
            rows = run("""SELECT e.EmployeeName,
                                 COUNT(DISTINCT o.OrderID),
                                 SUM(od.Quantity*od.SalePrice)
                          FROM Employees e
                          JOIN Orders o ON e.EmployeeID=o.EmployeeID
                          JOIN OrderDetails od ON o.OrderID=od.OrderID
                          GROUP BY e.EmployeeID,e.EmployeeName
                          ORDER BY 3 DESC""", fetch=True)
            for r in rows:
                tree.insert("", "end", values=r)

        elif mode == "inventory":
            cols = ("ID","Product","Price","Stock","Status")
            tf, tree = make_table(self.table_frame, cols, height=16)
            tf.pack(fill="both", expand=True)
            for r in run("SELECT * FROM Products ORDER BY StockQuantity ASC", fetch=True):
                status = "⚠ LOW" if r[3] < 5 else "OK"
                tree.insert("", "end", values=(*r, status))

    def show_revenue(self):
        self.clear()
        # Uses UDF calculate_total(qty, price) defined in advanced.sql
        val = run("SELECT SUM(calculate_total(Quantity, SalePrice)) FROM OrderDetails", fetch=True)[0][0]
        val = f"{val:,.2f}" if val else "0.00"

        wrapper = tk.Frame(self.table_frame, bg=PANEL)
        wrapper.pack(fill="both", expand=True, pady=20)

        tk.Label(wrapper, text="💰  Total Revenue", bg=PANEL, fg=SUBTEXT,
                 font=("Consolas", 13)).pack(pady=(30, 4))
        tk.Label(wrapper, text=val, bg=PANEL, fg=WARNING,
                 font=("Consolas", 36, "bold")).pack(pady=(0, 30))

        tk.Frame(wrapper, bg=BORDER, height=1).pack(fill="x", padx=60, pady=(0, 20))

        tk.Label(wrapper, text="⚙  Calculated using UDF:  calculate_total(Quantity, SalePrice)",
                 bg=PANEL, fg=SUBTEXT, font=("Consolas", 10)).pack()
        tk.Label(wrapper, text="SELECT SUM(calculate_total(Quantity, SalePrice)) FROM OrderDetails",
                 bg=CARD, fg=ACCENT, font=("Consolas", 10),
                 padx=16, pady=8).pack(pady=(6, 0))


# ─── ADVANCED DB PAGE ─────────────────────────────────────────────────────────

class AdvancedPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=PANEL)
        self.build()

    def build(self):
        section_title(self, "⚙  Advanced DB — Live Demo").pack(fill="x", padx=20, pady=(20, 6))
        tk.Label(self, text="Each feature below is LIVE — interact with your real database.",
                 bg=PANEL, fg=SUBTEXT, font=("Consolas", 10)).pack(anchor="w", padx=22, pady=(0,10))

        canvas = tk.Canvas(self, bg=PANEL, highlightthickness=0)
        sb = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        canvas.pack(fill="both", expand=True)
        inner = tk.Frame(canvas, bg=PANEL)
        canvas.create_window((0,0), window=inner, anchor="nw")
        inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        self._build_index(inner)
        self._build_view(inner)
        self._build_procedure(inner)
        self._build_udf(inner)
        self._build_trigger(inner)

    # ── helper to make a section card ──
    def _card(self, parent, title, color):
        outer = tk.Frame(parent, bg=CARD, padx=18, pady=14,
                         highlightbackground=color, highlightthickness=2)
        outer.pack(fill="x", padx=20, pady=(0,14))
        tk.Label(outer, text=title, bg=CARD, fg=color,
                 font=("Consolas", 12, "bold")).pack(anchor="w")
        tk.Frame(outer, bg=BORDER, height=1).pack(fill="x", pady=(6,10))
        return outer

    # ── 1. INDEX ──
    def _build_index(self, parent):
        card = self._card(parent, "🔍  INDEX — Search Products by Name (uses idx_product_name)", ACCENT)
        tk.Label(card, text="Type a product name below. MySQL uses the index to find it instantly.",
                 bg=CARD, fg=SUBTEXT, font=("Consolas", 10)).pack(anchor="w", pady=(0,8))

        row = tk.Frame(card, bg=CARD)
        row.pack(fill="x")
        self.idx_entry = styled_entry(row, width=20)
        self.idx_entry.pack(side="left", padx=(0,10))
        styled_btn(row, "Search", self._run_index, ACCENT, 10).pack(side="left")

        tf, self.idx_tree = make_table(card, ("ID","Product Name","Price","Stock"), height=4)
        tf.pack(fill="x", pady=(10,0))

    def _run_index(self):
        kw = self.idx_entry.get().strip()
        clear_tree(self.idx_tree)
        rows = run("SELECT * FROM Products WHERE ProductName LIKE %s", (f"%{kw}%",), fetch=True)
        for r in rows:
            self.idx_tree.insert("", "end", values=r)
        if not rows:
            messagebox.showinfo("Index Search", "No products found.")

    # ── 2. VIEW ──
    def _build_view(self, parent):
        card = self._card(parent, "👁  VIEW — Query SalesReport View", ACCENT2)
        tk.Label(card, text="Clicking 'Load View' runs:  SELECT * FROM SalesReport\n"
                            "The view joins 5 tables automatically — no complex SQL needed here.",
                 bg=CARD, fg=SUBTEXT, font=("Consolas", 10)).pack(anchor="w", pady=(0,8))

        styled_btn(card, "Load SalesReport View", self._run_view, ACCENT2, 22).pack(anchor="w")
        tf, self.view_tree = make_table(card,
            ("OrderID","Customer","Employee","Product","Qty","Price","Total"), height=5)
        tf.pack(fill="x", pady=(10,0))

    def _run_view(self):
        clear_tree(self.view_tree)
        for r in run("SELECT * FROM SalesReport", fetch=True):
            self.view_tree.insert("", "end", values=r)

    # ── 3. STORED PROCEDURE ──
    def _build_procedure(self, parent):
        card = self._card(parent, "⚙  STORED PROCEDURE — Call create_order", SUCCESS)
        tk.Label(card, text="Fill in the fields and click 'Call Procedure'.\n"
                            "Python calls:  cursor.callproc('create_order', [...])\n"
                            "MySQL inserts into Orders AND OrderDetails in one go.",
                 bg=CARD, fg=SUBTEXT, font=("Consolas", 10)).pack(anchor="w", pady=(0,8))

        row = tk.Frame(card, bg=CARD)
        row.pack(fill="x")
        labels = ["Customer ID", "Employee ID", "Product ID", "Quantity", "Price"]
        self.proc_entries = {}
        for lbl in labels:
            tk.Label(row, text=lbl, bg=CARD, fg=SUBTEXT,
                     font=("Consolas", 9)).pack(side="left", padx=(0,2))
            e = styled_entry(row, width=8)
            e.pack(side="left", padx=(0,10))
            self.proc_entries[lbl] = e

        self.proc_result = tk.Label(card, text="", bg=CARD, fg=SUCCESS,
                                    font=("Consolas", 10, "bold"))
        self.proc_result.pack(anchor="w", pady=(6,0))

        styled_btn(card, "Call Procedure", self._run_procedure, SUCCESS, 18).pack(anchor="w", pady=(6,0))

    def _run_procedure(self):
        try:
            c = int(self.proc_entries["Customer ID"].get())
            e = int(self.proc_entries["Employee ID"].get())
            p = int(self.proc_entries["Product ID"].get())
            q = int(self.proc_entries["Quantity"].get())
            pr = float(self.proc_entries["Price"].get())
        except:
            messagebox.showerror("Error", "All fields must be valid numbers."); return
        try:
            proc("create_order", [c, e, p, q, pr])
            self.proc_result.config(
                text=f"✔  Procedure executed! Order created for Customer {c}, Product {p} x{q}",
                fg=SUCCESS)
        except Exception as ex:
            self.proc_result.config(text=f"✘  {ex}", fg=DANGER)

    # ── 4. UDF ──
    def _build_udf(self, parent):
        card = self._card(parent, "🔢  USER DEFINED FUNCTION — calculate_total(qty, price)", WARNING)
        tk.Label(card, text="Enter any quantity and price. Calls your UDF directly:\n"
                            "SELECT calculate_total(qty, price)",
                 bg=CARD, fg=SUBTEXT, font=("Consolas", 10)).pack(anchor="w", pady=(0,8))

        row = tk.Frame(card, bg=CARD)
        row.pack(fill="x")
        tk.Label(row, text="Quantity:", bg=CARD, fg=SUBTEXT,
                 font=("Consolas", 10)).pack(side="left", padx=(0,4))
        self.udf_qty = styled_entry(row, width=8)
        self.udf_qty.pack(side="left", padx=(0,14))
        tk.Label(row, text="Price:", bg=CARD, fg=SUBTEXT,
                 font=("Consolas", 10)).pack(side="left", padx=(0,4))
        self.udf_price = styled_entry(row, width=10)
        self.udf_price.pack(side="left", padx=(0,14))
        styled_btn(row, "Calculate", self._run_udf, WARNING, 12).pack(side="left")

        self.udf_result = tk.Label(card, text="Result: —", bg=CARD, fg=WARNING,
                                   font=("Consolas", 16, "bold"))
        self.udf_result.pack(anchor="w", pady=(10,0))

    def _run_udf(self):
        try:
            q = int(self.udf_qty.get())
            p = float(self.udf_price.get())
        except:
            messagebox.showerror("Error", "Enter valid numbers."); return
        result = run("SELECT calculate_total(%s, %s)", (q, p), fetch=True)[0][0]
        self.udf_result.config(text=f"calculate_total({q}, {p})  =  {float(result):,.2f}")

    # ── 5. TRIGGER ──
    def _build_trigger(self, parent):
        card = self._card(parent, "⚡  TRIGGERS — Test trg_check_stock & trg_update_stock", DANGER)
        tk.Label(card, text="Test 1 — Valid order: stock reduces automatically after insert (trg_update_stock)\n"
                            "Test 2 — Over-stock order: trigger blocks it and shows error (trg_check_stock)",
                 bg=CARD, fg=SUBTEXT, font=("Consolas", 10)).pack(anchor="w", pady=(0,8))

        # Stock viewer
        styled_btn(card, "Refresh Stock", self._load_stock, "#555", 16).pack(anchor="w", pady=(0,6))
        tf, self.trg_tree = make_table(card, ("ID","Product","Stock"), height=4)
        tf.pack(fill="x", pady=(0,10))

        # Test controls
        row = tk.Frame(card, bg=CARD)
        row.pack(fill="x", pady=(0,6))
        tk.Label(row, text="Product ID:", bg=CARD, fg=SUBTEXT,
                 font=("Consolas", 10)).pack(side="left", padx=(0,4))
        self.trg_pid = styled_entry(row, width=6)
        self.trg_pid.pack(side="left", padx=(0,12))
        tk.Label(row, text="Quantity:", bg=CARD, fg=SUBTEXT,
                 font=("Consolas", 10)).pack(side="left", padx=(0,4))
        self.trg_qty = styled_entry(row, width=6)
        self.trg_qty.pack(side="left", padx=(0,12))

        btn_row = tk.Frame(card, bg=CARD)
        btn_row.pack(fill="x")
        styled_btn(btn_row, "✔ Valid Order (reduces stock)", self._trigger_valid, SUCCESS, 28).pack(side="left", padx=(0,10))
        styled_btn(btn_row, "✘ Over-Qty Order (blocked)", self._trigger_block, DANGER, 26).pack(side="left")

        self.trg_result = tk.Label(card, text="", bg=CARD,
                                   font=("Consolas", 10, "bold"))
        self.trg_result.pack(anchor="w", pady=(8,0))

        self._load_stock()

    def _load_stock(self):
        clear_tree(self.trg_tree)
        for r in run("SELECT ProductID, ProductName, StockQuantity FROM Products", fetch=True):
            self.trg_tree.insert("", "end", values=r)

    def _trigger_valid(self):
        try:
            pid = int(self.trg_pid.get())
            qty = int(self.trg_qty.get())
        except:
            messagebox.showerror("Error", "Enter valid Product ID and Quantity."); return
        try:
            # use first customer & employee available
            proc("create_order", [1, 1, pid, qty, 100.00])
            self.trg_result.config(
                text=f"✔  Order placed! Stock for Product {pid} reduced by {qty}. (trg_update_stock fired)",
                fg=SUCCESS)
            self._load_stock()
        except Exception as ex:
            self.trg_result.config(text=f"✘  {ex}", fg=DANGER)

    def _trigger_block(self):
        try:
            pid = int(self.trg_pid.get())
        except:
            messagebox.showerror("Error", "Enter valid Product ID."); return
        try:
            # attempt to order 99999 — always exceeds stock
            proc("create_order", [1, 1, pid, 99999, 100.00])
            self.trg_result.config(text="Order went through (stock was enough).", fg=WARNING)
        except Exception as ex:
            self.trg_result.config(
                text=f"✘  BLOCKED by trigger: {ex}  (trg_check_stock fired)",
                fg=DANGER)
        self._load_stock()


# ─── MAIN APP ─────────────────────────────────────────────────────────────────

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sales Management System")
        self.geometry("1200x720")
        self.minsize(900, 600)
        self.configure(bg=BG)
        self.resizable(True, True)
        self._build()

    def _build(self):
        # Sidebar
        sidebar = tk.Frame(self, bg=PANEL, width=NAV_W)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        tk.Label(sidebar, text="⬡", bg=PANEL, fg=ACCENT,
                 font=("Consolas", 28)).pack(pady=(24, 0))
        tk.Label(sidebar, text="SALES\nSYSTEM", bg=PANEL, fg=TEXT,
                 font=("Consolas", 11, "bold"), justify="center").pack(pady=(4, 28))

        tk.Frame(sidebar, bg=BORDER, height=1).pack(fill="x", padx=16, pady=(0, 16))

        self.pages = {}
        nav_items = [
            ("🏠  Dashboard",  "dashboard",  DashboardPage),
            ("👤  Customers",  "customers",  CustomerPage),
            ("📦  Products",   "products",   ProductPage),
            ("🛒  Orders",     "orders",     OrderPage),
            ("👔  Employees",  "employees",  EmployeePage),
            ("📊  Reports",    "reports",    ReportPage),
            ("⚙  Advanced DB", "advanced",  AdvancedPage),
        ]

        self.nav_btns = {}
        self.content = tk.Frame(self, bg=BG)
        self.content.pack(side="left", fill="both", expand=True)

        for label_text, key, PageClass in nav_items:
            page = PageClass(self.content)
            page.place(relwidth=1, relheight=1)
            self.pages[key] = page

            btn = tk.Button(sidebar, text=label_text,
                            command=lambda k=key: self.show(k),
                            bg=PANEL, fg=SUBTEXT, relief="flat",
                            font=("Consolas", 10), anchor="w",
                            padx=18, pady=10, cursor="hand2",
                            activebackground=CARD, activeforeground=TEXT,
                            bd=0)
            btn.pack(fill="x")
            self.nav_btns[key] = btn

        tk.Frame(sidebar, bg=BORDER, height=1).pack(fill="x", padx=16, pady=16)
        tk.Label(sidebar, text="v1.0  •  NEU", bg=PANEL, fg=BORDER,
                 font=("Consolas", 9)).pack(side="bottom", pady=12)

        self.show("dashboard")

    def show(self, key):
        for k, btn in self.nav_btns.items():
            if k == key:
                btn.config(bg=CARD, fg=ACCENT)
            else:
                btn.config(bg=PANEL, fg=SUBTEXT)
        self.pages[key].lift()


if __name__ == "__main__":
    App().mainloop()