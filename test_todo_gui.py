import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import sys

# ---------------- Sound Support ----------------
try:
    if sys.platform == "win32":
        import winsound
        def play_sound():
            winsound.MessageBeep()
    else:
        def play_sound():
            pass
except:
    def play_sound():
        pass

# ---------------- Constants ----------------
FILE_NAME = "tasks.txt"
PENDING = "[ ]"
DONE = "[x]"

# ---------------- File Handling ----------------
def load_tasks():
    tasks = []
    try:
        with open(FILE_NAME, "r") as file:
            for line in file:
                line = line.strip()
                if line:
                    tasks.append(line)
    except FileNotFoundError:
        pass
    return tasks

def save_tasks(tasks):
    with open(FILE_NAME, "w") as file:
        for task in tasks:
            file.write(task + "\n")

# ---------------- GUI App ----------------
class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List App")
        self.root.geometry("620x760")
        self.root.resizable(False, False)
        self.root.configure(bg="black")  # Removed border highlight

        self.tasks = load_tasks()
        self.filtered_tasks = []
        self.is_searching = False

        # ---------------- Title ----------------
        title = tk.Label(
            root,
            text="MY TO DO LIST",
            font=("Comic Sans MS", 24, "bold"),
            bg="black",
            fg="white"
        )
        title.pack(pady=10)

        # ---------------- Counter ----------------
        self.counter_label = tk.Label(root, text="", font=("Arial", 11, "bold"), bg="black", fg="#ffb6c1")
        self.counter_label.pack()

        # ---------------- Entry ----------------
        self.task_entry = tk.Entry(root, width=40, font=("Arial", 13), bd=2, relief="groove")
        self.task_entry.pack(pady=8)
        self.task_entry.focus()

        # ---------------- Buttons ----------------
        btn_frame = tk.Frame(root, bg="black")
        btn_frame.pack(pady=8)

        self.create_button(btn_frame, "➕ Add", self.add_task, 0, "#001f3f")
        self.create_button(btn_frame, "✏ Edit", self.edit_task, 1, "#87ceeb")
        self.create_button(btn_frame, "✔ Toggle", self.toggle_done, 2, "#f1c40f")
        self.create_button(btn_frame, "🗑 Delete", self.delete_task, 3, "#8b0000")

        # ---------------- Search ----------------
        search_frame = tk.Frame(root, bg="black")
        search_frame.pack(pady=10)

        self.search_entry = tk.Entry(search_frame, width=25, font=("Arial", 11), bd=2, bg="#dcdcdc", fg="black")
        self.search_entry.grid(row=0, column=0, padx=5)

        self.create_button(search_frame, "🔍 Search", self.search_tasks, 1, "#000000")
        self.create_button(search_frame, "💗 Clear", self.clear_search, 2, "#7f8c8d")

        # ---------------- Listbox ----------------
        list_frame = tk.Frame(root, bg="black")
        list_frame.pack(pady=10)

        self.task_listbox = tk.Listbox(list_frame, width=55, height=18, font=("Arial", 11), bd=2, relief="sunken",
                                       selectbackground="#ff69b4", activestyle="none")
        self.task_listbox.pack(side=tk.LEFT)

        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.task_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.task_listbox.yview)

        # ---------------- Progress Bar ----------------
        style = ttk.Style()
        style.theme_use("default")
        style.configure("pink.Horizontal.TProgressbar", troughcolor="#2c2c2c", background="#ff69b4", thickness=12)

        self.progress = ttk.Progressbar(root, length=420, mode="determinate", style="pink.Horizontal.TProgressbar")
        self.progress.pack(pady=8)

        # ---------------- Exit ----------------
        exit_btn = tk.Button(root, text="🚪 Exit", width=20, font=("Arial", 11, "bold"), bg="#8b0000",
                             fg="white", activebackground="#5c0000", cursor="hand2", command=root.quit)
        exit_btn.pack(pady=15)
        self.add_hover(exit_btn, "#8b0000", "#b00000")

        self.refresh_listbox()

    # ---------------- Button Creator ----------------
    def create_button(self, parent, text, command, col, color):
        btn = tk.Button(parent, text=text, width=11, font=("Arial", 10, "bold"), bg=color, fg="white", bd=0,
                        cursor="hand2", command=command)
        btn.grid(row=0, column=col, padx=6)
        self.add_hover(btn, color, "#555555")

    # ---------------- Hover Effect ----------------
    def add_hover(self, widget, normal, hover):
        widget.bind("<Enter>", lambda e: widget.config(bg=hover))
        widget.bind("<Leave>", lambda e: widget.config(bg=normal))

    # ---------------- Utility ----------------
    def get_active_list(self):
        return self.filtered_tasks if self.is_searching else self.tasks

    def refresh_listbox(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.get_active_list():
            self.task_listbox.insert(tk.END, task)
        self.update_counter()
        self.update_progress()

    def update_counter(self):
        total = len(self.tasks)
        done = len([t for t in self.tasks if t.startswith(DONE)])
        self.counter_label.config(text=f"💗 Tasks: {total}   |   ✔ Done: {done}")

    def update_progress(self):
        total = len(self.tasks)
        if total == 0:
            self.progress["value"] = 0
            return
        done = len([t for t in self.tasks if t.startswith(DONE)])
        self.progress["value"] = (done / total) * 100

    # ---------------- Features ----------------
    def add_task(self):
        task = self.task_entry.get().strip()
        if not task:
            messagebox.showwarning("Warning", "Task cannot be empty!")
            return
        new_task = PENDING + " " + task
        self.tasks.append(new_task)
        save_tasks(self.tasks)
        play_sound()
        self.task_entry.delete(0, tk.END)
        self.clear_search()

    def delete_task(self):
        try:
            index = self.task_listbox.curselection()[0]
            active = self.get_active_list()
            removed = active[index]
            self.tasks.remove(removed)
            save_tasks(self.tasks)
            play_sound()
            self.clear_search()
        except IndexError:
            messagebox.showwarning("Warning", "Select a task first!")

    def toggle_done(self):
        try:
            index = self.task_listbox.curselection()[0]
            active = self.get_active_list()
            task = active[index]
            updated = task.replace(PENDING, DONE, 1) if task.startswith(PENDING) else task.replace(DONE, PENDING, 1)
            self.tasks[self.tasks.index(task)] = updated
            save_tasks(self.tasks)
            play_sound()
            self.clear_search()
        except IndexError:
            messagebox.showwarning("Warning", "Select a task first!")

    def edit_task(self):
        try:
            index = self.task_listbox.curselection()[0]
            active = self.get_active_list()
            old = active[index]
            text = old[4:]
            new_text = simpledialog.askstring("Edit Task", "Update task:", initialvalue=text)
            if not new_text:
                return
            updated = old[:3] + " " + new_text.strip()
            self.tasks[self.tasks.index(old)] = updated
            save_tasks(self.tasks)
            play_sound()
            self.clear_search()
        except IndexError:
            messagebox.showwarning("Warning", "Select a task first!")

    def search_tasks(self):
        key = self.search_entry.get().strip().lower()
        if not key:
            messagebox.showwarning("Warning", "Enter keyword!")
            return
        self.filtered_tasks = [t for t in self.tasks if key in t.lower()]
        if not self.filtered_tasks:
            messagebox.showinfo("Search", "No match found!")
            return
        self.is_searching = True
        self.refresh_listbox()

    def clear_search(self):
        self.is_searching = False
        self.filtered_tasks = []
        self.search_entry.delete(0, tk.END)
        self.refresh_listbox()

# ---------------- Run ----------------
if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
