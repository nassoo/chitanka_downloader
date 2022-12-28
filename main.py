import logging

from src.main_window import UserInterface


def main():
    logging.basicConfig(level=logging.DEBUG,
                        handlers=[
                            logging.FileHandler("user_data/output.log", mode='w', encoding='utf-8'),
                            logging.StreamHandler()
                        ],
                        format='\n%(asctime)s %(levelname)s %(name)s: %(message)s')

    mw = UserInterface()
    mw.run_main_window()


if __name__ == '__main__':
    main()
