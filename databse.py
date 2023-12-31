import os.path
import sqlite3


class Database:
    DB_PATH = 'stats.db'

    STATS_TABLE = '''
        CREATE TABLE stats(
            times_played INTEGER DEFAULT 0
        )
    '''

    INIT_VALUES = 'INSERT INTO stats VALUES(0)'

    INCREMENT_TIMES_PLAYED = 'UPDATE stats SET times_played = times_played + 1'
    SELECT_TIMES_PLAYED = 'SELECT times_played FROM stats'

    def increment_times_played(self):
        return self.run_query(self.INCREMENT_TIMES_PLAYED, commit=True)

    def get_times_played(self):
        return self.run_query(self.SELECT_TIMES_PLAYED, fetch=True)

    def run_query(self, query, commit=False, fetch=False):
        with self.get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(query)

            if commit:
                connection.commit()
            if fetch:
                return cursor.fetchall()[0][0]  # parsing the result so we get rid of lists in the result

    def initialize(self):
        if os.path.exists(self.DB_PATH):
            return

        with self.get_connection() as connection:
            cursor = connection.cursor()

            cursor.execute(self.STATS_TABLE)
            cursor.execute(self.INIT_VALUES)

            connection.commit()

    def get_connection(self):
        return sqlite3.connect(self.DB_PATH)
