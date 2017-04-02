"""
File: db.py.

Module provides functions (CRUD) for interfacing with relational db server
running PostgreSQL instance.
"""

import sys

import psycopg2

conn = None


def initialize_db(password):
    """Initialize db connection with provided user password."""
    print('INITIALIZING...')
    global conn

    try:
        conn = psycopg2.connect(database="testtest",
                                user="viktor",
                                password=password,
                                host="127.0.0.1",
                                port="5432")

    except psycopg2.OperationalError as exception:
        print("PASSWORD IS INCORRECT. TRY AGAIN...")
        sys.exit()


def shutdown_db():
    """Close connection to db."""
    print('SHUTDOWN...')
    global conn
    conn.close()


def add_task(values):
    """Add specified task to the database.."""
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (name, priority, category, is_finished) VALUES (%s, %s, %s, %s) RETURNING id;",
                   (values[0], values[1], values[2], values[3]))

    text = cursor.fetchone()[0]
    conn.commit()
    print("Records created successfully")
    return text


def get_tasks():
    """Get all tasks from the database."""
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, priority, category, is_finished from tasks;")
    rows_count = cursor.fetchall()
    return rows_count


def edit_task(id, values):
    """Edit specified task in the database."""
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET name = %s, priority = %s, category = %s, is_finished = %s WHERE id = %s;",
                   (values[0], values[1], values[2], values[3], id))

    conn.commit()
    print("Number of records updated:", cursor.rowcount)


def delete_task(id):
    """Delete specified task from the database."""
    cursor = conn.cursor()
    cursor.execute("DELETE from tasks where id = %s;", (id, ))
    conn.commit()
    print("Number of records deleted:", cursor.rowcount)
