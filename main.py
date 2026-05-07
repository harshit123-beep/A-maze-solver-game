import tkinter as tk
from tkinter import ttk, messagebox
from maze import Maze

CELL_SIZE = 22

COLORS = {
    "wall":     "#1a1a2e",
    "path":     "#f0f0f0",
    "start":    "#00b4d8",
    "end":      "#ef233c",
    "explored": "#ffd166",
    "solution": "#06d6a0",
    "bg":       "#16213e",
}

class MazeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🤖 AI Maze Solver")
        self.root.configure(bg=COLORS["bg"])
        self.maze = None
        self.animation_id = None
        self.build_ui()
        self.new_maze()

    def build_ui(self):
        # Top control bar
        ctrl = tk.Frame(self.root, bg=COLORS["bg"], pady=8)
        ctrl.pack(fill="x", padx=10)

        tk.Label(ctrl, text="🤖 AI Maze Solver", font=("Helvetica", 16, "bold"),
                 bg=COLORS["bg"], fg="white").pack(side="left", padx=(0, 20))

        tk.Label(ctrl, text="Algorithm:", bg=COLORS["bg"], fg="white",
                 font=("Helvetica", 11)).pack(side="left")

        self.algo_var = tk.StringVar(value="bfs")
        algo_menu = ttk.Combobox(ctrl, textvariable=self.algo_var,
                                 values=["bfs", "dfs", "astar"],
                                 width=8, state="readonly", font=("Helvetica", 11))
        algo_menu.pack(side="left", padx=6)

        tk.Label(ctrl, text="Size:", bg=COLORS["bg"], fg="white",
                 font=("Helvetica", 11)).pack(side="left", padx=(10, 4))

        self.size_var = tk.StringVar(value="21")
        size_menu = ttk.Combobox(ctrl, textvariable=self.size_var,
                                 values=["15", "21", "31", "41"],
                                 width=5, state="readonly", font=("Helvetica", 11))
        size_menu.pack(side="left", padx=6)

        btn_style = {"font": ("Helvetica", 11, "bold"), "relief": "flat",
                     "padx": 12, "pady": 4, "cursor": "hand2"}

        tk.Button(ctrl, text="⟳ New Maze", bg="#0077b6", fg="white",
                  command=self.new_maze, **btn_style).pack(side="left", padx=8)

        tk.Button(ctrl, text="▶ Solve", bg="#06d6a0", fg="#1a1a2e",
                  command=self.solve, **btn_style).pack(side="left", padx=4)

        tk.Button(ctrl, text="✕ Reset", bg="#ef233c", fg="white",
                  command=self.reset_maze, **btn_style).pack(side="left", padx=8)

        # Canvas frame
        self.canvas_frame = tk.Frame(self.root, bg=COLORS["bg"])
        self.canvas_frame.pack(padx=10, pady=4)

        self.canvas = tk.Canvas(self.canvas_frame, bg=COLORS["wall"],
                                highlightthickness=0)
        self.canvas.pack()

        # Stats bar
        self.stats_frame = tk.Frame(self.root, bg="#0d1b2a", pady=6)
        self.stats_frame.pack(fill="x", padx=10, pady=(4, 8))

        self.stat_labels = {}
        stats = [("Path Length", "path_len"), ("Nodes Explored", "nodes"),
                 ("Time (ms)", "time"), ("Algorithm", "algo")]

        for label, key in stats:
            f = tk.Frame(self.stats_frame, bg="#0d1b2a", padx=16)
            f.pack(side="left")
            tk.Label(f, text=label, font=("Helvetica", 9), bg="#0d1b2a",
                     fg="#aaaaaa").pack()
            lbl = tk.Label(f, text="—", font=("Helvetica", 13, "bold"),
                           bg="#0d1b2a", fg="white")
            lbl.pack()
            self.stat_labels[key] = lbl

        # Legend
        leg = tk.Frame(self.root, bg=COLORS["bg"], pady=4)
        leg.pack()
        legend_items = [("Start", "start"), ("End", "end"),
                        ("Explored", "explored"), ("Solution", "solution")]
        for name, key in legend_items:
            tk.Label(leg, text="■", fg=COLORS[key], bg=COLORS["bg"],
                     font=("Helvetica", 14)).pack(side="left", padx=2)
            tk.Label(leg, text=name, fg="white", bg=COLORS["bg"],
                     font=("Helvetica", 10)).pack(side="left", padx=(0, 10))

    def new_maze(self):
        if self.animation_id:
            self.root.after_cancel(self.animation_id)
            self.animation_id = None
        size = int(self.size_var.get())
        self.maze = Maze(rows=size, cols=size)
        self.draw_maze()
        for key in self.stat_labels:
            self.stat_labels[key].config(text="—")

    def draw_maze(self, explored=None, solution=None):
        self.canvas.delete("all")
        rows, cols = self.maze.rows, self.maze.cols
        cs = CELL_SIZE

        self.canvas.config(width=cols * cs, height=rows * cs)

        explored_set = set(explored) if explored else set()
        solution_set = set(solution) if solution else set()

        for r in range(rows):
            for c in range(cols):
                x1, y1 = c * cs, r * cs
                x2, y2 = x1 + cs, y1 + cs
                cell = (r, c)

                if cell == self.maze.start:
                    color = COLORS["start"]
                elif cell == self.maze.end:
                    color = COLORS["end"]
                elif cell in solution_set:
                    color = COLORS["solution"]
                elif cell in explored_set:
                    color = COLORS["explored"]
                elif self.maze.grid[r][c] == 0:
                    color = COLORS["path"]
                else:
                    color = COLORS["wall"]

                self.canvas.create_rectangle(x1, y1, x2, y2,
                                             fill=color, outline="")

        # Draw S and E labels
        sr, sc = self.maze.start
        er, ec = self.maze.end
        self.canvas.create_text(sc*cs + cs//2, sr*cs + cs//2,
                                text="S", fill="white",
                                font=("Helvetica", 10, "bold"))
        self.canvas.create_text(ec*cs + cs//2, er*cs + cs//2,
                                text="E", fill="white",
                                font=("Helvetica", 10, "bold"))

    def reset_maze(self):
        if self.animation_id:
            self.root.after_cancel(self.animation_id)
            self.animation_id = None
        self.draw_maze()
        for key in self.stat_labels:
            self.stat_labels[key].config(text="—")

    def solve(self):
        if not self.maze:
            return
        if self.animation_id:
            self.root.after_cancel(self.animation_id)

        algo = self.algo_var.get()
        path, explored, elapsed = self.maze.solve(algo)

        if not path:
            messagebox.showinfo("No Solution", "The maze has no solution!")
            return

        # Update stats
        self.stat_labels["path_len"].config(text=str(len(path)))
        self.stat_labels["nodes"].config(text=str(len(explored)))
        self.stat_labels["time"].config(text=f"{elapsed*1000:.2f}")
        self.stat_labels["algo"].config(text=algo.upper())

        # Animate explored cells, then solution
        self.animate(explored, path)

    def animate(self, explored, solution):
        explored_so_far = []

        def step_explore(i):
            if i < len(explored):
                explored_so_far.append(explored[i])
                self.draw_maze(explored=explored_so_far)
                self.animation_id = self.root.after(18, lambda: step_explore(i + 1))
            else:
                step_solution(0)

        solution_so_far = []

        def step_solution(i):
            if i < len(solution):
                solution_so_far.append(solution[i])
                self.draw_maze(explored=explored, solution=solution_so_far)
                self.animation_id = self.root.after(30, lambda: step_solution(i + 1))

        step_explore(0)


if __name__ == "__main__":
    root = tk.Tk()
    app = MazeApp(root)
    root.mainloop()