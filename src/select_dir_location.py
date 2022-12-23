from abc import ABC, abstractmethod
# import tkinter as tk
from tkinter import filedialog


class GetDirectory(ABC):

    def __init__(self):
        self.root = None  # tk.Tk()

    @abstractmethod
    def get_directory(self):
        self.root.withdraw()
        self.root.directory = filedialog.askdirectory()
        return self.root.directory
