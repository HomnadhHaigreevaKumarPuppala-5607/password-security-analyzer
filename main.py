
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from zxcvbn import zxcvbn
import random
import string

# ---------------- HISTORY ---------------- #

history = []

show_password = False

# ---------------- PASSWORD CHECK ---------------- #

def check_password():

    password = entry.get()

    if password == "":
        messagebox.showwarning(
            "Warning",
            "Please Enter Password"
        )
        return

    history.append(password)

    result = zxcvbn(password)

    score = result['score']

    crack_time = result['crack_times_display'][
        'offline_fast_hashing_1e10_per_second'
    ]

    suggestions = result['feedback']['suggestions']

    feedback_text = ""

    for item in suggestions:
        feedback_text += "• " + item + "\n"

    if score == 0:
        strength = "Very Weak"
        color = "#ff1744"
        progress['value'] = 20

    elif score == 1:
        strength = "Weak"
        color = "#ff9100"
        progress['value'] = 40

    elif score == 2:
        strength = "Medium"
        color = "#ffd600"
        progress['value'] = 60

    elif score == 3:
        strength = "Strong"
        color = "#00e676"
        progress['value'] = 80

    else:
        strength = "Very Strong"
        color = "#00e5ff"
        progress['value'] = 100

    strength_label.config(
        text=f"Strength: {strength}",
        fg=color
    )

    result_label.config(
        text=f"Estimated Crack Time:\n{crack_time}\n\nSuggestions:\n{feedback_text}"
    )

# ---------------- GENERATE PASSWORD ---------------- #

def generate_password():

    characters = (
        string.ascii_letters +
        string.digits +
        string.punctuation
    )

    password = "".join(
        random.choice(characters)
        for i in range(16)
    )

    entry.delete(0, END)

    entry.insert(0, password)

# ---------------- SHOW/HIDE PASSWORD ---------------- #

def toggle_password():

    global show_password

    if show_password:
        entry.config(show="*")
        eye_btn.config(text="👁")
        show_password = False

    else:
        entry.config(show="")
        eye_btn.config(text="🔒")
        show_password = True

# ---------------- WORDLIST GENERATOR ---------------- #

def generate_wordlist():

    name = name_entry.get()
    pet = pet_entry.get()
    year = year_entry.get()

    if name == "" or pet == "" or year == "":
        messagebox.showwarning(
            "Warning",
            "Please Fill All Fields"
        )
        return

    words = [
        name,
        pet,
        year,
        name + "123",
        pet + "123",
        name + year,
        pet + year,
        name + "@123",
        pet + "@123",
        name.capitalize() + "123",
        pet.capitalize() + "123"
    ]

    with open("wordlists/wordlist.txt", "w") as file:

        for word in words:
            file.write(word + "\n")

    messagebox.showinfo(
        "Success",
        "Wordlist Generated Successfully"
    )

# ---------------- EXPORT REPORT ---------------- #

def export_report():

    report = result_label.cget("text")

    if report == "":
        messagebox.showwarning(
            "Warning",
            "Analyze Password First"
        )
        return

    with open("exports/password_report.txt", "w") as file:
        file.write(report)

    messagebox.showinfo(
        "Exported",
        "Report Saved Successfully"
    )

# ---------------- HISTORY ---------------- #

def show_history():

    if len(history) == 0:
        messagebox.showinfo(
            "History",
            "No Passwords Checked Yet"
        )
        return

    history_text = "\n".join(history)

    messagebox.showinfo(
        "Password History",
        history_text
    )

# ---------------- HOVER EFFECTS ---------------- #

def on_enter(e):
    e.widget['background'] = '#d4af37'
    e.widget['fg'] = 'black'

def on_leave(e):
    e.widget['background'] = '#111111'
    e.widget['fg'] = '#d4af37'

# ---------------- MAIN WINDOW ---------------- #

root = Tk()

root.title("CyberShield Password Analyzer")

root.geometry("850x850")

root.config(bg="#0a0a0a")

# ---------------- STYLE ---------------- #

style = ttk.Style()

style.theme_use('clam')

style.configure(
    "TProgressbar",
    thickness=25,
    troughcolor="#1a1a1a",
    background="#d4af37",
    bordercolor="#1a1a1a",
    lightcolor="#f5d76e",
    darkcolor="#b8860b"
)
# ---------------- TITLE ---------------- #

title = Label(
    root,
    text="CYBERSHIELD PASSWORD ANALYZER",
    font=("Arial", 28, "bold"),
    bg="#0a0a0a",
    fg="#d4af37",
    padx=20,
    pady=10
)

title.pack(pady=25)

# ---------------- SUBTITLE ---------------- #

subtitle = Label(
    root,
    text="Advanced Cybersecurity Password Analysis System",
    font=("Arial", 12),
    bg="#0f172a",
    fg="#c5a862"
)

subtitle.pack()

# ---------------- PASSWORD FRAME ---------------- #

password_frame = Frame(
    root,
    bg="#0f172a"
)

password_frame.pack(pady=25)

# ---------------- PASSWORD ENTRY ---------------- #

entry = Entry(
    password_frame,
    width=32,
    show="*",
    font=("TimesNewRoman", 18),
    bg="#111111",
    fg="#f5d76e",
    insertbackground="#d4af37",
    relief=FLAT,
    bd=10
)

entry.grid(row=0, column=0)

# ---------------- EYE BUTTON ---------------- #

eye_btn = Button(
    password_frame,
    text="👁",
    command=toggle_password,
    font=("TimesNewRoman", 14),
    bg="#111111",
    fg="#d4af37",
    activebackground="#d4af37",
    activeforeground="black",
    relief=FLAT,
    width=3
)

eye_btn.grid(row=0, column=1)

# ---------------- BUTTON STYLE ---------------- #

btn_style = {
    "font": ("TimesNewRoman", 12, "bold"),
    "bg": "#111111",
    "fg": "#d4af37",
    "activebackground": "#d4af37",
    "activeforeground": "black",
    "relief": FLAT,
    "bd": 0,
    "width": 28,
    "height": 2,
    "cursor": "hand2"
}

# ---------------- ANALYZE BUTTON ---------------- #

check_btn = Button(
    root,
    text="Analyze Password",
    command=check_password,
    **btn_style
)

check_btn.pack(pady=10)

# ---------------- GENERATE BUTTON ---------------- #

generate_btn = Button(
    root,
    text="Generate Strong Password",
    command=generate_password,
    **btn_style
)

generate_btn.pack(pady=10)

# ---------------- HOVER EFFECTS ---------------- #

buttons = [check_btn, generate_btn]

# ---------------- PROGRESS BAR ---------------- #

progress = ttk.Progressbar(
    root,
    orient=HORIZONTAL,
    length=500,
    mode='determinate'
)

progress.pack(pady=25)

# ---------------- STRENGTH LABEL ---------------- #

strength_label = Label(
    root,
    text="",
    font=("Arial", 18, "bold"),
    bg="#0f172a"
)

strength_label.pack(pady=10)

# ---------------- RESULT LABEL ---------------- #

result_label = Label(
    root,
    text="",
    font=("Arial", 12),
    justify=LEFT,
    wraplength=650,
    bg="#111111",
    fg="#f8e7a1",
    padx=20,
    pady=20
)

result_label.pack(pady=20)

# ---------------- WORDLIST TITLE ---------------- #

wordlist_title = Label(
    root,
    text="Custom Wordlist Generator",
    font=("Arial", 18, "bold"),
    bg="#0f172a",
    fg="#d4af37"
)

wordlist_title.pack(pady=20)

# ---------------- INPUT STYLE ---------------- #

input_style = {
    "font": ("Arial", 13),
    "bg": "#111111",
    "fg": "#f5d76e",
    "insertbackground": "#d4af37",
    "relief": FLAT,
    "width": 30
}

# ---------------- NAME ---------------- #

Label(
    root,
    text="Name",
    bg="#0f172a",
    fg="white",
    font=("Arial", 12)
).pack()

name_entry = Entry(root, **input_style)

name_entry.pack(pady=5)

# ---------------- PET ---------------- #

Label(
    root,
    text="Pet Name",
    bg="#0f172a",
    fg="white",
    font=("Arial", 12)
).pack()

pet_entry = Entry(root, **input_style)

pet_entry.pack(pady=5)

# ---------------- YEAR ---------------- #

Label(
    root,
    text="Birth Year",
    bg="#0f172a",
    fg="white",
    font=("Arial", 12)
).pack()

year_entry = Entry(root, **input_style)

year_entry.pack(pady=5)

# ---------------- WORDLIST BUTTON ---------------- #

wordlist_btn = Button(
    root,
    text="Generate Wordlist",
    command=generate_wordlist,
    **btn_style
)

wordlist_btn.pack(pady=15)

# ---------------- EXPORT BUTTON ---------------- #

export_btn = Button(
    root,
    text="Export Report",
    command=export_report,
    **btn_style
)

export_btn.pack(pady=10)

# ---------------- HISTORY BUTTON ---------------- #

history_btn = Button(
    root,
    text="Show Password History",
    command=show_history,
    **btn_style
)

history_btn.pack(pady=10)

# ---------------- HOVER BINDINGS ---------------- #

buttons.extend([
    wordlist_btn,
    export_btn,
    history_btn
])

for btn in buttons:
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)

# ---------------- FOOTER ---------------- #

footer = Label(
    root,
    text="Cybersecurity Internship Project • Premium Edition",
    font=("Arial", 10),
    bg="#0f172a",
    fg="#8b7355"
)

footer.pack(side=BOTTOM, pady=20)

# ---------------- RUN ---------------- #

root.mainloop()