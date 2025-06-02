import json
import tkinter
from datetime import datetime, date

class DailyTasksApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ежедневные задачи")
        self.tasks = []
        self.d