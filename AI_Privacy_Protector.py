"""
AI PRIVACY PROTECTOR
A local, rule-based privacy scanner for educational demonstration.

How it works:
- Scans text entered by the user.
- Detects common sensitive-data patterns (email, phone, Aadhaar-like number,
  and password-like text).
- Calculates a simple risk score.
- Masks detected values in a protected copy.
- Does not send data over the internet or save scanned text to a file.

Note: This is an educational prototype, not a certified security product.
Pattern matches can produce false positives or miss unusual formats.
"""

import re
import tkinter as tk
from tkinter import ttk, messagebox

PATTERNS = [
    ("Email address", re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"), 25),
    ("Indian mobile number", re.compile(r"(?<!\d)(?:\+91[\s-]?)?[6-9]\d{9}(?!\d)"), 25),
    ("Aadhaar-like 12-digit number", re.compile(r"(?<!\d)\d{4}[\s-]?\d{4}[\s-]?\d{4}(?!\d)"), 35),
    ("Password-like text", re.compile(r"(?i)\b(?:password|passcode|pwd)\s*[:=]\s*[^\s,;]+"), 35),
]

def scan_text(text):
    """Return detections as (label, start, end, matched_value, risk_points)."""
    found = []
    occupied = []
    for label, pattern, points in PATTERNS:
        for match in pattern.finditer(text):
            # Avoid double-counting overlapping matches.
            if any(match.start() < end and match.end() > start for start, end in occupied):
                continue
            found.append((label, match.start(), match.end(), match.group(), points))
            occupied.append((match.start(), match.end()))
    found.sort(key=lambda item: item[1])
    return found

def mask_text(text, detections):
    """Mask detected values while preserving surrounding text."""
    result = text
    for label, start, end, value, points in reversed(detections):
        replacement = "[REDACTED: " + label.upper() + "]"
        result = result[:start] + replacement + result[end:]
    return result

class PrivacyProtector:
    def __init__(self, root):
        self.root = root
        root.title("AI Privacy Protector")
        root.geometry("850x680")
        root.minsize(700, 560)

        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("Title.TLabel", font=("Arial", 20, "bold"), foreground="#153e75")
        style.configure("Sub.TLabel", font=("Arial", 10), foreground="#475569")
        style.configure("Action.TButton", font=("Arial", 10, "bold"), padding=7)

        main = ttk.Frame(root, padding=18)
        main.pack(fill="both", expand=True)

        ttk.Label(main, text="AI PRIVACY PROTECTOR", style="Title.TLabel").pack(anchor="w")
        ttk.Label(main, text="A local demonstration tool for identifying and masking sensitive information.",
                  style="Sub.TLabel").pack(anchor="w", pady=(2, 12))

        ttk.Label(main, text="Enter or paste sample text:").pack(anchor="w")
        self.input_box = tk.Text(main, height=10, wrap="word", font=("Arial", 11),
                                 relief="solid", borderwidth=1)
        self.input_box.pack(fill="both", expand=True, pady=(5, 10))
        self.input_box.insert("1.0",
            "Example: Contact me at student@example.com or 9876543210. "
            "Password: demoPass123. This is sample text only.")

        buttons = ttk.Frame(main)
        buttons.pack(fill="x", pady=3)
        ttk.Button(buttons, text="Scan for Privacy Risks", style="Action.TButton",
                   command=self.scan).pack(side="left", padx=(0, 8))
        ttk.Button(buttons, text="Clear", command=self.clear).pack(side="left")
        ttk.Button(buttons, text="Load Example", command=self.load_example).pack(side="left", padx=8)

        ttk.Label(main, text="Scan report:").pack(anchor="w", pady=(12, 4))
        self.report = tk.Text(main, height=8, wrap="word", font=("Arial", 10),
                              state="disabled", relief="solid", borderwidth=1)
        self.report.pack(fill="both", expand=True)

        ttk.Label(main, text="Masked / protected text:").pack(anchor="w", pady=(12, 4))
        self.output = tk.Text(main, height=6, wrap="word", font=("Arial", 10),
                              state="disabled", relief="solid", borderwidth=1)
        self.output.pack(fill="both", expand=True)

        ttk.Label(main,
            text="Privacy note: Text is analysed locally in this app. Do not enter real passwords or confidential data.",
            style="Sub.TLabel", wraplength=790).pack(anchor="w", pady=(10, 0))

    def set_text(self, widget, value):
        widget.configure(state="normal")
        widget.delete("1.0", "end")
        widget.insert("1.0", value)
        widget.configure(state="disabled")

    def scan(self):
        text = self.input_box.get("1.0", "end-1c")
        detections = scan_text(text)
        # Educational score: add points for each category, capped at 100.
        score = min(100, sum(item[4] for item in detections))
        if not detections:
            level = "LOW"
            summary = "No supported sensitive-data patterns were detected."
        elif score < 40:
            level = "MODERATE"
            summary = "Some potentially sensitive information was detected."
        else:
            level = "HIGH"
            summary = "Sensitive information may be exposed. Review and mask it."

        lines = [
            "PRIVACY SCAN REPORT",
            "-------------------",
            f"Risk score: {score}/100",
            f"Risk level: {level}",
            f"Findings: {len(detections)}",
            "",
            summary,
            "",
        ]
        if detections:
            for index, item in enumerate(detections, 1):
                label, start, end, value, points = item
                preview = value if len(value) <= 5 else value[:2] + "*" * min(8, len(value)-4) + value[-2:]
                lines.append(f"{index}. {label} detected (example: {preview})")
        else:
            lines.append("No matches found. Remember: this tool cannot guarantee that text is safe.")
        self.set_text(self.report, "\n".join(lines))
        self.set_text(self.output, mask_text(text, detections))

    def clear(self):
        self.input_box.delete("1.0", "end")
        self.set_text(self.report, "")
        self.set_text(self.output, "")

    def load_example(self):
        self.input_box.delete("1.0", "end")
        self.input_box.insert("1.0",
            "My email is learner@example.com. My contact number is 9876543210. "
            "Password: sampleOnly123. Aadhaar-like sample: 1234 5678 9012.")

if __name__ == "__main__":
    root = tk.Tk()
    app = PrivacyProtector(root)
    root.mainloop()
