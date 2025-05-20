import sqlite3

def create_connection():
    conn = sqlite3.connect("results.db", check_same_thread=False)
    return conn

def create_table():
    conn = create_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS results (
            roll_no TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            marks TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def insert_result(roll_no, name, marks):
    conn = create_connection()
    conn.execute("INSERT OR REPLACE INTO results (roll_no, name, marks) VALUES (?, ?, ?)", (roll_no, name, marks))
    conn.commit()
    conn.close()

def get_result(roll_no):
    conn = create_connection()
    cursor = conn.execute("SELECT name, marks FROM results WHERE roll_no=?", (roll_no,))
    result = cursor.fetchone()
    conn.close()
    return result
