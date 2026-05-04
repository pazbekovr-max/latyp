import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import json
import os

# Файл для сохранения истории
DATA_FILE = "task_history.json"

# Предопределенные задачи с категориями
DEFAULT_TASKS = [
    {"text": "Прочитать статью", "category": "учёба"},
    {"text": "Сделать зарядку", "category": "спорт"},
    {"text": "Проверить почту", "category": "работа"},
    {"text": "Выучить 5 новых слов", "category": "учёба"},
    {"text": "Пробежать 1 км", "category": "спорт"},
    {"text": "Написать отчет", "category": "работа"},
    {"text": "Посмотреть документальный фильм", "category": "учёба"},
    {"text": "Убрать рабочее место", "category": "работа"}
]

class TaskGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Task Generator")
        self.root.geometry("500x600")
        
        self.tasks = []
        self.history = []
        
        # Загрузка данных
        self.load_data()
        if not self.tasks:
            self.tasks = DEFAULT_TASKS

        self.create_widgets()

    def create_widgets(self):
        # Заголовок
        tk.Label(self.root, text="Генератор случайных задач", font=("Arial", 16, "bold")).pack(pady=10)

        # Область отображения текущей задачи
        self.task_label = tk.Label(self.root, text="Нажмите кнопку, чтобы получить задачу", font=("Arial", 14), fg="blue", wraplength=400)
        self.task_label.pack(pady=20)

        # Кнопка генерации
        self.generate_btn = tk.Button(self.root, text="Сгенерировать задачу", command=self.generate_task, bg="#4CAF50", fg="white", font=("Arial", 12))
        self.generate_btn.pack(pady=5)

        # Фильтр
        filter_frame = tk.Frame(self.root)
        filter_frame.pack(pady=10)
        tk.Label(filter_frame, text="Фильтр по категории:").pack(side=tk.LEFT)
        self.filter_var = tk.StringVar(value="Все")
        categories = ["Все", "учёба", "спорт", "работа"]
        self.filter_menu = tk.OptionMenu(filter_frame, self.filter_var, *categories, command=self.update_history_view)
        self.filter_menu.pack(side=tk.LEFT, padx=5)

        # Список истории
        tk.Label(self.root, text="История задач:", font=("Arial", 12, "bold")).pack(pady=5)
        self.history_listbox = tk.Listbox(self.root, height=10, width=60)
        self.history_listbox.pack(pady=5)
        
        # Кнопка добавления новой задачи
        add_btn = tk.Button(self.root, text="Добавить свою задачу", command=self.add_task)
        add_btn.pack(pady=10)

        # Кнопка сохранения (автоматически сохраняется, но можно добавить ручное)
        save_btn = tk.Button(self.root, text="Сохранить историю", command=self.save_data)
        save_btn.pack(pady=5)

        # Инициализация списка
        self.update_history_view()

    def generate_task(self):
        if not self.tasks:
            messagebox.showwarning("Внимание", "Список задач пуст! Добавьте новые задачи.")
            return

        task = random.choice(self.tasks)
        task_text = f"{task['text']} ({task['category']})"
        
        self.task_label.config(text=task_text)
        
        # Добавляем в историю
        history_entry = {
            "text": task["text"],
            "category": task["category"],
            "timestamp": "Сгенерировано" # В реальном проекте лучше использовать datetime
        }
        self.history.insert(0, history_entry)
        self.save_data()
        self.update_history_view()

    def add_task(self):
        # Ввод текста задачи
        task_text = simpledialog.askstring("Новая задача", "Введите текст задачи:")
        if not task_text or task_text.strip() == "":
            messagebox.showerror("Ошибка", "Текст задачи не может быть пустым!")
            return

        # Ввод категории
        category = simpledialog.askstring("Категория", "Введите категорию (учёба, спорт, работа):")
        if not category or category.strip() == "":
            messagebox.showerror("Ошибка", "Категория не может быть пустой!")
            return

        new_task = {"text": task_text.strip(), "category": category.strip().lower()}
        self.tasks.append(new_task)
        messagebox.showinfo("Успех", f"Задача '{task_text}' добавлена!")
        self.save_data()

    def update_history_view(self):
        self.history_listbox.delete(0, tk.END)
        filter_cat = self.filter_var.get()

        for entry in self.history:
            if filter_cat == "Все" or entry["category"] == filter_cat:
                display_text = f"{entry['text']} - {entry['category']}"
                self.history_listbox.insert(tk.END, display_text)

    def save_data(self):
        data = {
            "tasks": self.tasks,
            "history": self.history
        }
        try:
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить данные: {e}")

    def load_data(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.tasks = data.get("tasks", [])
                    self.history = data.get("history", [])
            except Exception:
                self.tasks = DEFAULT_TASKS
                self.history = []

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskGeneratorApp(root)
    root.mainloop()
