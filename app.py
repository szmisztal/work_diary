from db_utils import SQLite


class App:
    def __init__(self):
        self.db = SQLite("word_diary_db.db")
        self.is_running = False

