import streamlit as st
import time, os
from io import BytesIO
import pandas as pd
from library_backend import Library
import xlsxwriter

# THIS SHOULD ALWAYS BE THE FIRST LINE AFTER IMPORTS
st.set_page_config("LMS", page_icon="logo.png")

hide_isbn_css = """
    <style>
    [data-testid="stNumberInputStepDown"] {
        display: none;
    }
    [data-testid="stNumberInputStepUp"] {
    display: none;
    }
    </style>
"""
st.markdown(hide_isbn_css, unsafe_allow_html=True)

st.title("Library Management Sysytem")
user_id = st.text_input("Please enter your email address")

if user_id:
    library = Library(user_id)
    csv_file = f"{user_id}_library_books.csv"

    if os.path.exists:
        df = pd.read_csv(csv_file)
    else:
        st.data_editor(
            pd.DataFrame(columns=["Title", "Author", "ISBN", "Copies", "Read Within"]),
            use_container_width=True,
        )

    st.subheader(f"Library Inventory for {user_id}")
    st.data_editor(df, use_container_width=True, hide_index=True)

    operation_options = ["Add Book", "Check In", "Check Out", "Download File"]
    st.subheader("What operations are you trying to perform?")
    opration = st.radio(
        "",
        options=operation_options,
        horizontal=True,
        index=None,
        label_visibility="collapsed",
    )

    # Adding Book
    if opration == "Add Book":
        with st.form(key="add-book", clear_on_submit=True):
            st.write("This is a form to add a new book")
            title = st.text_input("please enter the book title")

            author = st.text_input("please enter the book author")

            isbn = st.number_input(
                "please enter the ISBN of the book",
                step=1,
                value=None,
            )
            if isbn:
                if len(str(int(isbn))) != 13:
                    st.info("ISBN Number must be 13 digits")

            num_of_copies = st.number_input(
                "How many copies", step=1, value=None, min_value=1
            )

            read_within_book = st.checkbox("Is this a special book?")

            submit = st.form_submit_button("Submit", type="primary")
            if submit:
                library.add_book(title, author, isbn, num_of_copies, read_within_book)
                st.success(
                    f"A New book with called {title} with {num_of_copies} copies has been added."
                )
                time.sleep(3)
                st.rerun()

    # Checking in Book
    if opration == "Check In":
        none, toggle_column = st.columns([1, 0.2], gap="large")
        with toggle_column:
            toggle_title_or_isbn = st.toggle("ISBN")

        # title or ISBN
        if toggle_title_or_isbn == False:
            title = st.text_input("please enter the book title", key=10)
        else:
            isbn = st.number_input(
                "please enter the ISBN of the book",
                step=1,
                value=None,
                key=11,
            )
            if isbn:
                if len(str(int(isbn))) != 13:
                    st.info("ISBN Number must be 13 digits")

        submit = st.button("Submit", type="primary")
        if submit:
            if toggle_title_or_isbn == False:
                library.check_in_book(ISBN=None, title=title)
                st.success(f"The {title} book has been checked in.")
            else:
                library.check_in_book(ISBN=isbn, title=None)
                st.success(f"The book with ISBN {isbn} book has been checked in.")

            time.sleep(3)
            st.rerun()

    # Checking Out Book
    if opration == "Check Out":

        none, toggle_column = st.columns([1, 0.2], gap="large")
        with toggle_column:
            toggle_title_or_isbn = st.toggle("ISBN")

        # title or ISBN
        if toggle_title_or_isbn == False:
            title = st.text_input("please enter the book title", key=10)
        else:
            isbn = st.number_input(
                "please enter the ISBN of the book",
                step=1,
                value=None,
                key=11,
            )
            if isbn:
                if len(str(int(isbn))) != 13:
                    st.info("ISBN Number must be 13 digits")

        submit = st.button("Submit", type="primary")
        if submit:
            if toggle_title_or_isbn == False:
                success, message = library.check_out_book(ISBN=None, title=title)
                if success is True:
                    st.success(f"The book {title} has been checked out successfully!")
                elif success is False:
                    st.error("This is a special book and it can not be checked out!")
            else:
                library.check_out_book(ISBN=isbn, title=None)
                success, message = library.check_out_book(ISBN=isbn, title=None)
                if success is True:
                    st.success(
                        f"The book with ISBN {isbn} has been checked out successfully!"
                    )
                elif success is False:
                    st.error("This is a special book and it can not be checked out!")

            time.sleep(3)
            st.rerun()

    # download file
    if opration == "Download File":
        if os.path.exists(csv_file):
            # Load the user's library data
            df = pd.read_csv(csv_file)

            # Button to download CSV
            csv_data = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="Download Library as CSV",
                data=csv_data,
                file_name=f"{user_id}_library_books.csv",
                mime="text/csv",
            )

            # Button to download Excel
            def to_excel(df):
                output = BytesIO()
                with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
                    df.to_excel(writer, index=False, sheet_name="Library")
                return output.getvalue()

            excel_data = to_excel(df)
            st.download_button(
                label="Download Library as Excel",
                data=excel_data,
                file_name=f"{user_id}_library_books.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
