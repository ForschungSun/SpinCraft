import tkinter as tk
from tkinter import messagebox
import random


class DiceApp:
    def __init__(self, master):
        self.master = master
        master.title("骰子")

        tk.Label(master, text="最小值:").grid(row=0, column=0, padx=5, pady=5)
        self.min_entry = tk.Entry(master, width=8)
        self.min_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(master, text="最大值:").grid(row=0, column=2, padx=5, pady=5)
        self.max_entry = tk.Entry(master, width=8)
        self.max_entry.grid(row=0, column=3, padx=5, pady=5)

        self.roll_button = tk.Button(master, text="掷骰子", command=self.start_roll)
        self.roll_button.grid(row=1, column=0, columnspan=4, pady=10)

        self.result_label = tk.Label(
            master,
            text="?",
            font=("Helvetica", 40, "bold"),
            width=4
        )
        self.result_label.grid(row=2, column=0, columnspan=4, pady=10)

        self.animating = False
        self.animation_steps = 0
        self.max_steps = 15
        self.animation_delay = 80

        self.current_min = 1
        self.current_max = 6

    def start_roll(self):

        if self.animating:
            return


        try:
            min_val = int(self.min_entry.get())
            max_val = int(self.max_entry.get())
        except ValueError:
            messagebox.showerror("输入错误", "请输入整数区间，例如：2 和 18")
            return

        if min_val > max_val:
            messagebox.showerror("输入错误", "最小值不能大于最大值")
            return

        self.current_min = min_val
        self.current_max = max_val


        self.animating = True
        self.animation_steps = 0
        self.roll_button.config(state=tk.DISABLED)  # 防止多次点击
        self.animate_roll()

    def animate_roll(self):
        if self.animation_steps < self.max_steps:

            tmp_val = random.randint(self.current_min, self.current_max)
            self.result_label.config(text=str(tmp_val))

            self.animation_steps += 1

            self.master.after(self.animation_delay, self.animate_roll)
        else:

            final_val = random.randint(self.current_min, self.current_max)
            self.result_label.config(text=str(final_val))

            self.animating = False
            self.roll_button.config(state=tk.NORMAL)


if __name__ == "__main__":
    root = tk.Tk()
    app = DiceApp(root)
    root.mainloop()
