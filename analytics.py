import os

# ── Matplotlib import 
try:
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    print("  [Warning] matplotlib not installed. Charts will be skipped.")
    print("  Run: pip install matplotlib\n")


# ── File paths (mirror file_handler.py) ────────────────────────────────────
USERS_FILE   = "users.txt"
GRADES_FILE  = "grades.txt"
ECA_FILE     = "eca.txt"

SUBJECTS = ["Math", "Science", "English", "CS", "Stats"]

#  DATA LOADERS
#  These read the .txt files directly so analytics.py stays independent.

def _load_users():
    """Returns list of dicts: {id, name, role, username}"""
    users = []
    try:
        with open(USERS_FILE, "r") as f:
            lines = f.readlines()
        for line in lines[1:]:           # skip header
            parts = line.strip().split(",")
            if len(parts) == 4:
                users.append({
                    "id":       parts[0].strip(),
                    "name":     parts[1].strip(),
                    "role":     parts[2].strip(),
                    "username": parts[3].strip()
                })
    except FileNotFoundError:
        print("  Error: users.txt not found.")
    return users


def _load_grades():
    """Returns list of dicts: {id, math, science, english, cs, stats}
       All mark values are floats."""
    grades = []
    try:
        with open(GRADES_FILE, "r") as f:
            lines = f.readlines()
        for line in lines[1:]:           # skip header
            parts = line.strip().split(",")
            if len(parts) == 6:
                try:
                    grades.append({
                        "id":      parts[0].strip(),
                        "math":    float(parts[1]),
                        "science": float(parts[2]),
                        "english": float(parts[3]),
                        "cs":      float(parts[4]),
                        "stats":   float(parts[5])
                    })
                except ValueError:
                    pass   # skip malformed rows
    except FileNotFoundError:
        print("  Error: grades.txt not found.")
    return grades


def _load_eca():
    """Returns dict: {student_id: [activity, ...]}"""
    eca_map = {}
    try:
        with open(ECA_FILE, "r") as f:
            lines = f.readlines()
        for line in lines[1:]:           # skip header
            parts = line.strip().split(",")
            if len(parts) == 2:
                sid      = parts[0].strip()
                activity = parts[1].strip()
                eca_map.setdefault(sid, []).append(activity)
    except FileNotFoundError:
        print("  Error: eca.txt not found.")
    return eca_map


def _get_student_name(student_id, users):
    """Return student's name given their ID, or the ID itself as fallback."""
    for u in users:
        if u["id"] == student_id:
            return u["name"]
    return student_id


def _average(values):
    """Safe average of a list of numbers."""
    return round(sum(values) / len(values), 2) if values else 0.0



#  DIVIDER HELPERS  


W = 75

def _rule(char="═"):
    print(char * W)

def _header(title):
    inner = W - 4
    print("╔" + "═" * (W - 2) + "╗")
    print("║  " + title.center(inner) + "  ║")
    print("╚" + "═" * (W - 2) + "╝")

def _divider():
    print("─" * W)


#  FEATURE 1 — Average Grades Per Subject


def show_average_grades():
    """Print and optionally chart the class average for every subject."""
    _header("AVERAGE GRADES PER SUBJECT")

    grades = _load_grades()
    if not grades:
        print("\n  No grade records found.")
        return

    averages = {
        "Math":    _average([g["math"]    for g in grades]),
        "Science": _average([g["science"] for g in grades]),
        "English": _average([g["english"] for g in grades]),
        "CS":      _average([g["cs"]      for g in grades]),
        "Stats":   _average([g["stats"]   for g in grades]),
    }

    print(f"\n  {'Subject':<15} {'Average':>10}")
    _divider()
    for subject, avg in averages.items():
        bar = "█" * int(avg // 5)          # simple ASCII bar (scale: 5 marks per block)
        print(f"  {subject:<15} {avg:>6.2f}  {bar}")
    _divider()
    print(f"  {'Overall Average':<15} {_average(list(averages.values())):>6.2f}")

    # ── Chart ──────────────────────────────────────────────────────────────
    if MATPLOTLIB_AVAILABLE:
        fig, ax = plt.subplots(figsize=(8, 4))
        subjects = list(averages.keys())
        values   = list(averages.values())
        bars = ax.bar(subjects, values, color=["#4C72B0","#DD8452","#55A868","#C44E52","#8172B2"])
        ax.set_ylim(0, 100)
        ax.set_ylabel("Average Mark")
        ax.set_title("Class Average Grades Per Subject")
        for bar, val in zip(bars, values):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1,
                    f"{val:.1f}", ha="center", va="bottom", fontsize=9)
        ax.axhline(y=50, color="red", linestyle="--", linewidth=0.8, label="Pass line (50)")
        ax.legend()
        plt.tight_layout()
        plt.show()


#  FEATURE 2 — Grade Trends Per Student

def show_grade_trends():
    """Bar chart showing each subject mark for every student."""
    _header("GRADE TRENDS PER STUDENT")

    grades = _load_grades()
    users  = _load_users()

    if not grades:
        print("\n  No grade records found.")
        return

    # ── Text table ─────────────────────────────────────────────────────────
    col_w = 10
    header_row = f"  {'Name':<18}" + "".join(f"{s:>{col_w}}" for s in SUBJECTS) + f"{'Average':>{col_w}}"
    print()
    print(header_row)
    _divider()

    all_averages = []
    for g in grades:
        name    = _get_student_name(g["id"], users)
        marks   = [g["math"], g["science"], g["english"], g["cs"], g["stats"]]
        avg     = _average(marks)
        all_averages.append((name, marks, avg))
        row = f"  {name:<18}" + "".join(f"{m:>{col_w}.1f}" for m in marks) + f"{avg:>{col_w}.2f}"
        print(row)

    _divider()

    # ── Chart ──────────────────────────────────────────────────────────────
    if MATPLOTLIB_AVAILABLE and all_averages:
        n_students = len(all_averages)
        n_subjects = len(SUBJECTS)
        import numpy as np
        x      = np.arange(n_subjects)
        width  = 0.8 / max(n_students, 1)
        colors = plt.cm.tab10.colors

        fig, ax = plt.subplots(figsize=(10, 5))
        for i, (name, marks, _) in enumerate(all_averages):
            offset = (i - n_students / 2) * width + width / 2
            ax.bar(x + offset, marks, width, label=name, color=colors[i % len(colors)])

        ax.set_xticks(x)
        ax.set_xticklabels(SUBJECTS)
        ax.set_ylim(0, 100)
        ax.set_ylabel("Mark")
        ax.set_title("Grade Trends Per Student")
        ax.axhline(y=50, color="red", linestyle="--", linewidth=0.8, label="Pass (50)")
        ax.legend(loc="lower right")
        plt.tight_layout()
        plt.show()



#  FEATURE 3 — ECA Impact on Academic Performance


def show_eca_impact():
    """Compare average grades of students WITH vs WITHOUT ECA involvement."""
    _header("ECA IMPACT ON ACADEMIC PERFORMANCE")

    grades  = _load_grades()
    eca_map = _load_eca()
    users   = _load_users()

    if not grades:
        print("\n  No grade records found.")
        return

    with_eca    = []
    without_eca = []

    print(f"\n  {'Name':<18} {'ECA':<20} {'Avg Grade':>10}")
    _divider()

    for g in grades:
        marks    = [g["math"], g["science"], g["english"], g["cs"], g["stats"]]
        avg      = _average(marks)
        name     = _get_student_name(g["id"], users)
        eca_list = eca_map.get(g["id"], [])

        if eca_list:
            eca_str = ", ".join(eca_list)
            with_eca.append(avg)
        else:
            eca_str = "None"
            without_eca.append(avg)

        print(f"  {name:<18} {eca_str:<20} {avg:>10.2f}")

    _divider()

    avg_with    = _average(with_eca)
    avg_without = _average(without_eca)

    print(f"\n  Students WITH ECA    →  Avg: {avg_with:.2f}  (n={len(with_eca)})")
    print(f"  Students WITHOUT ECA →  Avg: {avg_without:.2f}  (n={len(without_eca)})")

    if with_eca and without_eca:
        diff = avg_with - avg_without
        direction = "higher" if diff >= 0 else "lower"
        print(f"\n  Students with ECA score {abs(diff):.2f} marks {direction} on average.")

    # ── Chart ──────────────────────────────────────────────────────────────
    if MATPLOTLIB_AVAILABLE:
        labels = []
        values = []
        if with_eca:
            labels.append("With ECA")
            values.append(avg_with)
        if without_eca:
            labels.append("Without ECA")
            values.append(avg_without)

        if labels:
            fig, ax = plt.subplots(figsize=(5, 4))
            bars = ax.bar(labels, values, color=["#2ca02c", "#d62728"], width=0.4)
            ax.set_ylim(0, 100)
            ax.set_ylabel("Average Grade")
            ax.set_title("ECA Impact on Academic Performance")
            for bar, val in zip(bars, values):
                ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1,
                        f"{val:.2f}", ha="center", fontsize=10)
            ax.axhline(y=50, color="red", linestyle="--", linewidth=0.8, label="Pass (50)")
            ax.legend()
            plt.tight_layout()
            plt.show()



#  FEATURE 4 — Performance Alerts


def show_performance_alerts(threshold=50):
    """Flag students who are below the threshold in any subject."""
    _header("PERFORMANCE ALERTS")

    grades = _load_grades()
    users  = _load_users()

    if not grades:
        print("\n  No grade records found.")
        return

    print(f"\n  Threshold: {threshold} marks per subject")
    print(f"  Students scoring below this threshold are flagged.\n")

    alert_found = False

    for g in grades:
        name   = _get_student_name(g["id"], users)
        marks  = {
            "Math":    g["math"],
            "Science": g["science"],
            "English": g["english"],
            "CS":      g["cs"],
            "Stats":   g["stats"]
        }
        failing = {subj: mark for subj, mark in marks.items() if mark < threshold}

        if failing:
            alert_found = True
            avg = _average(list(marks.values()))
            print(f"  ⚠  {name}  (ID: {g['id']})  —  Overall Avg: {avg:.2f}")
            for subj, mark in failing.items():
                gap = threshold - mark
                print(f"       ✗  {subj:<10}  Mark: {mark:.1f}  (needs +{gap:.1f} to pass)")
            print(f"     Suggestion: arrange extra tutoring in {', '.join(failing.keys())}.")
            _divider()

    if not alert_found:
        print("  ✓  No students are currently below the threshold. Great work!")



#  ANALYTICS MENU  (called from main.py / admin menu)


def analytics_menu():
    """Interactive menu for the analytics dashboard."""

    W = 75

    def box_top():  print("╔" + "═" * (W - 2) + "╗")
    def box_mid():  print("╠" + "═" * (W - 2) + "╣")
    def box_bot():  print("╚" + "═" * (W - 2) + "╝")
    def box_row(t): print("║  " + t.ljust(W - 4) + "  ║")

    while True:
        print()
        box_top()
        box_row("")
        box_row("A N A L Y T I C S   D A S H B O A R D".center(W - 4))
        box_row("")
        box_mid()
        box_row("  1.  Average Grades Per Subject")
        box_row("  2.  Grade Trends Per Student")
        box_row("  3.  ECA Impact on Academic Performance")
        box_row("  4.  Performance Alerts  (below-threshold students)")
        box_row("  0.  Back")
        box_row("")
        box_bot()

        while True:
            try:
                choice = int(input("\n  Enter your choice  >>  "))
                if 0 <= choice <= 4:
                    break
                print("  Please enter a number between 0 and 4.")
            except ValueError:
                print("  Invalid input. Please enter a number.")

        print()

        if choice == 1:
            show_average_grades()
        elif choice == 2:
            show_grade_trends()
        elif choice == 3:
            show_eca_impact()
        elif choice == 4:
            # Let admin pick threshold
            while True:
                try:
                    t = int(input("  Enter failing threshold (default 50)  >>  ") or "50")
                    if 0 <= t <= 100:
                        break
                    print("  Please enter a number between 0 and 100.")
                except ValueError:
                    print("  Invalid input.")
            show_performance_alerts(threshold=t)
        elif choice == 0:
            break

        input("\n  Press Enter to continue...")
