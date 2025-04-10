import tkinter as tk
from tkinter import ttk

class SimulationController:
    def __init__(self, parent, verse_manager, config_manager):
        self.parent = parent
        self.verse_manager = verse_manager
        self.config_manager = config_manager

        self.frame = ttk.Frame(self.parent)
        self._build_ui()

    def _build_ui(self):
        label = ttk.Label(self.frame, text="Simulation Mode Coming Soon!", font=("Arial", 16))
        label.pack(pady=20)
