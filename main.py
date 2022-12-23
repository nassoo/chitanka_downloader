from src.download_from_server import DownloadFiles
from src.get_urls import GetContent
from src.main_window import UserInterface


def main():
    # gb = GetBooks()
    # gb.get_urls()
    # dl = DownloadBooks()
    # dl.download()
    mw = UserInterface()
    mw.run_main_window()


if __name__ == '__main__':
    main()
