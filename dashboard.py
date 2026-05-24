import tkinter as tk
from tkinter import ttk
import random

# Global mock database matching your schema variables
MINERALS_DATA = [
    {"name": "Iron Ore", "origin": "Sector A", "price": 120.0},
    {"name": "Copper Ore", "origin": "Sector B", "price": 420.0},
    {"name": "Lithium Crystals", "origin": "Sector C", "price": 950.0},
    {"name": "Gold Filament", "origin": "Sector D", "price": 2300.0},
]

class MineralsEngineApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Minerals Simulation Dashboard")
        self.master.geometry("700x650")
        self.master.configure(bg="#0f172a")

        # Runtime Engine State
        self.is_running = True
        self.ticks = 0
        self.shock_mode = "Normal"
        self.volatility_history = [0.0]
        self.price_history = [200.0]

        # Component Initialization Pipeline
        self.create_layout()
        self.update_loop()

    def create_layout(self):
        # 1. Header Toolbar Controls
        ctrl_frame = tk.Frame(self.master, bg="#0f172a")
        ctrl_frame.pack(fill="x", padx=15, pady=10)

        self.btn_pause = tk.Button(
            ctrl_frame, text="⏸️ PAUSE ENGINE", bg="#1e293b", fg="white",
            command=self.toggle_stream, font=("Arial", 10, "bold"), relief=tk.FLAT, padx=10
        )
        self.btn_pause.pack(side="left", padx=5)

        tk.Label(ctrl_frame, text="Shock Vector:", bg="#0f172a", fg="white", font=("Arial", 10)).pack(side="left", padx=10)
        
        self.shock_var = tk.StringVar(value="Normal")
        self.shock_dropdown = ttk.Combobox(
            ctrl_frame, textvariable=self.shock_var,
            values=["Normal Market", "Supply Shock Crisis", "Macro Crash", "Green Energy Boom"],
            state="readonly"
        )
        self.shock_dropdown.pack(side="left", padx=5)
        self.shock_dropdown.bind("<<ComboboxSelected>>", self.change_shock)

        # 2. KPI Metrics Panels (Fixed: -padding error corrected to standard tk parameters)
        kpi_frame = tk.Frame(self.master, bg="#0f172a")
        kpi_frame.pack(fill="x", padx=15, pady=5)

        self.ticks_card = self.create_kpi_card(kpi_frame, "Network Ticks", "0", "#38bdf8")
        self.ticks_card.pack(side="left", expand=True, fill="x", padx=5)

        self.sentiment_card = self.create_kpi_card(kpi_frame, "Market Sentiment", "STABLE", "#fbbf24")
        self.sentiment_card.pack(side="left", expand=True, fill="x", padx=5)

        # 3. Dynamic Live Table View
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#1e293b", fieldbackground="#1e293b", foreground="white")
        style.configure("Treeview.Heading", background="#334155", foreground="white", relief="flat")

        self.tree = ttk.Treeview(self.master, columns=("Name", "Origin", "Price", "Change"), show="headings", height=6)
        self.tree.heading("Name", text="Mineral Asset")
        self.tree.heading("Origin", text="Origin Core")
        self.tree.heading("Price", text="Market Spot Price")
        self.tree.heading("Change", text="Delta %")
        self.tree.pack(fill="x", padx=15, pady=10)

        # 4. Canvas Real-time Graph Vector
        self.canvas = tk.Canvas(self.master, height=220, bg="#1e293b", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=15, pady=10)

    def create_kpi_card(self, parent, title, init_val, accent_color):
        # Fixed: Changed custom 'py=10' layout attribute to standard 'pady=10'
        card = tk.Frame(parent, bg="#1e293b", bd=1, relief=tk.SOLID, padx=15, pady=10)
        
        lbl_title = tk.Label(card, text=title.upper(), bg="#1e293b", fg="#94a3b8", font=("Arial", 8, "bold"))
        lbl_title.pack(anchor="w")
        
        lbl_val = tk.Label(card, text=init_val, bg="#1e293b", fg=accent_color, font=("Arial", 16, "bold"))
        lbl_val.pack(anchor="w", pady=(5, 0))
        
        # Return internal reference node pointer label directly to mutate layout strings
        card.config_label = lbl_val
        return card

    def change_shock(self, event):
        self.shock_mode = self.shock_var.get()

    def toggle_stream(self):
        self.is_running = not self.is_running
        if not self.is_running:
            self.btn_pause.config(text="▶️ RESUME ENGINE", bg="#16a34a")
        else:
            self.btn_pause.config(text="⏸️ PAUSE ENGINE", bg="#1e293b")

    def update_loop(self):
        if self.is_running:
            self.ticks += 1
            self.ticks_card.config_label.config(text=f"{self.ticks:,}")

            vol_factor = 0.012
            dir_bias = 0.0

            if "Supply" in self.shock_mode:
                vol_factor = 0.040
                dir_bias = 0.010
                self.sentiment_card.config_label.config(text="BULLISH SHOCK", fg="#10b981")
            elif "Macro" in self.shock_mode:
                vol_factor = 0.035
                dir_bias = -0.018
                self.sentiment_card.config_label.config(text="BEARISH CRASH", fg="#ef4444")
            elif "Green" in self.shock_mode:
                vol_factor = 0.028
                dir_bias = 0.015
                self.sentiment_card.config_label.config(text="GREEN BOOM", fg="#38bdf8")
            else:
                self.sentiment_card.config_label.config(text="STABLE", fg="#fbbf24")

            gross_vol = 0.0
            total_market_value = 0.0

            # Flushed rendering clean tracking
            for item in self.tree.get_children():
                self.tree.delete(item)

            for m in MINERALS_DATA:
                change_percent = random.normalvariate(dir_bias, vol_factor)
                old_price = m["price"]
                new_price = max(0.01, old_price * (1 + change_percent))
                m["price"] = new_price
                
                gross_vol += abs(change_percent) * 100
                total_market_value += new_price
                sign = "+" if change_percent >= 0 else ""

                # Fixed: Fixed unterminated string literal compilation bug completely
                self.tree.insert(
                    "", 
                    tk.END, 
                    values=(m["name"], m["origin"], f"${new_price:,.2f}", f"{sign}{change_percent * 100:.2f}%")
                )

            # Store metrics indexes
            avg_vol = gross_vol / len(MINERALS_DATA)
            self.volatility_history.append(avg_vol)
            self.price_history.append(total_market_value / len(MINERALS_DATA))

            if len(self.price_history) > 70:
                self.price_history.pop(0)
                self.volatility_history.pop(0)

            # Fixed: Properly embedded internal renderer logic call structure securely
            self.draw_market_chart()

        # Frame loop timing refresh standard rate: 400ms
        self.master.after(400, self.update_loop)

    def draw_market_chart(self):
        self.canvas.delete("all")
        
        if not self.price_history:
            return
            
        points = []
        max_val = max(self.price_history)
        min_val = min(self.price_history)
        spread = (max_val - min_val) if max_val != min_val else 1
        
        # Safe structural bounds plotting transformations
        for idx, price in enumerate(self.price_history):
            x = 30 + (idx * 9)
            y = 180 - int(((price - min_val) / spread) * 140)
            points.append((x, y))

        # Core logic execution sequence matching loop structures exactly
        for idx in range(len(points) - 1):
            chart_color = "#ef4444" if self.volatility_history[idx + 1] > 3.5 else "#f59e0b"

            # Fixed: Formatted coordinate vectors array values properly into distinct arguments
            self.canvas.create_line(
                points[idx][0], points[idx][1],
                points[idx + 1][0], points[idx + 1][1],
                fill=chart_color,
                width=2
            )

            self.canvas.create_oval(
                points[idx][0] - 2, points[idx][1] - 2,
                points[idx][0] + 2, points[idx][1] + 2,
                fill="#fbbf24",
                outline=""
            )

# Fixed: Removed indentation compilation syntax failures completely
if __name__ == "__main__":
    app_root = tk.Tk()
    engine_app = MineralsEngineApp(app_root)
    app_root.mainloop()
