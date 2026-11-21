"""Happy Birthday Shivuuu - a small surprise app (Python + tkinter).
Run:  python shivuuu_birthday.py
No extra install needed, tkinter comes with Python.
"""
import random
import tkinter as tk

BG, ROSE, GOLD, INK, SOFT = "#2a0f2e", "#ff5c8a", "#ffd27a", "#fff4f0", "#f3c9dc"
W, H = 460, 680

MSGS = [
    "Today is all about you, and so am I. 💕",
    "We are miles apart, but you are still my first thought every morning and my last every night. 🌙",
    "There are billions of people in this world, but my world is just Shivuuu. 🌍",
    "I can’t wait for the day we meet in person and I finally get to hug you for real. 🤗💞",
    "You get prettier every year. Warning: the limit is being crossed! 😜",
    "Wishing you a day as sweet as you are. And don’t eat my share of the cake! 🍰",
]
HINTS = [
    "Go on, press No. I dare you. 😏",
    "Haha, nice try. 😏",
    "Catch me if you can! 🏃‍♂️",
    "Even the button knows the answer. 😂",
    "Only YES is left now. 🥺",
    "Stop trying and press YES! 😘",
]


class App:
    def __init__(self, root):
        self.root = root
        root.title("Happy Birthday Shivuuu 💖")
        root.geometry(f"{W}x{H}")
        root.configure(bg=BG)
        root.resizable(False, False)
        self.frame = None
        self.token = 0          # changes on every screen switch, stops old timers
        self.running = False
        root.bind("<Left>", lambda e: self.move_basket(self.bx - 40))
        root.bind("<Right>", lambda e: self.move_basket(self.bx + 40))
        self.intro()

    # ---------- helpers ----------
    def clear(self):
        self.token += 1
        self.running = False
        if self.frame:
            self.frame.destroy()
        self.frame = tk.Frame(self.root, bg=BG)
        self.frame.pack(fill="both", expand=True)
        return self.frame

    def label(self, parent, text, size=16, color=SOFT, bold=False, pady=10):
        lb = tk.Label(parent, text=text, font=("Arial", size, "bold" if bold else "normal"),
                      fg=color, bg=BG, wraplength=400, justify="center")
        lb.pack(pady=pady)
        return lb

    def button(self, parent, text, cmd, color=ROSE, fg="white"):
        b = tk.Button(parent, text=text, command=cmd, font=("Arial", 16, "bold"), bg=color,
                      fg=fg, activebackground=color, relief="flat", padx=24, pady=10, cursor="hand2")
        b.pack(pady=14)
        return b

    # ---------- 1. envelope ----------
    def intro(self):
        f = self.clear()
        tk.Frame(f, bg=BG, height=130).pack()
        self.label(f, "I made a little surprise just for you…", 16)
        env = self.label(f, "💌", 90, GOLD)
        env.config(cursor="hand2")
        env.bind("<Button-1>", lambda e: self.wishes())
        self.label(f, "Tap to open, Shivuuu", 22, GOLD, True)

    # ---------- 2. birthday messages ----------
    def wishes(self):
        f = self.clear()
        self.mi = 0
        tk.Frame(f, bg=BG, height=70).pack()
        self.label(f, "Happy Birthday,\nShivuuu! 🎂", 34, GOLD, True)
        self.msg = self.label(f, "", 18, INK, pady=30)
        self.msg.config(height=6)
        self.next_btn = self.button(f, "Next 💕", self.next_msg)
        self.type_msg()

    def type_msg(self):
        text, tok = MSGS[self.mi], self.token
        def step(i=0):
            if tok != self.token:
                return
            self.msg.config(text=text[:i])
            if i < len(text):
                self.root.after(35, step, i + 1)
        step()

    def next_msg(self):
        self.mi += 1
        if self.mi >= len(MSGS):
            self.game()
            return
        if self.mi == len(MSGS) - 1:
            self.next_btn.config(text="Play a game 🎮")
        self.type_msg()

    # ---------- 3. catch the cake game ----------
    def game(self):
        f = self.clear()
        self.c = tk.Canvas(f, width=W, height=H, bg=BG, highlightthickness=0)
        self.c.pack()
        self.items, self.score, self.left = [], 0, 20
        self.bx, self.by, self.spawn_t, self.running = W // 2, H - 70, 0, True
        self.hud = self.c.create_text(W // 2, 28, text="", fill=INK, font=("Arial", 18, "bold"))
        self.c.create_text(W // 2, 70, width=400, justify="center", fill=SOFT, font=("Arial", 13),
                           text="Move mouse (or ← →) to catch 🎂 +1 and ❤️ +2.\nDodge 🌶️, that’s my angry Shivuuu!")
        self.toast = self.c.create_text(W // 2, 200, text="", fill=ROSE, font=("Arial", 24, "bold"))
        self.basket = self.c.create_text(self.bx, self.by, text="🧺", font=("Arial", 44))
        self.c.bind("<Motion>", lambda e: self.move_basket(e.x))
        self.update_hud()
        self.loop(self.token)
        self.root.after(1000, self.countdown, self.token)

    def move_basket(self, x):
        if not self.running:
            return
        self.bx = max(30, min(W - 30, x))
        self.c.coords(self.basket, self.bx, self.by)

    def update_hud(self):
        self.c.itemconfig(self.hud, text=f"⏱ {self.left}     ⭐ {self.score}")

    def say(self, text):
        self.c.itemconfig(self.toast, text=text)
        self.root.after(700, lambda: self.running and self.c.itemconfig(self.toast, text=""))

    def spawn(self):
        r = random.random()
        kind = "🎂" if r < 0.55 else "❤️" if r < 0.8 else "🌶️"
        x = random.randint(30, W - 30)
        item = {"k": kind, "x": x, "y": 100, "v": random.uniform(4, 8)}
        item["id"] = self.c.create_text(x, 100, text=kind, font=("Arial", 30))
        self.items.append(item)

    def loop(self, tok):
        if tok != self.token or not self.running:
            return
        self.spawn_t += 1
        if self.spawn_t >= 18:
            self.spawn_t = 0
            self.spawn()
        for it in self.items[:]:
            it["y"] += it["v"]
            self.c.coords(it["id"], it["x"], it["y"])
            if abs(it["y"] - self.by) < 30 and abs(it["x"] - self.bx) < 50:
                if it["k"] == "🎂":
                    self.score += 1; self.say("Yummy! 😋")
                elif it["k"] == "❤️":
                    self.score += 2; self.say("Love caught! 💘")
                else:
                    self.score = max(0, self.score - 2); self.say("Ouch, so spicy! 🌶️😤")
                self.update_hud()
                self.c.delete(it["id"]); self.items.remove(it)
            elif it["y"] > H:
                self.c.delete(it["id"]); self.items.remove(it)
        self.root.after(30, self.loop, tok)

    def countdown(self, tok):
        if tok != self.token or not self.running:
            return
        self.left -= 1
        self.update_hud()
        if self.left <= 0:
            self.result()
        else:
            self.root.after(1000, self.countdown, tok)

    # ---------- 4. result ----------
    def result(self):
        s = self.score
        if s >= 22:
            title, text = "Cake Queen 👑", f"Score {s}! You ate my share of the cake too. I forgive you. 😂"
        elif s >= 10:
            title, text = "Sweet Shivuuu 🍰", f"Score {s}! Just like you: a little sweet, a little spicy. 😜"
        else:
            title, text = "Mirchi Girl 🌶️", f"Score {s}. No worries, you are still 100/100 to me. 💖"
        f = self.clear()
        tk.Frame(f, bg=BG, height=180).pack()
        self.label(f, title, 34, GOLD, True)
        self.label(f, text, 18, SOFT)
        self.button(f, "One last question 🙈", self.question)

    # ---------- 5. runaway "No" ----------
    def question(self):
        f = self.clear()
        self.tries, self.yes_size = 0, 18
        tk.Frame(f, bg=BG, height=110).pack()
        self.label(f, "Do you love me?", 38, GOLD, True)
        self.hint = self.label(f, HINTS[0], 15, SOFT)
        self.yes = tk.Button(f, text="YES 😍", font=("Arial", self.yes_size, "bold"), bg=GOLD,
                             fg="#4a1a4f", relief="flat", padx=20, pady=8, cursor="hand2",
                             command=self.final)
        self.yes.place(x=90, y=360)
        self.no = tk.Button(f, text="No 😤", font=("Arial", 16, "bold"), bg=ROSE, fg="white",
                            relief="flat", padx=20, pady=8)
        self.no.place(x=280, y=360)
        self.no.bind("<Enter>", self.dodge)
        self.no.bind("<Button-1>", self.dodge)

    def dodge(self, _event=None):
        self.tries += 1
        self.hint.config(text=HINTS[min(self.tries, len(HINTS) - 1)])
        self.no.place(x=random.randint(10, W - 110), y=random.randint(300, 600))
        self.yes_size = min(34, self.yes_size + 2)
        self.yes.config(font=("Arial", self.yes_size, "bold"))
        return "break"

    # ---------- 6. final ----------
    def final(self):
        f = self.clear()
        tk.Frame(f, bg=BG, height=100).pack()
        self.label(f, "I knew it! 🥰", 38, GOLD, True)
        self.label(f, "Shivuuu, you are my favourite person, my peace, and my reason to smile "
                      "even on the hardest days. Thank you for being mine, no matter how far apart we are.", 16)
        self.label(f, "Happy Birthday, my love 💖\nLove you always.", 24, GOLD, True, pady=20)
        self.button(f, "Play again 🎮", self.game, GOLD, "#4a1a4f")


if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
