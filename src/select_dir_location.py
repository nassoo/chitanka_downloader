from tkinter import filedialog


class GetDirectory:

    @staticmethod
    def get_directory():
        # self.root.withdraw()
        directory = filedialog.askdirectory()
        return directory
