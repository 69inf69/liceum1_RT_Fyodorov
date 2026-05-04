import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

class TrainingPlanner:
    def __init__(self, root):
        self.root = root
        self.root.title("Training Planner")
        self.root.geometry("800x600")

        self.trainings = self.load_trainings()

        self.setup_ui()
        self.update_table()

    def setup_ui(self):
        # Фрейм формы добавления
        form_frame = ttk.LabelFrame(self.root, text="Добавить тренировку", padding=10)
        form_frame.pack(fill=tk.X, padx=10, pady=5)

        # Дата
        ttk.Label(form_frame, text="Дата (ГГГГ-ММ-ДД):").grid(row=0, column=0, sticky="w", pady=2)
        self.date_entry = ttk.Entry(form_frame, width=20)
        self.date_entry.grid(row=0, column=1, padx=5, pady=2, sticky="ew")

        # Тип тренировки
        ttk.Label(form_frame, text="Тип тренировки:").grid(row=1, column=0, sticky="w", pady=2)
        self.type_var = tk.StringVar()
        types = ["Кардио", "Силовая", "Йога", "Плавание", "Бег", "Велоспорт"]
        self.type_combobox = ttk.Combobox(form_frame, textvariable=self.type_var, values=types, state="readonly")
        self.type_combobox.grid(row=1, column=1, padx=5, pady=2, sticky="ew")

        # Длительность
        ttk.Label(form_frame, text="Длительность (мин):").grid(row=2, column=0, sticky="w", pady=2)
        self.duration_entry = ttk.Entry(form_frame, width=20)
        self.duration_entry.grid(row=2, column=1, padx=5, pady=2, sticky="ew")

        # Кнопка добавления
        add_btn = ttk.Button(form_frame, text="Добавить тренировку", command=self.add_training)
        add_btn.grid(row=3, column=0, columnspan=2, pady=10)

        form_frame.columnconfigure(1, weight=1)

        # Фрейм фильтрации
        filter_frame = ttk.LabelFrame(self.root, text="Фильтрация", padding=10)
        filter_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(filter_frame, text="Тип:").grid(row=0, column=0, sticky="w")
        self.filter_type_var = tk.StringVar()
        filter_types = ["Все"] + types
        self.filter_type_combobox = ttk.Combobox(filter_frame, textvariable=self.filter_type_var,
                                                   values=filter_types, state="readonly")
        self.filter_type_combobox.grid(row=0, column=1, padx=5)
        self.filter_type_combobox.set("Все")

        ttk.Label(filter_frame, text="Дата:").grid(row=0, column=2, sticky="w", padx=(20, 0))
        self.filter_date_entry = ttk.Entry(filter_frame, width=15)
        self.filter_date_entry.grid(row=0, column=3, padx=5)

        filter_btn = ttk.Button(filter_frame, text="Применить фильтр", command=self.apply_filter)
        filter_btn.grid(row=0, column=4, padx=(10, 0))

        clear_filter_btn = ttk.Button(filter_frame, text="Сбросить фильтр", command=self.clear_filter)
        clear_filter_btn.grid(row=0, column=5, padx=5)

        filter_frame.columnconfigure(1, weight=1)


        # Таблица тренировок
        table_frame = ttk.Frame(self.root)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        columns = ("date", "type", "duration")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        self.tree.heading("date", text="Дата")
        self.tree.heading("type", text="Тип тренировки")
        self.tree.heading("duration", text="Длительность (мин)")
        self.tree.column("date", width=120)
        self.tree.column("type", width=150)
        self.tree.column("duration", width=120)

        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def validate_input(self, date_str, duration_str):
        """Проверка корректности ввода."""
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Ошибка", "Неверный формат даты. Используйте ГГГГ-ММ-ДД")
            return False

        try:
            duration = float(duration_str)
            if duration <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Длительность должна быть положительным числом")
            return False

        return True

    def add_training(self):
        """Добавление новой тренировки."""
        date = self.date_entry.get().strip()
        training_type = self.type_var.get()
        duration = self.duration_entry.get().strip()

        if not self.validate_input(date, duration):
            return

        training = {
            "date": date,
            "type": training_type,
            "duration": float(duration)
        }

        self.trainings.append(training)
        self.save_trainings()
        self.update_table()
        self.clear_form()
        messagebox.showinfo("Успех", "Тренировка добавлена!")

    def clear_form(self):
        """Очистка формы ввода."""
        self.date_entry.delete(0, tk.END)
        self.type_var.set("")
        self.duration_entry.delete(0, tk.END)

    def load_trainings(self):
        """Загрузка тренировок из JSON-файла."""
        if os.path.exists("data.json"):
            try:
                with open("data.json", "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                messagebox.showwarning("Предупреждение", "Не удалось загрузить данные. Создан новый список.")
        return []

    def save_trainings(self):
        """Сохранение тренировок в JSON-файл."""
        try:
            with open("data.json", "w", encoding="utf-8") as f:
                json.dump(self.trainings, f, ensure_ascii=False, indent=2)
        except IOError as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить данные: {e}")


    def update_table(self, filtered_trainings=None):
        """Обновление таблицы тренировок."""
        for item in self.tree.get_children():
            self.tree.delete(item)

        trainings_to_show = filtered_trainings if filtered_trainings is not None else self.trainings

        for training in trainings_to_show:
            self.tree.insert("", tk.END
