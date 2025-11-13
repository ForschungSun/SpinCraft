import json
import tkinter as tk
from pathlib import Path

from wheel.model import WheelModel
from wheel.renderer import WheelRenderer
from wheel.animation import WheelAnimator


def load_default_entries():
    base_dir = Path(__file__).resolve().parent
    cfg_path = base_dir / "config" / "default_entries.json"
    if not cfg_path.exists():
        # fallback
        return [("A", 1), ("B", 1), ("C", 1), ("D", 1)]
    with cfg_path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    entries = []
    for item in data.get("entries", []):
        entries.append((item["label"], float(item["weight"])))
    return entries


def main():
    root = tk.Tk()
    root.title("SpinCraft - Weighted Wheel")
    root.configure(bg="#1f2430")

    canvas_size = 500
    radius = 200

    canvas = tk.Canvas(
        root,
        width=canvas_size,
        height=canvas_size,
        bg="#1f2430",
        highlightthickness=0,
    )
    canvas.grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 10))

    result_var = tk.StringVar(value="SpinCraft")
    result_label = tk.Label(
        root,
        textvariable=result_var,
        fg="#e5e9f0",
        bg="#1f2430",
        font=("Helvetica", 14, "bold"),
    )
    result_label.grid(row=1, column=0, columnspan=2, pady=(0, 10))

    entries = load_default_entries()
    model = WheelModel(entries)
    renderer = WheelRenderer(canvas, model, canvas_size // 2, canvas_size // 2, radius)

    def on_finish(result_label_text):
        result_var.set(f"结果：{result_label_text}")

    animator = WheelAnimator(root, model, renderer, on_finish=on_finish)
    renderer.draw(animator.current_angle)

    spin_button = tk.Button(
        root,
        text="开始",
        command=animator.start_spin,
        font=("Helvetica", 12, "bold"),
        fg="#1f2430",
        bg="#88c0d0",
        activebackground="#81a1c1",
        activeforeground="#1f2430",
        relief=tk.FLAT,
        padx=20,
        pady=6,
    )
    spin_button.grid(row=2, column=0, pady=(0, 20), padx=(40, 5), sticky="e")

    def quit_app():
        root.destroy()

    quit_button = tk.Button(
        root,
        text="退出",
        command=quit_app,
        font=("Helvetica", 12),
        fg="#d8dee9",
        bg="#3b4252",
        activebackground="#4c566a",
        activeforeground="#eceff4",
        relief=tk.FLAT,
        padx=20,
        pady=6,
    )
    quit_button.grid(row=2, column=1, pady=(0, 20), padx=(5, 40), sticky="w")

    root.mainloop()


if __name__ == "__main__":
    main()
