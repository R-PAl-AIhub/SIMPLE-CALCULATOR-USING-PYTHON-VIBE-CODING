import tkinter as tk
from tkinter import ttk


class CalculatorApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Vibe Calculator")
        self.root.geometry("420x640")
        self.root.minsize(360, 560)
        self.root.configure(bg="#121212")

        self.expression = ""
        self.current_text = tk.StringVar(value="0")
        self.history_text = tk.StringVar(value="")

        self._build_ui()
        self._bind_keys()

    def _build_ui(self) -> None:
        style = ttk.Style()
        style.theme_use("clam")

        container = tk.Frame(self.root, bg="#121212", padx=18, pady=18)
        container.pack(fill="both", expand=True)

        title = tk.Label(
            container,
            text="Vibe Calculator",
            bg="#121212",
            fg="#f4f4f5",
            font=("Segoe UI", 18, "bold"),
            anchor="w",
        )
        title.pack(fill="x", pady=(0, 14))

        display_card = tk.Frame(container, bg="#1d1d1f", bd=0, highlightthickness=0)
        display_card.pack(fill="x", pady=(0, 18), ipady=14)

        history_label = tk.Label(
            display_card,
            textvariable=self.history_text,
            bg="#1d1d1f",
            fg="#8e8e93",
            anchor="e",
            padx=14,
            font=("Consolas", 12),
        )
        history_label.pack(fill="x")

        display_label = tk.Label(
            display_card,
            textvariable=self.current_text,
            bg="#1d1d1f",
            fg="#ffffff",
            anchor="e",
            padx=14,
            pady=8,
            font=("Consolas", 32, "bold"),
        )
        display_label.pack(fill="x")

        buttons_frame = tk.Frame(container, bg="#121212")
        buttons_frame.pack(fill="both", expand=True)

        for i in range(5):
            buttons_frame.rowconfigure(i, weight=1, uniform="row")
        for j in range(4):
            buttons_frame.columnconfigure(j, weight=1, uniform="col")

        layout = [
            [("C", "action"), ("⌫", "action"), ("%", "operator"), ("÷", "operator")],
            [("7", "number"), ("8", "number"), ("9", "number"), ("×", "operator")],
            [("4", "number"), ("5", "number"), ("6", "number"), ("-", "operator")],
            [("1", "number"), ("2", "number"), ("3", "number"), ("+", "operator")],
            [("±", "action"), ("0", "number"), (".", "number"), ("=", "equals")],
        ]

        for r, row in enumerate(layout):
            for c, (label, kind) in enumerate(row):
                button = self._create_button(buttons_frame, label, kind)
                button.grid(row=r, column=c, padx=6, pady=6, sticky="nsew")

    def _create_button(self, parent: tk.Frame, label: str, kind: str) -> tk.Button:
        colors = {
            "number": ("#2a2a2d", "#f5f5f7", "#353539"),
            "operator": ("#ff9f0a", "#1a1a1a", "#ffb340"),
            "action": ("#3a3a3c", "#f5f5f7", "#4a4a4e"),
            "equals": ("#4f46e5", "#ffffff", "#6366f1"),
        }
        bg, fg, active_bg = colors[kind]

        command = lambda value=label: self._on_button_press(value)
        button = tk.Button(
            parent,
            text=label,
            command=command,
            bg=bg,
            fg=fg,
            activebackground=active_bg,
            activeforeground=fg,
            relief="flat",
            bd=0,
            highlightthickness=0,
            font=("Segoe UI", 18, "bold"),
            cursor="hand2",
        )

        button.bind("<Enter>", lambda _e, b=button, h=active_bg: b.config(bg=h))
        button.bind("<Leave>", lambda _e, b=button, n=bg: b.config(bg=n))
        return button

    def _bind_keys(self) -> None:
        self.root.bind("<Key>", self._handle_keypress)
        self.root.bind("<Return>", lambda _e: self._on_button_press("="))
        self.root.bind("<BackSpace>", lambda _e: self._on_button_press("⌫"))
        self.root.bind("<Escape>", lambda _e: self._on_button_press("C"))

    def _handle_keypress(self, event: tk.Event) -> None:
        char = event.char
        if char in "0123456789.+-*/%":
            if char == "*":
                self._on_button_press("×")
            elif char == "/":
                self._on_button_press("÷")
            else:
                self._on_button_press(char)

    def _on_button_press(self, value: str) -> None:
        if value == "C":
            self.expression = ""
            self.history_text.set("")
            self.current_text.set("0")
            return

        if value == "⌫":
            self.expression = self.expression[:-1]
            self.current_text.set(self.expression or "0")
            return

        if value == "±":
            self._toggle_sign()
            return

        if value == "=":
            self._evaluate_expression()
            return

        translated = "*" if value == "×" else "/" if value == "÷" else value
        self.expression += translated
        self.current_text.set(self.expression)

    def _toggle_sign(self) -> None:
        if not self.expression:
            self.expression = "-"
            self.current_text.set(self.expression)
            return

        token_start = max(
            self.expression.rfind("+"),
            self.expression.rfind("-"),
            self.expression.rfind("*"),
            self.expression.rfind("/"),
            self.expression.rfind("%"),
        )

        if token_start == -1:
            self.expression = self.expression[1:] if self.expression.startswith("-") else f"-{self.expression}"
        else:
            number = self.expression[token_start + 1 :]
            if number.startswith("-"):
                number = number[1:]
            else:
                number = f"-{number}"
            self.expression = f"{self.expression[:token_start + 1]}{number}"

        self.current_text.set(self.expression or "0")

    def _evaluate_expression(self) -> None:
        if not self.expression:
            return

        expression = self.expression
        try:
            result = eval(expression, {"__builtins__": {}}, {})
            result_text = str(result)
            self.history_text.set(f"{expression} =")
            self.expression = result_text
            self.current_text.set(result_text)
        except Exception:
            self.history_text.set(f"{expression} =")
            self.current_text.set("Error")
            self.expression = ""


def main() -> None:
    root = tk.Tk()
    CalculatorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
