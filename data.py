"""TODO."""

import psycopg2

conn = None


def get_items():
    """TODO."""
    cur = conn.cursor()
    cur.execute("SELECT id, name, priority, category, is_finished from tasks;")
    rows = cur.fetchall()
    return rows


def remove_item(item):
    """TODO."""
    cur = conn.cursor()
    cur.execute("DELETE from tasks where id = " + item + ";")
    conn.commit()
    print("Number of records deleted:", cur.rowcount)


def change_item(text, values):
    """TODO."""
    cur = conn.cursor()
    cur.execute("UPDATE tasks set name = '" + values[0] + "', priority = " + values[1] + ", category = '" + values[2] + "', is_finished = " + values[3] + " where ID = " + text + ";")
    conn.commit()
    print("Number of records updated:", cur.rowcount)


def create_item(values):
    """TODO."""
    cur = conn.cursor()
    cur.execute("INSERT INTO tasks (name, priority, category, is_finished) VALUES ('" + values[0] + "', " + values[1] + ", '" + values[2] + "', " + values[3] + ") RETURNING id;" );
    text = cur.fetchone()[0]
    conn.commit()
    print("Records created successfully")
    return text


def initialize_db():
    """TODO."""
    print('INITIALIZING...')
    global conn
    conn = psycopg2.connect(database="testtest", user="viktor", password="v1i2t3y4a5!", host="127.0.0.1", port="5432")


def shutdown_db():
    """TODO."""
    print('SHUTDOWN...')
    global conn
    conn.close()
