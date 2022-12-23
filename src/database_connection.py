from src.select_dir_location import GetDirectory
import sqlite3
import sys
import os


# Connect to SQLiteDB
class ConnectDatabase(GetDirectory):

    def get_directory(self):
        return GetDirectory.get_directory(self)

    def connect_db(self):
        db_path = os.path.join(self.get_directory(), "chitanka-content/chitanka.db")
        try:
            con = sqlite3.connect('file:' + db_path + '?mode=ro', uri=True)
            # print("DB connected")
            return con.cursor(), "Базата данни е свързана"
        except sqlite3.OperationalError as e:
            print(f"Error connecting to DB: {e}")
            # sys.exit(1)
            return None, f"Неуспешно свързване с базата данни: {e}.\n" \
                         f"Проверете дали сте въвели правилната директория!\n" \
                         f"и опитайте отново."
