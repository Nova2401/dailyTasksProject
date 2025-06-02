import json
import tkinter as tk
from datetime import datetime, date
from tkinter import messagebox, simpledialog


class DailyTasksApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ежедневные задачи")
        self.tasks = []
        self.data_file = "tasks.json"

        # Перенесём вызов load_tasks() после определения всех методов
        self.setup_ui()  # Сначала инициализируем интерфейс
        self.load_tasks()  # Затем загружаем задачи

        # Проверяем, нужно ли сбросить задачи (если новый день)
        if not self.was_reset_today():
            self.reset_tasks_status()

    def was_reset_today(self):
        """Проверяет, был ли сегодня сброс задач"""
        today = date.today().isoformat()
        return any(task.get("last_reset") == today for task in self.tasks)

    def load_tasks(self):
        """Загружает задачи из JSON-файла"""
        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                self.tasks = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.tasks = []
        finally:
            self.update_task_listbox()  # Обновляем список после загрузки

    def save_tasks(self):
        """Сохраняет задачи в JSON-файл"""
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(self.tasks, f, ensure_ascii=False, indent=2)

    def reset_tasks_status(self):
        """Сбрасывает статус выполнения всех задач"""
        today = date.today().isoformat()
        for task in self.tasks:
            task["completed"] = False
            task["last_reset"] = today
        self.save_tasks()
        self.update_task_listbox()

    def setup_ui(self):
        """Настраивает интерфейс"""
        # Фрейм для списка задач
        self.task_frame = tk.Frame(self.root)
        self.task_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        # Список задач
        self.task_listbox = tk.Listbox(
            self.task_frame,
            width=60,
            height=20,
            font=("Arial", 15),
            selectbackground="#d9d9d9"
        )
        self.task_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Скроллбар
        scrollbar = tk.Scrollbar(self.task_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.task_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.task_listbox.yview)

        # Кнопки управления
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=5)

        tk.Button(
            button_frame,
            text="Добавить задачу",
            command=self.add_task,
            bg="#4CAF50",
            fg="white"
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            button_frame,
            text="Удалить задачу",
            command=self.delete_task,
            bg="#f44336",
            fg="white"
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            button_frame,
            text="Сбросить галочки",
            command=self.reset_tasks_status,
            bg="#2196F3",
            fg="white"
        ).pack(side=tk.LEFT, padx=5)

        # Обработка клика по задаче (отметка выполнения)
        self.task_listbox.bind("<Button-1>", self.toggle_task_status)

    def update_task_listbox(self):
        """Обновляет список задач в интерфейсе"""
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            status = "✓" if task["completed"] else "◻"
            self.task_listbox.insert(tk.END, f"{status} {task['name']}")

    def add_task(self):
        """Добавляет новую задачу"""
        new_task = simpledialog.askstring("Новая задача", "Введите задачу:")
        if new_task and new_task.strip():
            self.tasks.append({
                "name": new_task.strip(),
                "completed": False,
                "last_reset": date.today().isoformat()  # Исправлено на last_reset
            })
            self.save_tasks()
            self.update_task_listbox()

    def delete_task(self):
        """Удаляет выбранную задачу"""
        selected = self.task_listbox.curselection()
        if selected:
            index = selected[0]
            self.tasks.pop(index)
            self.save_tasks()
            self.update_task_listbox()

    def toggle_task_status(self, event):
        """Отмечает задачу выполненной/невыполненной"""
        selected = self.task_listbox.curselection()
        if selected:
            index = selected[0]
            self.tasks[index]["completed"] = not self.tasks[index]["completed"]
            self.save_tasks()
            self.update_task_listbox()


if __name__ == "__main__":
    root = tk.Tk()
    app = DailyTasksApp(root)
    root.mainloop()