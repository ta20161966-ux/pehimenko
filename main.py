import tkinter as tk
from tkinter import messagebox, ttk
import random
import json
import os

# --- Конфигурация ---
FILE_HISTORY = "history.json"
DEFAULT_TASKS = [
    {"name": "Прочитать статью", "type": "учёба"},
    {"name": "Сделать зарядку", "type": "спорт"},
    {"name": "Написать отчёт", "type": "работа"},
    {"name": "Посмотреть обучающее видео", "type": "учёба"},
    {"name": "Погулять на свежем воздухе", "type": "спорт"},
    {"name": "Провести планёрку", "type": "работа"},
]

class TaskGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Task Generator")
        self.root.geometry("500x500")

        # Данные
        self.tasks = DEFAULT_TASKS.copy()
        self.history = self.load_history()

        # Создание виджетов
        self.create_widgets()

    def create_widgets(self):
        # --- Верхняя панель: Генерация задачи ---
        frame_top = tk.Frame(self.root)
        frame_top.pack(pady=10, fill=tk.X)

        self.lbl_current_task = tk.Label(frame_top, text="Ваша задача появится здесь", font=("Arial", 12), wraplength=400)
        self.lbl_current_task.pack()

        btn_generate = tk.Button(frame_top, text="Сгенерировать задачу", command=self.generate_task)
        btn_generate.pack(pady=5)

        # --- Средняя панель: Фильтр и добавление ---
        frame_middle = tk.Frame(self.root)
        frame_middle.pack(pady=10, fill=tk.X)

        # Фильтр
        lbl_filter = tk.Label(frame_middle, text="Фильтр по типу:")
        lbl_filter.grid(row=0, column=0, padx=5)

        self.filter_var = tk.StringVar(value="все")
        filter_options = ["все"] + sorted(list(set(task["type"] for task in self.tasks)))
        filter_menu = ttk.OptionMenu(frame_middle, self.filter_var, *filter_options, command=self.update_history_display)
        filter_menu.grid(row=0, column=1, padx=5)

        # Добавление новой задачи
        lbl_new = tk.Label(frame_middle, text="Добавить свою задачу:")
        lbl_new.grid(row=1, column=0, padx=5, pady=(10, 0))

        self.entry_task = tk.Entry(frame_middle, width=30)
        self.entry_task.grid(row=2, column=0, padx=5)

        # Тип для новой задачи (по умолчанию "прочее")
        self.new_type_var = tk.StringVar(value="прочее")
        type_menu_new = ttk.OptionMenu(frame_middle, self.new_type_var, *filter_options[1:])
        type_menu_new.grid(row=2, column=1, padx=5)

        btn_add = tk.Button(frame_middle, text="Добавить задачу", command=self.add_custom_task)
        btn_add.grid(row=3, column=0, columnspan=2, pady=5)

        # --- Нижняя панель: История ---
        frame_bottom = tk.Frame(self.root)
        frame_bottom.pack(pady=10, fill=tk.BOTH, expand=True)

        lbl_history = tk.Label(frame_bottom, text="История сгенерированных задач:")
        lbl_history.pack()

        self.listbox_history = tk.Listbox(frame_bottom, height=12, width=60)
        self.listbox_history.pack(fill=tk.BOTH, expand=True, padx=5)

    def generate_task(self):
        """Генерирует случайную задачу и добавляет её в историю."""
        if not self.tasks:
            messagebox.showwarning("Нет задач", "Список задач пуст. Добавьте свои задачи!")
            return

        task = random.choice(self.tasks)
        
         # Добавляем в историю (если такой ещё нет в текущей сессии, чтобы не дублировать при каждом запуске)
         # Здесь мы просто добавляем каждое новое сгенерированное событие.
         # Если нужно хранить только уникальные за сессию, логика усложнится.
        
        self.history.append(task)
        
         # Обновляем отображение истории и текущую задачу
         # Текущая задача
        
        self.lbl_current_task.config(text=f"🎲 {task['name']} (Тип: {task['type']})")
        
         # История (с учётом фильтра)
        
        self.update_history_display()
        
         # Сохраняем историю в файл
        
        self.save_history()

    def update_history_display(self, *args):
         """Обновляет список истории в зависимости от выбранного фильтра."""
        
        self.listbox_history.delete(0, tk.END)
        
         filter_type = self.filter_var.get()
        
         for task in self.history:
             if filter_type == "все" or task["type"] == filter_type:
                 self.listbox_history.insert(tk.END, f"{task['name']} ({task['type']})")

    def add_custom_task(self):
         """Добавляет новую задачу, введённую пользователем."""
        
         task_name = self.entry_task.get().strip()
         task_type = self.new_type_var.get()
        
         if not task_name:
             messagebox.showerror("Ошибка", "Поле задачи не может быть пустым!")
             return
        
         new_task = {"name": task_name, "type": task_type}
         self.tasks.append(new_task)
        
         # Обновляем фильтр (добавляем новый тип, если его не было)
         current_options = list(self.filter_var._root().children['menu'].entrycget(0, 'label').split()) # Грязный хак, лучше пересоздать меню или хранить опции отдельно.
         # Проще: обновим список опций в виджете OptionMenu (требует пересоздания, но для учебного проекта допустим простой вариант).
         # Для простоты просто обновим список опций фильтра.
         all_types = sorted(list(set(task["type"] for task in self.tasks)))
         menu = self.filter_var._root().children['menu']
         menu.delete(0, 'end')
         for t in ["все"] + all_types:
             menu.add_command(label=t, command=lambda value=t: self.filter_var.set(value))
         
         # Также обновим меню для типа новой задачи
         menu_new = self.new_type_var._root().children['menu']
         menu_new.delete(0, 'end')
         for t in all_types:
             menu_new.add_command(label=t, command=lambda value=t: self.new_type_var.set(value))
         
         messagebox.showinfo("Успех", f"Задача '{task_name}' добавлена!")
         self.entry_task.delete(0, tk.END) # Очищаем поле ввода

    def save_history(self):
         """Сохраняет историю в файл JSON."""
        
        try:
            with open(FILE_HISTORY, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, ensure_ascii=False, indent=4)
            print("История сохранена.")
            
            # Git: добавить изменения и сделать коммит (автоматизация через Python не рекомендуется для реальных проектов,
            # но для учебного примера можно показать команду)
            os.system('git add .')
            os.system('git commit -m "Обновление истории задач"')
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
             except Exception as e:
            messagebox.showerror("Ошибка сохранения", f"Не удалось сохранить историю: {e}")

    def load_history(self):
         """Загружает историю из файла JSON."""
        
        if os.path.exists(FILE_HISTORY):
            try:
                with open(FILE_HISTORY, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Ошибка загрузки истории: {e}")
                return []
                 return []


if __name__ == "__main__":
    root = tk.Tk()
    app = TaskGeneratorApp(root)
    root.mainloop()
