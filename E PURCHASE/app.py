import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os, math, warnings, urllib.request, io
warnings.filterwarnings("ignore", category=UserWarning)

# ══════════════════════════════════════════════════════════
#  LIGHT GLASSMORPHISM THEME
# ══════════════════════════════════════════════════════════
BG      = "#EEF2F7"
PANEL   = "#FFFFFF"
GLASS_B = "#F0F4FA"
BORDER  = "#D8E2EE"
ACCENT  = "#4A90D9"
ACCENT2 = "#7B5EA7"
GOLD    = "#E8A838"
RED     = "#E05C6C"
GREEN   = "#3CB371"
DARK    = "#1E2A3A"
MID     = "#5A6A7E"
LIGHT   = "#A8B8CC"
WHITE   = "#FFFFFF"
ORANGE  = "#F07030"

FT   = ("Segoe UI", 12, "bold")
FT_S = ("Segoe UI", 10)
FT_L = ("Segoe UI", 16, "bold")
FT_XL= ("Segoe UI", 22, "bold")
FT_T = ("Segoe UI", 9)

AUTH = "users.xlsx"

# ══════════════════════════════════════════════════════════
#  LOAD DATA
# ══════════════════════════════════════════════════════════
def load_data():
    global df, monthly_sales, has_dates
    has_dates = False; monthly_sales = None
    try:
        df = pd.read_csv("dataexcel.csv")
        df.columns = df.columns.str.strip().str.replace(" ", "_")
        if "Profit" not in df.columns: df["Profit"] = df["Sales"] * 0.40
        if "Cost"   not in df.columns: df["Cost"]   = df["Sales"] - df["Profit"]
        ct = df.groupby("Customer_ID")["Sales"].transform("sum")
        df["Spend_Tier"] = pd.cut(ct,
            bins=[-1, ct.quantile(.33), ct.quantile(.66), float("inf")],
            labels=["Normal","Premium","VIP"])
        df["Suspicious"] = df["Sales"] > df["Sales"].mean() * 3
        if "Purchase_Date" in df.columns:
            df["_date"] = pd.to_datetime(df["Purchase_Date"], dayfirst=True, errors="coerce")
            df["_ym"]   = df["_date"].dt.to_period("M")
            ms = df.groupby("_ym")["Sales"].sum().sort_index()
            if len(ms) >= 3:
                monthly_sales = ms; has_dates = True
    except Exception:
        df = pd.DataFrame()

df = pd.DataFrame(); monthly_sales = None; has_dates = False
load_data()

def init_auth():
    if not os.path.exists(AUTH):
        pd.DataFrame([{"username":"admin","password":"admin123"}]).to_excel(AUTH,index=False)
init_auth()

# ══════════════════════════════════════════════════════════
#  ROOT WINDOW
# ══════════════════════════════════════════════════════════
root = tk.Tk()
root.title("E-Commerce Analytics  ·  Nithya.P")
root.state("zoomed"); root.configure(bg=BG)

sidebar  = tk.Frame(root, bg=PANEL, width=230)
sidebar.pack(side="left", fill="y"); sidebar.pack_propagate(False)
main_area= tk.Frame(root, bg=BG)
main_area.pack(side="right", fill="both", expand=True)
content  = tk.Frame(main_area, bg=BG)
content.pack(fill="both", expand=True)

# ══════════════════════════════════════════════════════════
#  HELPERS
# ══════════════════════════════════════════════════════════
def clear_frame():
    for w in content.winfo_children(): w.destroy()

def apply_treeview_style():
    s = ttk.Style(); s.theme_use("clam")
    s.configure("Treeview", background=WHITE, foreground=DARK,
                fieldbackground=WHITE, rowheight=26,
                font=("Segoe UI",10), borderwidth=0)
    s.configure("Treeview.Heading", background=GLASS_B, foreground=ACCENT,
                font=("Segoe UI",10,"bold"), relief="flat")
    s.map("Treeview", background=[("selected",ACCENT)], foreground=[("selected",WHITE)])

def page_title(text, color=ACCENT, back_cmd=None):
    hf = tk.Frame(content, bg=WHITE); hf.pack(fill="x")
    tk.Frame(hf, bg=color, width=4).pack(side="left", fill="y")
    if back_cmd:
        tk.Button(hf, text="← Back", font=("Segoe UI",10,"bold"),
                  bg=WHITE, fg=color, activebackground=GLASS_B,
                  bd=0, cursor="hand2", padx=14, pady=14,
                  command=back_cmd).pack(side="left")
    tk.Label(hf, text=text, font=FT_L, bg=WHITE, fg=DARK,
             padx=18, pady=14).pack(side="left")
    tk.Frame(content, bg=BORDER, height=1).pack(fill="x")

def big_btn(parent, text, cmd, color=ACCENT, w=22):
    b = tk.Button(parent, text=text, font=FT, bg=color, fg=WHITE,
                  activebackground=DARK, bd=0, cursor="hand2",
                  width=w, pady=9, relief="flat", command=cmd)
    b.bind("<Enter>", lambda e: b.config(bg=DARK))
    b.bind("<Leave>", lambda e: b.config(bg=color))
    return b

def embed(fig):
    c = FigureCanvasTkAgg(fig, master=content)
    w = c.get_tk_widget(); w.configure(bg=WHITE, highlightthickness=0)
    w.pack(fill="both", expand=True, padx=20, pady=10)
    c.draw(); plt.close(fig)

def embed_in(fig, parent):
    for w in parent.winfo_children(): w.destroy()
    c = FigureCanvasTkAgg(fig, master=parent)
    w = c.get_tk_widget(); w.configure(bg=WHITE, highlightthickness=0)
    w.pack(fill="both", expand=True, padx=4, pady=4)
    c.draw(); plt.close(fig)

def styled_fig(w=10, h=4.5):
    fig, ax = plt.subplots(figsize=(w,h), facecolor=WHITE)
    ax.set_facecolor("#F7FAFF")
    ax.tick_params(colors=MID, labelsize=9)
    ax.xaxis.label.set_color(MID); ax.yaxis.label.set_color(MID)
    for sp in ax.spines.values(): sp.set_edgecolor(BORDER); sp.set_linewidth(0.8)
    ax.grid(color=BORDER, linewidth=0.6, linestyle="--", alpha=0.8)
    ax.set_axisbelow(True)
    return fig, ax

def kpi_box(parent, icon, label, value, color):
    box   = tk.Frame(parent, bg=WHITE, highlightbackground=color, highlightthickness=2)
    inner = tk.Frame(box, bg=WHITE, padx=22, pady=16); inner.pack()
    tk.Frame(box, bg=color, height=3).place(relx=0, rely=0, relwidth=1)
    tk.Label(inner, text=icon,  font=("Segoe UI",20), bg=WHITE, fg=color).pack(pady=(4,0))
    tk.Label(inner, text=value, font=FT_XL,            bg=WHITE, fg=DARK).pack(pady=(3,1))
    tk.Label(inner, text=label, font=FT_T,              bg=WHITE, fg=MID).pack()
    return box

def sb_btn(icon_text, cmd):
    b = tk.Button(sidebar, text=icon_text, font=("Segoe UI",11),
                  bg=PANEL, fg=DARK, activebackground=GLASS_B,
                  activeforeground=ACCENT, bd=0, cursor="hand2",
                  anchor="w", padx=20, pady=11, command=cmd)
    b.pack(fill="x")
    b.bind("<Enter>", lambda e: b.config(bg=GLASS_B, fg=ACCENT))
    b.bind("<Leave>", lambda e: b.config(bg=PANEL, fg=DARK))
    tk.Frame(sidebar, bg=BORDER, height=1).pack(fill="x")
    return b

def watermark():
    tk.Label(content,
             text="NITHYA.P  ·  BCA FINAL  ·  E-COMMERCE ANALYTICS",
             font=("Segoe UI",8), bg=BG, fg=LIGHT).pack(side="bottom", pady=4)

def ctrl_strip(color=ACCENT):
    ctrl = tk.Frame(content, bg=WHITE)
    ctrl.pack(fill="x", padx=20, pady=(10,0))
    tk.Frame(ctrl, bg=color,  height=3).pack(fill="x", side="top")
    tk.Frame(ctrl, bg=BORDER, height=1).pack(fill="x", side="bottom")
    inn = tk.Frame(ctrl, bg=WHITE, padx=14, pady=10); inn.pack(fill="x")
    return inn

# ══════════════════════════════════════════════════════════
#  1. LOGIN
# ══════════════════════════════════════════════════════════
_login_photo = None

def show_login():
    global _login_photo
    sidebar.pack_forget(); clear_frame()

    cv = tk.Canvas(content, highlightthickness=0, bg="#1C2B4A")
    cv.place(relx=0, rely=0, relwidth=1, relheight=1)

    def _load_photo():
        global _login_photo
        try:
            url = "https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?w=1600&q=80"
            with urllib.request.urlopen(url, timeout=6) as resp:
                data = resp.read()
            from PIL import Image, ImageTk, ImageFilter, ImageEnhance
            img = Image.open(io.BytesIO(data))
            img = img.filter(ImageFilter.GaussianBlur(radius=2))
            img = ImageEnhance.Brightness(img).enhance(0.55)
            w = content.winfo_width() or 1200; h = content.winfo_height() or 750
            img = img.resize((w,h), Image.LANCZOS)
            _login_photo = ImageTk.PhotoImage(img)
            cv.create_image(0,0, anchor="nw", image=_login_photo, tags="bg")
            cv.tag_lower("bg")
        except Exception:
            _draw_fallback_bg()

    def _draw_fallback_bg(event=None):
        w = content.winfo_width() or 1200; h = content.winfo_height() or 750
        cv.delete("bg")
        for i in range(60):
            t = i/60
            r_ = int(28+t*20); g_ = int(43+t*30); b_ = int(74+t*60)
            y0 = int(h*i/60); y1 = int(h*(i+1)/60)+1
            cv.create_rectangle(0,y0,w,y1, fill=f"#{r_:02x}{g_:02x}{b_:02x}",
                                 outline="", tags="bg")
        sky = "#0D1B2A"
        blds = [(0,h,80,h-180),(80,h,160,h-240),(160,h,220,h-160),(220,h,300,h-310),
                (300,h,360,h-200),(360,h,420,h-270),(420,h,480,h-190),(480,h,560,h-350),
                (560,h,620,h-220),(620,h,700,h-290),(700,h,760,h-170),(760,h,840,h-320),
                (840,h,900,h-200),(900,h,960,h-260),(960,h,1040,h-180),(1040,h,1120,h-240),
                (1120,h,1200,h-160),(1200,h,1300,h-200),(1300,h,1400,h-170),(1400,h,1600,h-140)]
        for x1,y1,x2,y2 in blds:
            cv.create_rectangle(x1,y1,x2,y2, fill=sky, outline="", tags="bg")
        import random; random.seed(42)
        for x1,y1,x2,y2 in blds:
            for wx in range(x1+6, x2-6, 12):
                for wy in range(y2+8, y1-8, 16):
                    if random.random() > 0.45:
                        wc = random.choice(["#FFE08A","#FFD060","#FFF0B0","#A0C8FF"])
                        cv.create_rectangle(wx,wy,wx+6,wy+8, fill=wc, outline="", tags="bg")
        for i in range(8):
            yy = h-60+i*8
            cv.create_line(0,yy,w,yy, fill=f"#{10+i*4:02x}{20+i*6:02x}{40+i*8:02x}",
                           width=2, tags="bg")
        cv.tag_lower("bg")

    content.update_idletasks()
    try:
        from PIL import Image; root.after(100, _load_photo); _draw_fallback_bg()
    except ImportError:
        _draw_fallback_bg()
    content.bind("<Configure>", lambda e: _draw_fallback_bg() if _login_photo is None else None)

    CARD_W = 440
    outer = tk.Frame(content, bg=WHITE, highlightbackground=WHITE, highlightthickness=1)
    outer.place(relx=0.5, rely=0.5, anchor="center", width=CARD_W)
    top_band = tk.Frame(outer, height=6); top_band.pack(fill="x")
    tk.Frame(top_band, bg=ACCENT,  width=CARD_W//2, height=6).place(x=0, y=0)
    tk.Frame(top_band, bg=ACCENT2, width=CARD_W//2, height=6).place(x=CARD_W//2, y=0)
    inn = tk.Frame(outer, bg=WHITE, padx=44, pady=36); inn.pack(fill="x")

    logo_f = tk.Frame(inn, bg=WHITE); logo_f.pack(pady=(0,6))
    tk.Label(logo_f, text="⬡", font=("Segoe UI",28), bg=WHITE, fg=ACCENT).pack(side="left", padx=(0,10))
    name_f = tk.Frame(logo_f, bg=WHITE); name_f.pack(side="left")
    tk.Label(name_f, text="NITHYA.P",           font=("Segoe UI",20,"bold"), bg=WHITE, fg=DARK).pack(anchor="w")
    tk.Label(name_f, text="E-Commerce Analytics",font=("Segoe UI",9),        bg=WHITE, fg=MID).pack(anchor="w")

    div = tk.Frame(inn, bg=WHITE); div.pack(fill="x", pady=(10,18))
    tk.Frame(div, bg=ACCENT,  height=2, width=80).pack(side="left")
    tk.Frame(div, bg=ACCENT2, height=2, width=50).pack(side="left", padx=3)
    tk.Frame(div, bg=GOLD,    height=2, width=30).pack(side="left")

    def field(parent, label, show=""):
        tk.Label(parent, text=label, font=("Segoe UI",9,"bold"),
                 bg=WHITE, fg=MID, anchor="w").pack(fill="x", pady=(4,2))
        wrapper = tk.Frame(parent, bg=BORDER, padx=1, pady=1); wrapper.pack(fill="x")
        inner_f = tk.Frame(wrapper, bg=WHITE); inner_f.pack(fill="x")
        e = tk.Entry(inner_f, font=("Segoe UI",11), bg=WHITE, fg=DARK,
                     insertbackground=ACCENT, show=show, bd=0, highlightthickness=0)
        e.pack(fill="x", ipady=10, padx=12)
        e.bind("<FocusIn>",  lambda _: wrapper.config(bg=ACCENT))
        e.bind("<FocusOut>", lambda _: wrapper.config(bg=BORDER))
        return e, wrapper

    u_entry, _ = field(inn, "USERNAME")
    tk.Label(inn, text="PASSWORD", font=("Segoe UI",9,"bold"),
             bg=WHITE, fg=MID, anchor="w").pack(fill="x", pady=(12,2))
    pw_wrap  = tk.Frame(inn, bg=BORDER, padx=1, pady=1); pw_wrap.pack(fill="x")
    pw_inner = tk.Frame(pw_wrap, bg=WHITE); pw_inner.pack(fill="x")
    p_entry  = tk.Entry(pw_inner, font=("Segoe UI",11), bg=WHITE, fg=DARK,
                        insertbackground=ACCENT2, show="*", bd=0, highlightthickness=0)
    p_entry.pack(side="left", fill="x", expand=True, ipady=10, padx=(12,0))

    def _toggle():
        p_entry.config(show="" if p_entry.cget("show")=="*" else "*")
        eye.config(text="●" if p_entry.cget("show")=="" else "○",
                   fg=ACCENT if p_entry.cget("show")==""  else MID)
    eye = tk.Button(pw_inner, text="○", font=("Segoe UI",12),
                    bg=WHITE, fg=MID, bd=0, cursor="hand2", command=_toggle)
    eye.pack(side="right", padx=10)
    p_entry.bind("<FocusIn>",  lambda _: pw_wrap.config(bg=ACCENT2))
    p_entry.bind("<FocusOut>", lambda _: pw_wrap.config(bg=BORDER))
    tk.Frame(inn, bg=BORDER, height=1).pack(fill="x", pady=(20,16))

    def _hov_in(e):  sign_btn.config(bg=DARK)
    def _hov_out(e): sign_btn.config(bg=ACCENT)
    sign_btn = tk.Button(inn, text="SIGN IN", font=("Segoe UI",12,"bold"),
                         bg=ACCENT, fg=WHITE, activebackground=DARK,
                         bd=0, cursor="hand2", pady=12, relief="flat",
                         command=lambda: _do_login())
    sign_btn.pack(fill="x", pady=(0,8))
    sign_btn.bind("<Enter>", _hov_in); sign_btn.bind("<Leave>", _hov_out)
    tk.Button(inn, text="Create account  →", font=("Segoe UI",10),
              bg=WHITE, fg=ACCENT2, bd=0, cursor="hand2",
              command=show_register).pack(fill="x")
    status_lbl = tk.Label(inn, text="", font=("Segoe UI",9), bg=WHITE, fg=RED)
    status_lbl.pack(pady=(8,0))

    def _do_login():
        u = u_entry.get().strip(); p = p_entry.get().strip()
        if not u or not p:
            status_lbl.config(text="⚠  Please enter username and password."); return
        try:
            udf = pd.read_excel(AUTH)
            if not udf[(udf.username==u)&(udf.password.astype(str)==str(p))].empty:
                sidebar.pack(side="left", fill="y"); show_dashboard()
            else:
                status_lbl.config(text="✗  Wrong username or password.")
        except Exception as ex:
            status_lbl.config(text=f"Error: {ex}")

    root.bind("<Return>", lambda e: _do_login())
    tk.Label(content, text="◆  NITHYA.P  ·  BCA FINAL  ·  E-COMMERCE ANALYTICS  ·  2024",
             font=("Segoe UI",8), bg="#1C2B4A", fg="#4A6080"
             ).place(relx=0.5, rely=0.97, anchor="center")


# ══════════════════════════════════════════════════════════
#  2. REGISTER
# ══════════════════════════════════════════════════════════
def show_register():
    clear_frame()
    card = tk.Frame(content, bg=WHITE, highlightbackground=ACCENT, highlightthickness=1)
    card.place(relx=0.5, rely=0.5, anchor="center", width=430)
    tk.Frame(card, bg=ACCENT, height=4).pack(fill="x")
    inn = tk.Frame(card, bg=WHITE, padx=44, pady=36); inn.pack(fill="x")
    tk.Label(inn, text="Create Account", font=("Segoe UI",20,"bold"),
             bg=WHITE, fg=DARK).pack(pady=(0,20))
    entries = {}
    for lbl, show in [("USERNAME",""),("PASSWORD","*")]:
        tk.Label(inn, text=lbl, font=("Segoe UI",9,"bold"),
                 bg=WHITE, fg=MID, anchor="w").pack(fill="x", pady=(6,2))
        bf = tk.Frame(inn, bg=BORDER, padx=1, pady=1); bf.pack(fill="x")
        bi = tk.Frame(bf, bg=WHITE); bi.pack(fill="x")
        e  = tk.Entry(bi, font=("Segoe UI",11), bg=WHITE, fg=DARK,
                      insertbackground=ACCENT, show=show, bd=0)
        e.pack(fill="x", ipady=10, padx=12); entries[lbl] = e

    def save():
        u = entries["USERNAME"].get().strip(); p = entries["PASSWORD"].get().strip()
        if u and p:
            udf = pd.read_excel(AUTH)
            if u in udf.username.values:
                messagebox.showwarning("Taken","Username already exists.")
            else:
                pd.concat([udf, pd.DataFrame([{"username":u,"password":p}])],
                          ignore_index=True).to_excel(AUTH, index=False)
                messagebox.showinfo("Done","Account created! Sign in now.")
                show_login()
        else:
            messagebox.showwarning("Empty","Fill both fields.")

    tk.Frame(inn, bg=BORDER, height=1).pack(fill="x", pady=(16,14))
    big_btn(inn, "REGISTER", save, ACCENT, 28).pack(fill="x", pady=(0,8))
    tk.Button(inn, text="← Back to sign in", font=("Segoe UI",10),
              bg=WHITE, fg=MID, bd=0, cursor="hand2", command=show_login).pack()


# ══════════════════════════════════════════════════════════
#  3. DASHBOARD
# ══════════════════════════════════════════════════════════
def show_dashboard():
    clear_frame()
    page_title("Dashboard", ACCENT)
    if df.empty:
        tk.Label(content, text="⚠  dataexcel.csv not found!",
                 font=FT_L, bg=BG, fg=RED).pack(pady=40)
        return
    krow = tk.Frame(content, bg=BG); krow.pack(pady=22, padx=30)
    for icon,lbl,val,col in [
        ("₹","Total Sales",  f"₹{df.Sales.sum():,.0f}",     ACCENT),
        ("＋","Total Profit", f"₹{df.Profit.sum():,.0f}",    GREEN),
        ("◎","Orders",       f"{len(df):,}",                  ACCENT2),
        ("◈","Customers",    f"{df.Customer_ID.nunique():,}", GOLD),
        ("⚑","Fraud Alerts", f"{int(df.Suspicious.sum())}",  RED),
    ]:
        kpi_box(krow,icon,lbl,val,col).pack(side="left", padx=10)
    if "Product_Category" in df.columns:
        tk.Label(content, text="Sales by Category", font=FT,
                 bg=BG, fg=MID).pack(anchor="w", padx=30, pady=(10,0))
        fig, ax = styled_fig(10, 3.2)
        data = df.groupby("Product_Category")["Sales"].sum().sort_values(ascending=False)
        colors = [ACCENT, ACCENT2, GOLD, GREEN, RED][:len(data)]
        bars = ax.bar(data.index, data.values, color=colors, edgecolor=WHITE, width=0.6)
        ax.set_ylabel("₹", color=MID)
        for bar, val in zip(bars, data.values):
            ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()*1.01,
                    f"₹{val/1000:.0f}k", ha="center", fontsize=8, color=MID)
        plt.xticks(rotation=20, ha="right"); plt.tight_layout(); embed(fig)
    watermark()


# ══════════════════════════════════════════════════════════
#  4. SALES BY PRODUCT
# ══════════════════════════════════════════════════════════
def show_sales():
    clear_frame()
    page_title("Sales by Product", ACCENT, show_dashboard)
    if df.empty: watermark(); return
    inn = ctrl_strip(ACCENT)
    cities  = sorted(df.City.unique().tolist())
    city_var= tk.StringVar(value="All")
    tk.Label(inn, text="City:", font=FT, bg=WHITE, fg=DARK).pack(side="left", padx=(0,6))
    ttk.Combobox(inn, textvariable=city_var,
                 values=["All"]+cities, width=20, state="readonly").pack(side="left", padx=(0,18))
    chart_area = tk.Frame(content, bg=BG)
    chart_area.pack(fill="both", expand=True, padx=20, pady=8)

    def plot():
        for w in chart_area.winfo_children(): w.destroy()
        fd = df.copy()
        if city_var.get() != "All": fd = fd[fd.City == city_var.get()]
        if fd.empty:
            tk.Label(chart_area, text="No data.", font=FT, bg=BG, fg=LIGHT).pack(pady=60)
            return
        cl   = [ACCENT,ACCENT2,GOLD,GREEN,RED,"#FF9F43","#A78BFA"]
        data = fd.groupby("Product_Category")["Sales"].sum().sort_values(ascending=False)
        fig  = plt.figure(figsize=(11,5.5), facecolor=WHITE)
        if city_var.get() != "All":
            ax1 = fig.add_axes([0.07,0.42,0.88,0.50])
            ax2 = fig.add_axes([0.07,0.05,0.88,0.32])
            ax1.bar(range(len(data)), data.values, color=cl[:len(data)],
                    edgecolor=WHITE, linewidth=1.2, width=0.6)
            ax1.set_facecolor("#F7FAFF")
            ax1.set_xticks(range(len(data)))
            ax1.set_xticklabels(data.index, rotation=20, ha="right", fontsize=9, color=MID)
            ax1.tick_params(colors=MID, labelsize=9); ax1.set_ylabel("Sales ₹", color=MID)
            ax1.set_title(f"Category Sales — {city_var.get()}", color=DARK, fontsize=11, pad=8)
            for sp in ax1.spines.values(): sp.set_edgecolor(BORDER)
            ax1.grid(color=BORDER, linewidth=0.5, linestyle="--", alpha=0.8, axis="y")
            ax1.set_axisbelow(True)
            for i,v in enumerate(data.values):
                ax1.text(i, v*1.015, f"₹{v:,.0f}", ha="center", fontsize=8, color=MID, fontweight="bold")
            cd  = df.groupby("City")["Sales"].sum().sort_values()
            bcs = [GOLD if c==city_var.get() else "#D8E8F8" for c in cd.index]
            ax2.barh(range(len(cd)), cd.values, color=bcs, edgecolor=WHITE, height=0.6)
            ax2.set_facecolor("#F7FAFF"); ax2.set_yticks(range(len(cd)))
            ax2.set_yticklabels(cd.index, fontsize=7, color=MID)
            ax2.tick_params(colors=MID, labelsize=7); ax2.set_xlabel("Sales ₹", color=MID)
            ax2.set_title(f"All Cities  (gold = {city_var.get()})", color=MID, fontsize=8, pad=4)
            for sp in ax2.spines.values(): sp.set_edgecolor(BORDER)
            ax2.grid(color=BORDER, linewidth=0.4, linestyle="--", alpha=0.6, axis="x")
        else:
            ax = fig.add_axes([0.07,0.12,0.88,0.80])
            ax.bar(range(len(data)), data.values, color=cl[:len(data)],
                   edgecolor=WHITE, linewidth=1.2, width=0.6)
            ax.set_facecolor("#F7FAFF"); ax.set_xticks(range(len(data)))
            ax.set_xticklabels(data.index, rotation=20, ha="right", fontsize=10, color=MID)
            ax.tick_params(colors=MID, labelsize=9); ax.set_ylabel("Sales ₹", color=MID)
            ax.set_title("Category Sales — All Cities", color=DARK, fontsize=12, pad=10)
            for sp in ax.spines.values(): sp.set_edgecolor(BORDER)
            ax.grid(color=BORDER, linewidth=0.5, linestyle="--", alpha=0.8, axis="y")
            ax.set_axisbelow(True)
            for i,v in enumerate(data.values):
                ax.text(i, v*1.015, f"₹{v:,.0f}", ha="center", fontsize=9, color=MID, fontweight="bold")
        embed_in(fig, chart_area)

    big_btn(inn, "Show Graph", plot, GREEN, 18).pack(side="left")
    plot(); watermark()


# ══════════════════════════════════════════════════════════
#  5. INVENTORY & SALES FORECASTING
#  FIX 1: Indentation error in for loop fixed
#  FIX 2: Slider added for live forecast update
#  FIX 3: Full forecast with confidence band
# ══════════════════════════════════════════════════════════
def show_customers():
    clear_frame()
    page_title("Inventory & Sales Forecasting", ACCENT2, show_dashboard)
    if df.empty: watermark(); return

    # ── Data prep ────────────────────────────────────────
    REORDER_PCT  = 0.25
    cat_qty      = df.groupby("Product_Category")["Quantity"].sum()
    cat_sales    = df.groupby("Product_Category")["Sales"].sum()
    cat_profit   = df.groupby("Product_Category")["Profit"].sum()
    max_qty      = cat_qty.max()
    reorder_th   = cat_qty.quantile(REORDER_PCT)
    reorder_n    = int((cat_qty <= reorder_th).sum())
    avg_mo       = int(monthly_sales.mean()) if has_dates else int(df["Sales"].sum()/12)

    # Days-to-stockout estimate
    total_days   = max(df["_date"].nunique(), 1) if (has_dates and "_date" in df.columns) else 365
    cat_daily    = (cat_qty / total_days).replace(0, np.nan)
    cat_stockout = (cat_qty / cat_daily).round(0).fillna(0).astype(int)

    # ── KPI strip ────────────────────────────────────────
    krow = tk.Frame(content, bg=BG); krow.pack(pady=(14,8), padx=22)
    for icon,lbl,val,col in [
        ("📦","Total Units Sold",   f"{int(cat_qty.sum()):,}",  ACCENT),
        ("⚠", "Reorder Alerts",     f"{reorder_n} categories",  RED),
        ("🏆","Top Category",       cat_sales.idxmax(),          GOLD),
        ("📈","Avg Monthly Revenue",f"₹{avg_mo:,.0f}",           GREEN),
    ]:
        kpi_box(krow,icon,lbl,val,col).pack(side="left", padx=10)

    # ── Body layout ──────────────────────────────────────
    body = tk.Frame(content, bg=BG)
    body.pack(fill="both", expand=True, padx=18, pady=(4,10))
    body.grid_columnconfigure(0, weight=4); body.grid_columnconfigure(1, weight=6)
    body.grid_rowconfigure(0, weight=1)

    # ════════════════════
    #  LEFT — Inventory
    # ════════════════════
    inv_outer = tk.Frame(body, bg=WHITE, highlightbackground=ACCENT2, highlightthickness=2)
    inv_outer.grid(row=0, column=0, sticky="nsew", padx=(0,10))
    inv_top = tk.Frame(inv_outer, bg=ACCENT2, padx=14, pady=10); inv_top.pack(fill="x")
    tk.Label(inv_top, text="📦  Stock Levels & Reorder Alerts",
             font=("Segoe UI",12,"bold"), bg=ACCENT2, fg=WHITE).pack(anchor="w")
    tk.Label(inv_top, text="Bottom 25% qty = reorder alert  ·  Days to stockout shown per card",
             font=("Segoe UI",8), bg=ACCENT2, fg="#D8C8F0").pack(anchor="w")

    # Scrollable frame
    canvas_wrap  = tk.Frame(inv_outer, bg=WHITE); canvas_wrap.pack(fill="both", expand=True)
    inv_canvas   = tk.Canvas(canvas_wrap, bg=WHITE, highlightthickness=0)
    inv_scroll   = ttk.Scrollbar(canvas_wrap, orient="vertical", command=inv_canvas.yview)
    inv_canvas.configure(yscrollcommand=inv_scroll.set)
    inv_scroll.pack(side="right", fill="y"); inv_canvas.pack(side="left", fill="both", expand=True)
    scroll_f = tk.Frame(inv_canvas, bg=WHITE)
    scroll_win = inv_canvas.create_window((0,0), window=scroll_f, anchor="nw")
    inv_canvas.bind("<Configure>", lambda e: inv_canvas.itemconfig(scroll_win, width=e.width))
    scroll_f.bind("<Configure>",   lambda e: inv_canvas.configure(scrollregion=inv_canvas.bbox("all")))
    inv_canvas.bind_all("<MouseWheel>",
                        lambda e: inv_canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

    # Rank badges
    rank_badges = {cat_sales.idxmax(): ("🥇 TOP SELLER", GOLD),
                   cat_profit.idxmax(): ("💚 MOST PROFITABLE", GREEN)}
    if cat_qty.idxmin() not in rank_badges:
        rank_badges[cat_qty.idxmin()] = ("⚠ LOWEST STOCK", RED)

    cats_sorted = cat_qty.sort_values(ascending=False)

    # ── FIX 1: All card body code is now properly indented inside the for loop ──
    for rank_i, cat in enumerate(cats_sorted.index):
        qty       = int(cat_qty[cat])
        sale      = cat_sales[cat]
        pft       = cat_profit[cat]
        pct       = qty / max_qty if max_qty > 0 else 0
        alert     = qty <= reorder_th
        days_left = int(cat_stockout.get(cat, 0))

        card_bg  = "#FFF5F5" if alert else WHITE
        card_bdr = RED       if alert else BORDER

        card = tk.Frame(scroll_f, bg=card_bg,
                        highlightbackground=card_bdr, highlightthickness=1)
        card.pack(fill="x", pady=5, padx=8)

        # Top row
        top = tk.Frame(card, bg=card_bg); top.pack(fill="x", padx=12, pady=10)
        lf  = tk.Frame(top,  bg=card_bg); lf.pack(side="left", fill="x", expand=True)
        name_row = tk.Frame(lf, bg=card_bg); name_row.pack(anchor="w")
        tk.Label(name_row, text=f"#{rank_i+1}  {cat}",
                 font=("Segoe UI",11,"bold"), bg=card_bg, fg=DARK).pack(side="left")
        if cat in rank_badges:
            bt, bc = rank_badges[cat]
            bf = tk.Frame(name_row, bg=bc); bf.pack(side="left", padx=(8,0))
            tk.Label(bf, text=bt, font=("Segoe UI",7,"bold"),
                     bg=bc, fg=WHITE).pack(padx=6, pady=2)
        tk.Label(lf, text="🔴 REORDER NOW" if alert else "🟢 In Stock",
                 font=("Segoe UI",8,"bold"), bg=card_bg,
                 fg=RED if alert else GREEN).pack(anchor="w", pady=(2,0))

        rf = tk.Frame(top, bg=card_bg); rf.pack(side="right")
        tk.Label(rf, text=f"{qty:,} units",
                 font=("Segoe UI",13,"bold"), bg=card_bg,
                 fg=RED if alert else GOLD).pack(anchor="e")
        days_col = RED if days_left<30 else (GOLD if days_left<90 else GREEN)
        tk.Label(rf, text=f"⏳ ~{days_left} days left",
                 font=("Segoe UI",8,"bold"), bg=card_bg, fg=days_col).pack(anchor="e")

        # Progress bar
        bar_frame = tk.Frame(card, bg=card_bg); bar_frame.pack(fill="x", padx=12, pady=(2,4))
        bar_bg    = tk.Frame(bar_frame, bg=BORDER, height=10); bar_bg.pack(fill="x")
        bar_bg.update_idletasks()
        bw       = max(bar_bg.winfo_width(), 220)
        fill_col = RED if alert else (GOLD if pct<0.55 else GREEN)
        tk.Frame(bar_bg, bg=fill_col, height=10,
                 width=max(int(bw*pct),4)).place(x=0, y=0)
        tk.Label(bar_frame, text=f"{int(pct*100)}% of max stock",
                 font=("Segoe UI",7), bg=card_bg, fg=MID).pack(anchor="e")

        # Stats row
        sf = tk.Frame(card, bg=card_bg); sf.pack(fill="x", padx=12, pady=(0,8))
        for lt, vt, ct in [("💰 Sales",f"₹{sale:,.0f}",ACCENT),
                            ("📊 Profit",f"₹{pft:,.0f}",GREEN),
                            ("📦 Qty",f"{qty:,}",MID)]:
            pill = tk.Frame(sf, bg=GLASS_B); pill.pack(side="left", padx=(0,6), pady=2)
            tk.Label(pill, text=lt, font=("Segoe UI",7),    bg=GLASS_B, fg=MID).pack(padx=8, pady=(3,0))
            tk.Label(pill, text=vt, font=("Segoe UI",8,"bold"), bg=GLASS_B, fg=ct).pack(padx=8, pady=(0,3))

    # ════════════════════
    #  RIGHT — Forecast
    # ════════════════════
    fc_outer = tk.Frame(body, bg=WHITE, highlightbackground=GOLD, highlightthickness=2)
    fc_outer.grid(row=0, column=1, sticky="nsew")
    fc_top = tk.Frame(fc_outer, bg=GOLD, padx=14, pady=10); fc_top.pack(fill="x")
    tk.Label(fc_top, text="📈  Revenue Forecast — Drag Slider to Predict",
             font=("Segoe UI",12,"bold"), bg=GOLD, fg=WHITE).pack(anchor="w")
    tk.Label(fc_top, text="Based on real monthly data  ·  Linear trend + confidence band",
             font=("Segoe UI",8), bg=GOLD, fg="#FFF8E0").pack(anchor="w")

    # ── FIX 2: Slider row ────────────────────────────────
    sl_row = tk.Frame(fc_outer, bg=WHITE, padx=14, pady=10); sl_row.pack(fill="x")
    tk.Label(sl_row, text="Forecast Months:", font=("Segoe UI",11,"bold"),
             bg=WHITE, fg=MID).pack(side="left", padx=(0,12))
    months_var = tk.IntVar(value=3)
    val_lbl    = tk.Label(sl_row, text="3 months ahead",
                          font=("Segoe UI",12,"bold"), bg=WHITE, fg=GOLD, width=16)
    val_lbl.pack(side="right", padx=(0,10))

    # FIX 3: Forecast area + insight label
    tk.Frame(fc_outer, bg=BORDER, height=1).pack(fill="x")
    fc_chart = tk.Frame(fc_outer, bg=WHITE); fc_chart.pack(fill="both", expand=True, padx=8, pady=(0,4))
    insight  = tk.Label(fc_outer, text="", font=("Segoe UI",9,"bold"),
                        bg=WHITE, fg=DARK, pady=6, padx=14, anchor="w")
    insight.pack(fill="x")

    # Pre-compute regression
    if has_dates and monthly_sales is not None:
        y_all    = monthly_sales.values.astype(float)
        x_all    = np.arange(len(y_all))
        coeffs   = np.polyfit(x_all, y_all, 1)
        std_res  = float(np.std(y_all - np.polyval(coeffs, x_all)))
        mo_labels= [str(p) for p in monthly_sales.index]
    else:
        cs       = cat_sales.sort_values(ascending=False)
        y_all    = cs.values.astype(float)
        x_all    = np.arange(len(y_all))
        coeffs   = np.polyfit(x_all, y_all, 1)
        std_res  = float(np.std(y_all - np.polyval(coeffs, x_all)))
        mo_labels= list(cs.index)

    slope    = coeffs[0]
    mean_rev = float(np.mean(y_all))

    # ── FIX 2: update_forecast — live on slider drag ──────
    def update_forecast(*_):
        n = months_var.get()
        val_lbl.config(text=f"{n} month{'s' if n>1 else ''} ahead")
        x_fut  = np.arange(len(y_all), len(y_all)+n)
        y_pred = np.polyval(coeffs, x_fut)
        lower  = y_pred - std_res*(1.0 + np.arange(n)*0.12)
        upper  = y_pred + std_res*(1.0 + np.arange(n)*0.12)

        fig, ax = plt.subplots(figsize=(6.8,4.2), facecolor=WHITE)
        ax.set_facecolor("#F7FAFF"); ax.tick_params(colors=MID, labelsize=8)
        for sp in ax.spines.values(): sp.set_edgecolor(BORDER); sp.set_linewidth(0.8)
        ax.grid(color=BORDER, linewidth=0.5, linestyle="--", alpha=0.8); ax.set_axisbelow(True)

        n_show   = min(8, len(y_all))
        x_show   = x_all[-n_show:]; y_show = y_all[-n_show:]
        lbl_show = mo_labels[-n_show:]

        # Actual line
        ax.plot(x_show, y_show, color=ACCENT, linewidth=2.4,
                marker="o", markerfacecolor=WHITE, markeredgecolor=ACCENT, markersize=6,
                label="Actual Revenue", zorder=3)
        ax.fill_between(x_show, y_show-std_res*0.3, y_show+std_res*0.3,
                        alpha=0.08, color=ACCENT)
        # Bridge
        ax.plot([x_all[-1], x_fut[0]], [y_all[-1], y_pred[0]],
                color=LIGHT, linewidth=1.5, linestyle=":", zorder=2)
        # Forecast
        ax.plot(x_fut, y_pred, color=GOLD, linewidth=2.4,
                marker="D", markerfacecolor=WHITE, markeredgecolor=GOLD, markersize=6,
                linestyle="--", label=f"Forecast ({n}m)", zorder=3)
        ax.fill_between(x_fut, lower, upper, alpha=0.18, color=GOLD, label="Confidence Band")

        # Labels on forecast points
        for xi, yp in zip(x_fut, y_pred):
            ax.text(xi, yp+std_res*0.08, f"₹{yp/1000:.1f}k",
                    ha="center", fontsize=7.5, color=GOLD, fontweight="bold")

        # Divider
        ax.axvline(x=x_all[-1]+0.5, color=LIGHT, linewidth=1.2, linestyle="--", alpha=0.7)
        ax.text(x_all[-1]+0.55, ax.get_ylim()[0], " Actual ◀ | ▶ Forecast",
                fontsize=7, color=MID, va="bottom")

        # X labels
        all_ticks  = list(x_show) + list(x_fut)
        all_labels = list(lbl_show) + [f"M+{i+1}" for i in range(n)]
        ax.set_xticks(all_ticks)
        ax.set_xticklabels(all_labels, rotation=30, ha="right", fontsize=8)
        ax.set_ylabel("Revenue (₹)", color=MID, fontsize=9)
        ax.set_title(f"Revenue Forecast — {n} Month{'s' if n>1 else ''} Ahead",
                     color=DARK, fontsize=11, pad=8)
        ax.legend(facecolor=WHITE, edgecolor=BORDER, labelcolor=DARK,
                  fontsize=8, loc="upper left")
        plt.tight_layout()
        embed_in(fig, fc_chart)

        direction = "↑ INCREASING" if slope>=0 else "↓ DECREASING"
        pct_mo    = abs(slope)/mean_rev*100 if mean_rev else 0
        insight.config(
            text=f"Trend: {direction}  ·  ~{pct_mo:.1f}% per month  "
                 f"·  Month+{n} Prediction: ₹{y_pred[-1]:,.0f}",
            fg=GREEN if slope>=0 else RED)

    # Slider — triggers live update on drag
    slider = tk.Scale(sl_row, from_=1, to=6, orient="horizontal",
                      variable=months_var, bg=WHITE, fg=DARK,
                      troughcolor=GLASS_B, activebackground=GOLD,
                      highlightthickness=0, bd=0, length=260,
                      showvalue=False, sliderlength=24,
                      command=update_forecast)
    slider.pack(side="left", fill="x", expand=True)

    update_forecast()   # draw initial chart
    watermark()


# ══════════════════════════════════════════════════════════
#  6. FRAUD RISK SCORE PREDICTOR
# ══════════════════════════════════════════════════════════
def show_fraud_risk():
    clear_frame()
    page_title("Fraud Risk Score Predictor", ORANGE, show_dashboard)
    mean_sales = df["Sales"].mean() if not df.empty else 5000

    body = tk.Frame(content, bg=BG)
    body.pack(fill="both", expand=True, padx=24, pady=12)
    body.grid_columnconfigure(0, weight=3); body.grid_columnconfigure(1, weight=4)
    body.grid_rowconfigure(0, weight=1)

    form_outer = tk.Frame(body, bg=WHITE, highlightbackground=BORDER, highlightthickness=1)
    form_outer.grid(row=0, column=0, sticky="nsew", padx=(0,10))
    tk.Frame(form_outer, bg=ORANGE, height=4).pack(fill="x")
    form_inn = tk.Frame(form_outer, bg=WHITE, padx=26, pady=20)
    form_inn.pack(fill="both", expand=True)
    tk.Label(form_inn, text="🔍  Enter Transaction Details",
             font=("Segoe UI",13,"bold"), bg=WHITE, fg=DARK).pack(anchor="w", pady=(0,14))

    entries = {}

    def form_field(parent, label, default="", wtype="entry", options=None):
        row = tk.Frame(parent, bg=WHITE); row.pack(fill="x", pady=5)
        tk.Label(row, text=label, font=("Segoe UI",9,"bold"),
                 bg=WHITE, fg=MID, width=22, anchor="w").pack(side="left")
        if wtype == "entry":
            wrap = tk.Frame(row, bg=BORDER, padx=1, pady=1); wrap.pack(side="left", fill="x", expand=True)
            e = tk.Entry(wrap, font=("Segoe UI",11), bg=WHITE, fg=DARK,
                         insertbackground=ORANGE, bd=0, highlightthickness=0)
            e.insert(0, default); e.pack(fill="x", ipady=7, padx=8)
            e.bind("<FocusIn>",  lambda _: wrap.config(bg=ORANGE))
            e.bind("<FocusOut>", lambda _: wrap.config(bg=BORDER))
            return e
        else:
            var = tk.StringVar(value=default)
            ttk.Combobox(row, textvariable=var, values=options,
                         width=22, state="readonly", font=("Segoe UI",10)).pack(side="left")
            return var

    cats  = sorted(df["Product_Category"].unique()) if not df.empty else ["Electronics"]
    pays  = sorted(df["Payment_Method"].unique())   if not df.empty else ["Credit Card"]
    ctys  = sorted(df["City"].unique())             if not df.empty else ["Mumbai"]

    entries["amount"]  = form_field(form_inn, "Transaction Amount (₹):", "5000")
    entries["age"]     = form_field(form_inn, "Customer Age:", "30")
    entries["cat"]     = form_field(form_inn, "Product Category:", cats[0], "combo", cats)
    entries["pay"]     = form_field(form_inn, "Payment Method:",   pays[0], "combo", pays)
    entries["city"]    = form_field(form_inn, "City:",             ctys[0], "combo", ctys)
    entries["orders"]  = form_field(form_inn, "No. of Orders Today:", "1")
    entries["new_cust"]= form_field(form_inn, "New Customer:", "Yes", "combo", ["Yes","No"])
    entries["time"]    = form_field(form_inn, "Time of Transaction:", "Afternoon (12–6pm)",
                                    "combo", ["Early Morning (12–6am)","Morning (6–12pm)",
                                              "Afternoon (12–6pm)","Night (6–12am)"])

    tk.Frame(form_inn, bg=BORDER, height=1).pack(fill="x", pady=(16,12))

    result_outer = tk.Frame(body, bg=WHITE, highlightbackground=BORDER, highlightthickness=1)
    result_outer.grid(row=0, column=1, sticky="nsew")
    tk.Frame(result_outer, bg=ORANGE, height=4).pack(fill="x")
    result_inn = tk.Frame(result_outer, bg=WHITE, padx=28, pady=20)
    result_inn.pack(fill="both", expand=True)
    tk.Label(result_inn, text="⚡  Risk Assessment",
             font=("Segoe UI",13,"bold"), bg=WHITE, fg=DARK).pack(anchor="w", pady=(0,10))

    gauge_frame = tk.Frame(result_inn, bg=WHITE); gauge_frame.pack(fill="both", expand=True)

    def draw_gauge(score, level, color, reasons):
        for w in gauge_frame.winfo_children(): w.destroy()
        fig, ax = plt.subplots(figsize=(5.5,3), facecolor=WHITE)
        ax.set_facecolor(WHITE); ax.set_xlim(0,10); ax.set_ylim(0,5.5); ax.axis("off")
        theta = np.linspace(np.pi,0,200); r=2.2; cx,cy=5,1.2
        ax.plot(cx+r*np.cos(theta), cy+r*np.sin(theta),
                color=BORDER, linewidth=18, solid_capstyle="round")
        theta_fill = np.linspace(np.pi, np.pi-(score/100)*np.pi, 200)
        ax.plot(cx+r*np.cos(theta_fill), cy+r*np.sin(theta_fill),
                color=color, linewidth=18, solid_capstyle="round", zorder=2)
        na = np.pi-(score/100)*np.pi
        ax.annotate("", xy=(cx+(r-0.1)*np.cos(na), cy+(r-0.1)*np.sin(na)),
                    xytext=(cx,cy),
                    arrowprops=dict(arrowstyle="-|>",color=DARK,lw=2,mutation_scale=12))
        ax.plot(cx,cy,"o",color=DARK,markersize=10,zorder=5)
        for val,ang in [(0,np.pi),(25,np.pi*.75),(50,np.pi*.5),(75,np.pi*.25),(100,0)]:
            ax.text(cx+(r+0.35)*np.cos(ang), cy+(r+0.35)*np.sin(ang),
                    str(val), ha="center", va="center", fontsize=8, color=MID)
        for lb2,ang,c2 in [("LOW",np.pi*.88,GREEN),("MED",np.pi*.5,GOLD),("HIGH",np.pi*.12,RED)]:
            ax.text(cx+(r-0.7)*np.cos(ang), cy+(r-0.7)*np.sin(ang),
                    lb2, ha="center", va="center", fontsize=7, color=c2, fontweight="bold")
        ax.text(cx,cy+0.9,f"{score}",ha="center",va="center",fontsize=34,fontweight="bold",color=color)
        ax.text(cx,cy+0.3,"RISK SCORE",ha="center",va="center",fontsize=9,color=MID)
        ax.text(cx,cy-0.3,f"[ {level} ]",ha="center",va="center",fontsize=11,fontweight="bold",color=color)
        plt.tight_layout(pad=0.2); embed_in(fig, gauge_frame)

        rf = tk.Frame(result_inn, bg=WHITE); rf.pack(fill="x", pady=(8,0))
        tk.Label(rf, text="Risk Factors Detected:",
                 font=("Segoe UI",10,"bold"), bg=WHITE, fg=DARK).pack(anchor="w")
        for rt,rs,rc in reasons:
            rrow = tk.Frame(rf, bg=WHITE); rrow.pack(fill="x", pady=2)
            icon = "🔴" if rs>=20 else ("🟡" if rs>=10 else "🟢")
            tk.Label(rrow, text=f"{icon}  {rt}", font=("Segoe UI",9),
                     bg=WHITE, fg=DARK, anchor="w").pack(side="left")
            tk.Label(rrow, text=f"+{rs} pts", font=("Segoe UI",9,"bold"),
                     bg=WHITE, fg=rc).pack(side="right")

        rec = {"LOW":(GREEN,"#F0FFF5","✅ Transaction appears normal. Approve."),
               "MEDIUM":(GOLD,"#FFFBF0","⚠️ Moderate risk. Request verification."),
               "HIGH":(RED,"#FFF0F0","🚨 High risk! Block and notify security.")}
        rc2,rbg,rtext = rec.get(level,(MID,GLASS_B,"Review manually."))
        rb = tk.Frame(result_inn, bg=rbg, padx=14, pady=10,
                      highlightbackground=rc2, highlightthickness=1)
        rb.pack(fill="x", pady=(10,0))
        tk.Label(rb, text="Recommendation", font=("Segoe UI",9,"bold"), bg=rbg, fg=rc2).pack(anchor="w")
        tk.Label(rb, text=rtext, font=("Segoe UI",9), bg=rbg, fg=DARK,
                 wraplength=360, justify="left").pack(anchor="w", pady=(3,0))

    tk.Label(gauge_frame,
             text="Fill in the transaction details\nand click  ›  Calculate Risk Score",
             font=("Segoe UI",12), bg=WHITE, fg=LIGHT, justify="center"
             ).pack(expand=True, pady=60)

    def calculate_risk():
        try:
            sale_val = float(entries["amount"].get())
            age_val  = int(entries["age"].get())
            n_orders = int(entries["orders"].get())
        except ValueError:
            messagebox.showwarning("Invalid Input",
                "Please enter valid numbers for Amount, Age, and Orders."); return
        payment=entries["pay"].get(); city=entries["city"].get()
        is_new=entries["new_cust"].get(); tod=entries["time"].get()
        score=0; reasons=[]
        ratio = sale_val/mean_sales if mean_sales else 1
        if ratio>5:   score+=35; reasons.append((f"Amount ₹{sale_val:,.0f} is {ratio:.1f}× avg",35,RED))
        elif ratio>3: score+=25; reasons.append((f"Amount {ratio:.1f}× above average",25,ORANGE))
        elif ratio>1.5: score+=10; reasons.append(("Slightly above average",10,GOLD))
        else: reasons.append(("Amount within normal range",0,GREEN))
        if "Early Morning" in tod: score+=20; reasons.append(("Unusual hour (12–6am)",20,RED))
        elif "Night" in tod:       score+=10; reasons.append(("Late night transaction",10,GOLD))
        else:                      reasons.append(("Business hours transaction",0,GREEN))
        if is_new=="Yes":
            score+=10; reasons.append(("New customer account",10,GOLD))
            if sale_val>mean_sales*2: score+=15; reasons.append(("New customer + high-value",15,RED))
        if n_orders>=5:   score+=20; reasons.append((f"{n_orders} orders today — velocity spike",20,RED))
        elif n_orders>=3: score+=8;  reasons.append((f"{n_orders} orders today",8,GOLD))
        else:             reasons.append(("Normal order frequency",0,GREEN))
        if any(rp.lower() in payment.lower() for rp in ["cash on delivery","cod","cash"]):
            score+=12; reasons.append((f"Payment '{payment}' higher risk",12,GOLD))
        if age_val<16 or age_val>85: score+=12; reasons.append((f"Unusual age ({age_val})",12,GOLD))
        if not df.empty and city in df["City"].values:
            cfr = df[df["City"]==city]["Suspicious"].mean()
            if cfr>0.15:  score+=15; reasons.append((f"{city} elevated fraud history",15,RED))
            elif cfr>0.08:score+=6;  reasons.append((f"{city} moderate fraud signals",6,GOLD))
        nz=[(r,s,c) for r,s,c in reasons if s>0]
        zeros=[(r,s,c) for r,s,c in reasons if s==0]
        score=min(score,100)
        level="LOW" if score<=30 else ("MEDIUM" if score<=60 else "HIGH")
        color=GREEN if score<=30 else (GOLD if score<=60 else RED)
        draw_gauge(score,level,color,nz+zeros[:2])

    calc_btn = tk.Button(form_inn, text="▶   Calculate Risk Score",
                         font=("Segoe UI",12,"bold"), bg=ORANGE, fg=WHITE,
                         activebackground=DARK, bd=0, cursor="hand2",
                         pady=11, relief="flat", command=calculate_risk)
    calc_btn.pack(fill="x")
    calc_btn.bind("<Enter>", lambda e: calc_btn.config(bg=DARK))
    calc_btn.bind("<Leave>", lambda e: calc_btn.config(bg=ORANGE))

    def reset_form():
        for w in gauge_frame.winfo_children(): w.destroy()
        for f in result_inn.winfo_children():
            if f != gauge_frame: f.destroy()
        tk.Label(gauge_frame,
                 text="Fill in the transaction details\nand click  ›  Calculate Risk Score",
                 font=("Segoe UI",12), bg=WHITE, fg=LIGHT,
                 justify="center").pack(expand=True, pady=60)

    tk.Button(form_inn, text="↺  Reset", font=("Segoe UI",10),
              bg=WHITE, fg=MID, activebackground=GLASS_B,
              bd=0, cursor="hand2", pady=6, command=reset_form
              ).pack(fill="x", pady=(6,0))
    watermark()


# ══════════════════════════════════════════════════════════
#  7. PURCHASE PATTERNS
# ══════════════════════════════════════════════════════════
def show_patterns():
    clear_frame()
    page_title("Purchase Patterns", GOLD, show_dashboard)
    if df.empty: watermark(); return
    inn = ctrl_strip(GOLD)
    tk.Label(inn, text="View:", font=FT, bg=WHITE, fg=DARK).pack(side="left", padx=(0,8))
    view_var = tk.StringVar(value="By Age")
    ttk.Combobox(inn, textvariable=view_var,
                 values=["By Age","By Gender","By State","By City (Top 10)"],
                 width=22, state="readonly").pack(side="left")
    chart_area = tk.Frame(content, bg=BG)
    chart_area.pack(fill="both", expand=True, padx=20, pady=8)

    def plot():
        for w in chart_area.winfo_children(): w.destroy()
        v = view_var.get()
        if v == "By Age":
            fig, ax = styled_fig(10,4.4)
            data = df.groupby("Age")["Sales"].sum().sort_index()
            ages = data.index.tolist(); vals = data.values
            ax.plot(ages,vals,color=ACCENT,linewidth=2.5,marker="o",markerfacecolor=WHITE,markersize=5,zorder=3)
            ax.fill_between(ages,vals,alpha=0.12,color=ACCENT)
            if "Profit" in df.columns:
                pd2 = df.groupby("Age")["Profit"].sum().sort_index()
                ax.plot(pd2.index,pd2.values,color=GREEN,linewidth=1.8,linestyle="--",
                        marker="s",markerfacecolor=WHITE,markersize=4,label="Profit",zorder=3)
                ax.fill_between(pd2.index,pd2.values,alpha=0.06,color=GREEN)
                ax.legend(facecolor=WHITE,edgecolor=BORDER,labelcolor=DARK,fontsize=8)
            pk = ages[int(np.argmax(vals))]; pv = vals.max()
            ax.annotate(f"Peak\nAge {pk}", xy=(pk,pv), xytext=(pk+3,pv*0.92),
                        arrowprops=dict(arrowstyle="->",color=GOLD,lw=1.2), fontsize=8,color=GOLD)
            ax.set_xlabel("Age",color=MID); ax.set_ylabel("Sales ₹",color=MID)
            ax.set_title("Sales & Profit Trend by Age",color=DARK,fontsize=11)
            plt.tight_layout()
        elif v == "By Gender":
            fig,axes = plt.subplots(1,2,figsize=(10,4.2),facecolor=WHITE)
            for ax in axes: ax.set_facecolor(WHITE)
            sd=df.groupby("Gender")["Sales"].sum(); od=df.groupby("Gender")["Sales"].count()
            pal=[ACCENT,ACCENT2,GOLD,GREEN]
            for ax,data,title,unit in [(axes[0],sd,"Revenue Share","₹"),(axes[1],od,"Order Count","#")]:
                wedges,texts,aut=ax.pie(data.values,labels=data.index,autopct="%1.1f%%",
                    colors=pal[:len(data)],startangle=90,
                    wedgeprops=dict(width=0.55,edgecolor=WHITE,linewidth=2),
                    textprops={"color":DARK,"fontsize":10})
                for at in aut: at.set_fontsize(9)
                total=data.sum()
                ax.text(0,0,f"{unit}{total:,.0f}" if unit=="₹" else f"{total:,}",
                        ha="center",va="center",fontsize=10,color=DARK,fontweight="bold")
                ax.set_title(title,color=DARK,fontsize=11,pad=10)
            plt.tight_layout()
        elif v == "By State":
            fig,ax=styled_fig(10,4.6)
            data=df.groupby("State")["Sales"].sum().nlargest(12).sort_values()
            y_pos=range(len(data))
            ax.barh(y_pos,data.values,height=0.04,color=LIGHT,alpha=0.6)
            ax.scatter(data.values,y_pos,s=160,
                       c=[ACCENT if i==len(data)-1 else GOLD for i in range(len(data))],
                       edgecolors=WHITE,linewidths=1.5,zorder=3)
            ax.set_yticks(y_pos); ax.set_yticklabels(data.index,fontsize=8)
            ax.set_xlabel("Sales ₹",color=MID)
            ax.set_title("Top 12 States — Lollipop",color=DARK,fontsize=11)
            for i,v2 in enumerate(data.values):
                ax.text(v2*1.005,i,f"₹{v2/1000:.0f}k",va="center",fontsize=7,color=MID)
            plt.tight_layout()
        else:
            fig,ax=styled_fig(10,4.4)
            top_cities=df.groupby("City")["Sales"].sum().nlargest(10).index.tolist()
            pivot=df[df.City.isin(top_cities)].pivot_table(
                index="City",columns="Product_Category",values="Sales",
                aggfunc="sum",fill_value=0).loc[top_cities]
            cat_colors=[ACCENT,ACCENT2,GOLD,GREEN,RED,"#FF9F43","#A78BFA"]
            bottom=np.zeros(len(top_cities)); x_pos=np.arange(len(top_cities))
            for i,cat in enumerate(pivot.columns):
                vals=pivot[cat].values.astype(float)
                ax.bar(x_pos,vals,bottom=bottom,color=cat_colors[i%len(cat_colors)],
                       edgecolor=WHITE,linewidth=0.8,width=0.65,label=cat)
                for j,(v2,b) in enumerate(zip(vals,bottom)):
                    if v2>pivot.values.max()*0.06:
                        ax.text(j,b+v2/2,f"{v2/1000:.0f}k",ha="center",va="center",fontsize=5.5,color=WHITE)
                bottom+=vals
            ax.set_xticks(x_pos); ax.set_xticklabels(top_cities,rotation=30,ha="right",fontsize=8)
            ax.set_ylabel("Sales ₹",color=MID)
            ax.set_title("Top 10 Cities — Stacked by Category",color=DARK,fontsize=11)
            ax.legend(facecolor=WHITE,edgecolor=BORDER,labelcolor=DARK,fontsize=7,loc="upper right",ncol=2)
            plt.tight_layout()
        embed_in(fig, chart_area)

    big_btn(inn,"View Trend",plot,GOLD,16).pack(side="left",padx=14)
    plot(); watermark()


# ══════════════════════════════════════════════════════════
#  8. PROFIT ANALYSIS
#  FIX 4: canvas_widget = embed_in(...) removed (embed_in returns None)
#  FIX 5: _build_interactive_meter now self-contained, no import errors
# ══════════════════════════════════════════════════════════
def show_profit():
    clear_frame()
    page_title("Profit Intelligence Dashboard", GREEN, show_dashboard)
    if df.empty: watermark(); return

    ts = df["Sales"].sum(); tp = df["Profit"].sum()
    tc = df["Cost"].sum() if "Cost" in df.columns else ts-tp
    mg = (tp/ts*100) if ts else 0

    krow = tk.Frame(content, bg=BG); krow.pack(pady=12)
    for icon,lbl,val,col in [
        ("₹","Total Sales",  f"₹{ts:,.0f}", ACCENT),
        ("−","Total Cost",   f"₹{tc:,.0f}", RED),
        ("+","Total Profit", f"₹{tp:,.0f}", GREEN),
        ("%","Profit Margin",f"{mg:.1f}%",  GOLD),
    ]:
        kpi_box(krow,icon,lbl,val,col).pack(side="left", padx=10)

    topbar   = ctrl_strip(GREEN)
    view_var = tk.StringVar(value="Profit Donut")
    ttk.Combobox(topbar, textvariable=view_var,
                 values=["Profit Donut","Top Categories","Profit Meter"],
                 state="readonly", width=22).pack(side="left", padx=(0,15))
    chart_area = tk.Frame(content, bg=BG); chart_area.pack(fill="both", expand=True, padx=20, pady=10)

    def plot():
        for w in chart_area.winfo_children(): w.destroy()
        view = view_var.get()

        if view == "Profit Donut":
            fig, ax = styled_fig(6,4)
            values=[tp,tc]; labels=["Profit","Cost"]; colors=[GREEN,RED]
            wedges, _ = ax.pie(values, colors=colors, startangle=90,
                                wedgeprops=dict(width=0.42, edgecolor=WHITE))
            ax.text(0,0,f"₹{tp:,.0f}",ha="center",va="center",
                    fontsize=16,color=DARK,fontweight="bold")
            ax.set_title("Profit Distribution",fontsize=14,color=DARK)
            ax.legend(wedges,labels,loc="upper right",frameon=False)
            embed_in(fig, chart_area)

        elif view == "Top Categories":
            fig, ax = styled_fig(9,4)
            data       = df.groupby("Product_Category")["Profit"].sum().sort_values(ascending=False)
            final_vals = data.values.tolist(); cats = data.index.tolist(); n = len(cats)
            steps      = 20

            bars       = ax.bar(cats,[0]*n,color=GREEN,edgecolor=WHITE,linewidth=2)
            ax.set_ylim(0, max(final_vals)*1.15)
            ax.set_title("Top Profit Categories",fontsize=13,color=DARK)
            ax.tick_params(axis="x",rotation=20)

            labels_list = [ax.text(bar.get_x()+bar.get_width()/2, 0, "",
                                   ha="center", fontsize=8, color=DARK)
                           for bar in bars]

            # FIX 4: embed first, then animate — no canvas_widget assignment
            embed_in(fig, chart_area)

            def animate(step):
                frac = (step+1)/steps
                for i, bar in enumerate(bars):
                    h = final_vals[i]*frac
                    bar.set_height(h)
                    labels_list[i].set_position((bar.get_x()+bar.get_width()/2, h))
                    labels_list[i].set_text(f"₹{h:,.0f}" if step==steps-1 else "")
                fig.canvas.draw_idle()
                if step < steps-1:
                    chart_area.after(30, animate, step+1)

            animate(0)

        elif view == "Profit Meter":
            _build_interactive_meter(chart_area, ts, tp, tc, mg)

    big_btn(topbar,"Show Analysis",lambda:plot(),GREEN,16).pack(side="left")
    plot(); watermark()


def _build_interactive_meter(parent, total_sales, total_profit, total_cost, actual_margin):
    """Draggable profit meter gauge — all pure tkinter + math."""
    CANVAS_W, CANVAS_H = 560, 320
    CX, CY, R, TW = 280, 260, 200, 28

    wrapper = tk.Frame(parent, bg=BG); wrapper.pack(expand=True)
    tk.Label(wrapper, text="🎯  Profit Prediction Meter",
             font=("Segoe UI",15,"bold"), bg=BG, fg=GREEN).pack(pady=(10,0))
    tk.Label(wrapper, text="Drag the needle to simulate different profit margins",
             font=("Segoe UI",10), bg=BG, fg=DARK).pack()

    cv = tk.Canvas(wrapper, width=CANVAS_W, height=CANVAS_H, bg=WHITE, highlightthickness=0)
    cv.pack(pady=6)

    info_row = tk.Frame(wrapper, bg=BG); info_row.pack(pady=4)

    def _info_box(parent, label, color):
        f = tk.Frame(parent, bg=WHITE, bd=1, relief="solid")
        f.pack(side="left", padx=12, ipadx=14, ipady=6)
        tk.Label(f, text=label, font=("Segoe UI",9), bg=WHITE, fg=DARK).pack()
        var = tk.StringVar(value="—")
        tk.Label(f, textvariable=var, font=("Segoe UI",13,"bold"), bg=WHITE, fg=color).pack()
        return var

    pm_var  = _info_box(info_row, "Target Margin %",  GOLD)
    pp_var  = _info_box(info_row, "Predicted Profit",  GREEN)
    pc_var  = _info_box(info_row, "Predicted Cost",    RED)
    rs_var  = _info_box(info_row, "Sales Needed",      ACCENT)

    tk.Label(wrapper, text=f"Actual margin: {actual_margin:.1f}%  |  Actual profit: ₹{total_profit:,.0f}",
             font=("Segoe UI",9,"italic"), bg=BG, fg=DARK).pack(pady=(2,8))

    def _angle_for(pct): return 180 - pct*1.8

    def _needle_tip(angle_deg):
        a = math.radians(angle_deg)
        return (CX + R*math.cos(a), CY - R*math.sin(a))

    def _draw_gauge(pct):
        cv.delete("all")
        cv.create_arc(CX-R, CY-R, CX+R, CY+R, start=0, extent=180,
                      style="arc", outline="#E0E0E0", width=TW)
        if pct > 0:
            fill_col = RED if pct<40 else (GOLD if pct<70 else GREEN)
            cv.create_arc(CX-R, CY-R, CX+R, CY+R, start=180, extent=-(pct*1.8),
                          style="arc", outline=fill_col, width=TW)
        for p in range(0,101,20):
            a  = math.radians(_angle_for(p))
            x1 = CX+(R-TW-2)*math.cos(a); y1 = CY-(R-TW-2)*math.sin(a)
            x2 = CX+(R+TW+2)*math.cos(a); y2 = CY-(R+TW+2)*math.sin(a)
            cv.create_line(x1,y1,x2,y2, fill=DARK, width=2)
            cv.create_text(CX+(R+TW+16)*math.cos(a), CY-(R+TW+16)*math.sin(a),
                           text=f"{p}%", font=("Segoe UI",8,"bold"), fill=DARK)
        aa = math.radians(_angle_for(actual_margin))
        cv.create_line(CX+(R-TW-10)*math.cos(aa), CY-(R-TW-10)*math.sin(aa),
                       CX+(R+TW+10)*math.cos(aa), CY-(R+TW+10)*math.sin(aa),
                       fill=ACCENT, width=3, dash=(6,3))
        cv.create_text(CX+(R+TW+14)*math.cos(aa)-4, CY-(R+TW+14)*math.sin(aa)-10,
                       text="Actual", font=("Segoe UI",8,"italic"), fill=ACCENT, anchor="w")
        tip_x,tip_y = _needle_tip(_angle_for(pct))
        cv.create_line(CX,CY,tip_x,tip_y, fill=DARK, width=4, tags="needle")
        cv.create_oval(CX-10,CY-10,CX+10,CY+10, fill=DARK, outline="", tags="hub")
        cv.create_text(CX,CY-42, text=f"{pct:.1f}%",
                       font=("Segoe UI",22,"bold"), fill=DARK, tags="cpct")

    def _update_info(pct):
        pm_var.set(f"{pct:.1f}%")
        pred_p = total_sales*pct/100; pred_c = total_sales-pred_p
        req_s  = total_cost/(1-pct/100) if pct<100 else float("inf")
        pp_var.set(f"₹{pred_p:,.0f}"); pc_var.set(f"₹{pred_c:,.0f}")
        rs_var.set(f"₹{req_s:,.0f}" if req_s!=float("inf") else "∞")

    state = {"pct": actual_margin, "dragging": False}

    def _pct_from_xy(x,y):
        dx,dy = x-CX, CY-y
        angle = math.degrees(math.atan2(dy,dx))
        angle = max(0.0, min(180.0, angle))
        return (180-angle)/1.8

    def on_press(event):
        tip_x,tip_y = _needle_tip(_angle_for(state["pct"]))
        if math.hypot(event.x-tip_x, event.y-tip_y) < 22:
            state["dragging"] = True

    def on_drag(event):
        if not state["dragging"]: return
        pct = max(1.0, min(99.0, _pct_from_xy(event.x, event.y)))
        state["pct"] = pct; _draw_gauge(pct); _update_info(pct)

    def on_release(_): state["dragging"] = False

    cv.bind("<ButtonPress-1>",   on_press)
    cv.bind("<B1-Motion>",       on_drag)
    cv.bind("<ButtonRelease-1>", on_release)
    _draw_gauge(actual_margin); _update_info(actual_margin)


# ══════════════════════════════════════════════════════════
#  9. PAYMENT METHODS
# ══════════════════════════════════════════════════════════
def show_payment():
    clear_frame()
    page_title("Payment Methods", ACCENT, show_dashboard)
    if df.empty: watermark(); return
    inn  = ctrl_strip(ACCENT)
    pays = sorted(df.Payment_Method.unique().tolist())
    pay_var = tk.StringVar(value="All")
    tk.Label(inn,text="Filter:",font=FT,bg=WHITE,fg=DARK).pack(side="left",padx=(0,8))
    ttk.Combobox(inn,textvariable=pay_var,values=["All"]+pays,width=18,state="readonly").pack(side="left")
    krow_f     = tk.Frame(content,bg=BG); krow_f.pack(pady=(10,0),padx=20)
    chart_area = tk.Frame(content,bg=BG); chart_area.pack(fill="both",expand=True,padx=20,pady=6)

    def plot():
        for w in krow_f.winfo_children():     w.destroy()
        for w in chart_area.winfo_children(): w.destroy()
        fd  = df if pay_var.get()=="All" else df[df.Payment_Method==pay_var.get()]
        top = fd.groupby("Product_Category")["Sales"].sum().idxmax() if len(fd) else "-"
        row = tk.Frame(krow_f,bg=BG); row.pack()
        for icon,lbl,val,col in [
            ("◎","Orders",      f"{len(fd):,}",                         ACCENT),
            ("₹","Sales",       f"₹{fd.Sales.sum():,.0f}",              GOLD),
            ("~","Avg Sale",    f"₹{fd.Sales.mean():,.0f}" if len(fd) else "-", GREEN),
            ("⬡","Top Category",top,                                     ACCENT2),
        ]:
            kpi_box(row,icon,lbl,val,col).pack(side="left",padx=10)
        fig,axes = plt.subplots(1,2,figsize=(10,3.8),facecolor=WHITE)
        for ax in axes:
            ax.set_facecolor("#F7FAFF"); ax.tick_params(colors=MID,labelsize=8)
            for sp in ax.spines.values(): sp.set_edgecolor(BORDER)
        pm = df.groupby("Payment_Method")["Sales"].sum()
        axes[0].pie(pm.values,labels=pm.index,autopct="%1.1f%%",
                    colors=[ACCENT,GOLD,GREEN,ACCENT2,RED],
                    textprops={"color":DARK,"fontsize":9},
                    wedgeprops=dict(edgecolor=WHITE,linewidth=1.5))
        axes[0].set_title("Revenue Share by Payment",color=DARK,fontsize=10)
        pc = fd.groupby("Product_Category")["Sales"].sum().sort_values(ascending=False)
        axes[1].bar(range(len(pc)),pc.values,
                    color=[ACCENT if i==0 else ACCENT2 for i in range(len(pc))],
                    edgecolor=WHITE,linewidth=1)
        axes[1].set_xticks(range(len(pc))); axes[1].set_xticklabels(pc.index,rotation=25,ha="right",fontsize=8)
        axes[1].set_title("Category Sales (filtered)",color=DARK,fontsize=10)
        plt.tight_layout(); embed_in(fig,chart_area)

    big_btn(inn,"Analyse",plot,ACCENT,14).pack(side="left",padx=14)
    plot(); watermark()


# ══════════════════════════════════════════════════════════
#  10. SEARCH — by City
# ══════════════════════════════════════════════════════════
def show_search():
    clear_frame()
    page_title("Search by City", ACCENT, show_dashboard)
    if df.empty: watermark(); return
    inn = ctrl_strip(ACCENT)
    cities   = ["All"]+sorted(df.City.astype(str).unique().tolist())
    city_var = tk.StringVar(value="All")
    tk.Label(inn,text="City:",font=FT,bg=WHITE,fg=DARK).pack(side="left",padx=(0,6))
    ttk.Combobox(inn,textvariable=city_var,values=cities,width=22,
                 state="readonly").pack(side="left",padx=(0,16))
    res_lbl = tk.Label(content, text="Select a City and click Search", font=FT, bg=BG, fg=MID)
    res_lbl.pack(anchor="w", padx=24, pady=(8,0))
    tree_frame = tk.Frame(content, bg=BG); tree_frame.pack(fill="both", expand=True, padx=20, pady=6)

    def search():
        for w in tree_frame.winfo_children(): w.destroy()
        fd = df.copy()
        if city_var.get()!="All": fd=fd[fd.City.astype(str)==city_var.get()]
        if len(fd):
            res_lbl.config(
                text=f"  {len(fd)} orders  ·  City: {city_var.get()}"
                     f"  ·  Sales: ₹{fd.Sales.sum():,.0f}"
                     f"  ·  Profit: ₹{fd.Profit.sum():,.0f}"
                     f"  ·  Customers: {fd['Customer_ID'].nunique()}",
                fg=GREEN)
        else:
            res_lbl.config(text="  No records found for this City.", fg=RED); return
        cols = list(df.columns); apply_treeview_style()
        tree = ttk.Treeview(tree_frame, columns=cols, show="headings", height=15)
        sy   = ttk.Scrollbar(tree_frame, orient="vertical",   command=tree.yview)
        sx   = ttk.Scrollbar(tree_frame, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=sy.set, xscrollcommand=sx.set)
        tree.grid(row=0,column=0,sticky="nsew")
        sy.grid(row=0,column=1,sticky="ns"); sx.grid(row=1,column=0,sticky="ew")
        tree_frame.grid_columnconfigure(0,weight=1); tree_frame.grid_rowconfigure(0,weight=1)
        for c in cols:
            tree.heading(c,text=c.replace("_"," ")); tree.column(c,width=120,anchor="center")
        tree.tag_configure("odd",background="#F7FAFF"); tree.tag_configure("even",background=WHITE)
        for i,(_,r) in enumerate(fd.head(200).iterrows()):
            tree.insert("","end",values=list(r),tags=("odd" if i%2 else "even",))

    def reset():
        city_var.set("All"); res_lbl.config(text="Select a City and click Search",fg=MID)
        for w in tree_frame.winfo_children(): w.destroy()

    big_btn(inn,"Search",search,ACCENT,12).pack(side="left",padx=(14,8))
    big_btn(inn,"Reset", reset, "#A8B8CC",10).pack(side="left")
    watermark()


# ══════════════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════════════
def build_sidebar():
    tk.Frame(sidebar, bg=ACCENT, height=4).pack(fill="x")
    brand = tk.Frame(sidebar, bg=PANEL, pady=18); brand.pack(fill="x")
    tk.Label(brand, text="⬡",        font=("Segoe UI",24),        bg=PANEL, fg=ACCENT).pack()
    tk.Label(brand, text="NITHYA.P",  font=("Segoe UI",13,"bold"), bg=PANEL, fg=DARK).pack(pady=(4,2))
    tk.Label(brand, text="BCA Final Project", font=("Segoe UI",9), bg=PANEL, fg=LIGHT).pack()
    tk.Frame(sidebar, bg=BORDER, height=1).pack(fill="x", pady=(8,0))

    for txt, cmd in [
        ("  📊  Dashboard",            show_dashboard),
        ("  🛒  Sales by Product",     show_sales),
        ("  📦  Inventory & Forecast", show_customers),
        ("  🎯  Fraud Risk Score",     show_fraud_risk),
        ("  📈  Purchase Patterns",    show_patterns),
        ("  💰  Profit Analysis",      show_profit),
        ("  💳  Payment Methods",      show_payment),
        ("  🔎  Search City",          show_search),
    ]:
        sb_btn(txt, cmd)

    tk.Frame(sidebar, bg=PANEL).pack(fill="both", expand=True)
    tk.Frame(sidebar, bg=BORDER, height=1).pack(fill="x")
    sb_btn("  ←  Sign Out", show_login)
    tk.Label(sidebar, text="v4.0  ·  Light Theme",
             font=("Segoe UI",8), bg=PANEL, fg=LIGHT).pack(pady=8)

build_sidebar()
show_login()
root.mainloop()