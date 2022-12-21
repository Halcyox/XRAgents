import sqlite3

def print_table(conn, table_name):
    c = conn.cursor()
    c.execute("SELECT * FROM {}".format(table_name))

    # get the column names
    names = list(map(lambda x: x[0], c.description))

    # get the table data
    data = c.fetchall()

    # find the maximum width for each column
    widths = []
    for name in names:
        widths.append(len(name))
    for row in data:
        for i, col in enumerate(row):
            widths[i] = max(widths[i], len(str(col)))

    # print the table
    for name, width in zip(names, widths):
        print("{:<{}}".format(name, width), end=" ")
    print()
    for row in data:
        for col, width in zip(row, widths):
            print("{:<{}}".format(col, width), end=" ")
        print()

def get_tables(conn):
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table'")
    return [row[0] for row in c.fetchall()]


def print_database(conn):
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in c.fetchall()]

    for table in tables:
        print("Table: {}".format(table))
        print_table(conn, table)
        print()

conn = sqlite3.connect("digital-humans.db")
print_database(conn)