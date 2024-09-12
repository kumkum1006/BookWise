import pandas as pd
import os


class Library:
    def __init__(self, user_id):
        self.user_id = user_id
        self.csv_file = f"{self.user_id}_library_books.csv"
        self._initialize_csv()

    def _initialize_csv(self):
        # Check if user's CSV file exists, if not, create a new one
        if not os.path.exists(self.csv_file):
            df = pd.DataFrame(
                columns=["Title", "Author", "ISBN", "Copies", "Read Within"]
            )
            df.to_csv(self.csv_file, index=False)

    def add_book(self, title, author, ISBN, copies, read_within=False):
        new_book = pd.DataFrame(
            {
                "Title": [title],
                "Author": [author],
                "ISBN": [ISBN],
                "Copies": [copies],
                "Read WithIn": [read_within],
            }
        )

        # Append to the existing CSV file
        df = pd.read_csv(self.csv_file)
        updated_df = pd.concat([df, new_book], ignore_index=True)
        updated_df.to_csv(self.csv_file, index=False)
        print(f"{title} has been added to the library.")

    def check_in_book(self, ISBN=None, title=None):
        df = pd.read_csv(self.csv_file)

        if ISBN:
            book_index = df[df["ISBN"] == ISBN].index
        elif title:
            book_index = df[df["Title"].str.lower() == title.lower()].index
        else:
            print("Please provide ISBN or Title.")
            return

        if len(book_index) > 0:
            df.at[book_index[0], "Copies"] += 1
            df.to_csv(self.csv_file, index=False)
            print(f"Book has been checked in.")
        else:
            print("Book not found!")

    def check_out_book(self, ISBN=None, title=None):
        df = pd.read_csv(self.csv_file)

        if ISBN:
            book_index = df[df["ISBN"] == ISBN].index
        elif title:
            book_index = df[df["Title"].str.lower() == title.lower()].index
        else:
            return None("Please provide ISBN or Title.")
            return

        if len(book_index) > 0:
            if df.at[book_index[0], "Read WithIn"]:
                return False, ("This book can only be read within the library.")
            elif df.at[book_index[0], "Copies"] > 0:
                df.at[book_index[0], "Copies"] -= 1
                df.to_csv(self.csv_file, index=False)
                return True, (f"Book has been checked out.")
            else:
                return None, ("No copies available.")
        else:
            return None, ("Book not found!")
