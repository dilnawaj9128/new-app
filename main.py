import mysql.connector
import time
import sys

def get_db_connection():
    # Retry logic: Kyunki MySQL start hone mein thoda waqt leta hai
    while True:
        try:
            connection = mysql.connector.connect(
                host='db',          # Docker compose mein service ka naam 'db' hai
                user='root',
                password='password123',
                database='student_db'
            )
            return connection
        except mysql.connector.Error:
            print("Database se connect ho raha hai... intezar karein.")
            time.sleep(5)

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS students (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), course VARCHAR(255))")
    conn.commit()
    conn.close()

def add_student(name, course):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO students (name, course) VALUES (%s, %s)", (name, course))
    conn.commit()
    conn.close()
    print(f"\n[Success] {name} ka data MySQL mein save ho gaya!")

def view_students():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()
    conn.close()
    print("\n--- Student Records (From MySQL) ---")
    for row in rows:
        print(f"ID: {row[0]} | Name: {row[1]} | Course: {row[2]}")

if __name__ == "__main__":
    init_db()
    while True:
        print("\n1. Add Student\n2. View Students\n3. Exit")
        choice = input("Option select karein: ")
        if choice == '1':
            n = input("Name: ")
            c = input("Course: ")
            add_student(n, c)
        elif choice == '2':
            view_students()
        elif choice == '3':
            sys.exit()