from random import choice
from pathlib import Path
from sqlite3 import connect
from requests import get
from re import findall

class Words:
    def __init__(self):
        db_home = str(Path.home()) + '\wordle.db'
        if not Path(str(Path.home()) + '\wordle.db').is_file():
            self.initialize(db_home)
        self.con = connect(db_home)
        self.cursor = self.con.cursor()
        self.set_word()

    def initialize(self, db_home):
        con = connect(db_home)

        length = 5
        words = []
        regex= r"\w{3} \d{1,2} \d{4} Day \d{1,4} (\w{5})"
        regex1 = r"<a href=\/[a-zA-Z]{"+str(length)+r"}>([a-zA-Z]{"+str(length)+r"}).*?<\/a>"
        regex2 = r"<li><a .*?>(\w{5})<\/a><\/li>"
        regex3 = r"""<a rel="nofollow" title="5 Letter Word - Find the meaning of \w{5}" href="\/word-meaning\/\w{5}">(\w{5})<\/a>"""

        print("Retrieving from the first source")
        i = 1
        page = ""
        while True:
            print(f"page: {i}", end="\r")
            res = get(f"https://en.wikwik.org/{length}letterwords{page}.htm")
            found = findall(regex1, res.text)
            if len(found) == 0:
                break
            words += found
            i+=1
            page=f"page{i}"
        print("\nRetrieving from the second source")
        i = 1
        while True:
            print(f"page: {i}", end="\r")
            res = get(f"https://wordgenerator.org/{length}-letter-words?page={i}")
            found = findall(regex2, res.text)
            if len(found) == 0:
                break
            words += found
            i+=1
        print("\nRetrieving from the third source")
        i=1
        while True:
            print(f"page: {i}", end="\r")
            res = get(f"https://www.wordunscrambler.net/words/{length}-letter?page={i}")
            found = findall(regex3, res.text)
            if len(found) == 0:
                break
            words += found
            i+=1
        print()

        res = get('https://medium.com/@owenyin/here-lies-wordle-2021-2027-full-answer-list-52017ee99e86')
        answers = findall(regex, res.text)

        cursor = con.cursor()
        cursor.execute("""
            CREATE TABLE bank (
            word VARCHAR(50)
            )
        """)
        cursor.execute("""
            CREATE TABLE answers (
            word VARCHAR(50)
            )
        """)
        cursor.executemany("""
            INSERT INTO bank
            VALUES
            (?)
        """, [(i,) for i in words + answers])
        cursor.executemany("""
            INSERT INTO answers
            VALUES
            (?)
        """, [(i,) for i in answers])
        con.commit()
        con.close()

    def get_word(self):
        return self.word

    def set_word(self):
        self.cursor.execute("""
            SELECT word FROM answers
            ORDER BY RANDOM()
            LIMIT 1
            """
        )
        rows = self.cursor.fetchall()
        self.word = rows[0][0].lower()

    def check_word(self, word_to_check):
        self.cursor.execute(f"""
            SELECT word FROM bank
            WHERE word = "{word_to_check}"
            """
        )
        rows = self.cursor.fetchall()
        return len(rows) > 0

    def close(self):
        self.con.close()

def main():
    words = Words()
    print(words.get_word())
    print(words.check_word('boats'))
    print(words.check_word('zzzzz'))
    words.close()

if __name__ == '__main__':
    main()