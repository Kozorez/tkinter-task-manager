import psycopg2

def get_items():
    conn = psycopg2.connect(database="testtest", user="viktor", password="v1i2t3y4a5!", host="127.0.0.1", port="5432")

    print("Opened database successfully")

    cur = conn.cursor()

    cur.execute("SELECT id, name, priority, category, is_finished from tasks")
    rows = cur.fetchall()

    print("Operation done successfully")
    conn.close()
    return rows

def remove_item(item):
    conn = psycopg2.connect(database="testtest", user="viktor", password="v1i2t3y4a5!", host="127.0.0.1", port="5432")
    print("Opened database successfully")

    cur = conn.cursor()
    string = "DELETE from tasks where id = " + item + ";"
    #print(string)
    cur.execute(string)
    conn.commit()

    print("Total number of rows deleted :", cur.rowcount)

    print("Operation done successfully")
    conn.close()

def change_item(item):
    print(item)
