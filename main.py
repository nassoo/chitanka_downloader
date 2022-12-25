import logging

from src.main_window import UserInterface


def main():
    logging.basicConfig(filename='user_data/output.log', level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(name)s %(message)s')

    mw = UserInterface()
    mw.run_main_window()


if __name__ == '__main__':
    main()
