import logging
import os
import importlib.util

from src.app import App


def main():
    if '_PYIBoot_SPLASH' in os.environ and importlib.util.find_spec("pyi_splash"):
        import pyi_splash
        pyi_splash.update_text('UI Loaded ...')
        pyi_splash.close()

    logging.basicConfig(level=logging.DEBUG,
                        handlers=[
                            logging.FileHandler("user_data/output.log", mode='w', encoding='utf-8'),
                            logging.StreamHandler()
                        ],
                        format='\n%(asctime)s %(levelname)s %(name)s: %(message)s')

    app = App()
    app.mainloop()


if __name__ == '__main__':
    main()
