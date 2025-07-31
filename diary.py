import sqlite3
from datetime import datetime

# Connect or create the database
conn = sqlite3.connect("diary.db")
c = conn.cursor()

# Create diary table if not exists
c.execute('''
CREATE TABLE IF NOT EXISTS diary (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    title TEXT,
    entry TEXT
)
''')
conn.commit()

# --- Login (Simple password) ---
def login():
    password = "tanaya123"  # 🔒 You can change this
    user_input = input("Enter diary password: ")
    if user_input != password:
        print("❌ Incorrect password. Access denied.")
        exit()
    print("✅ Logged in successfully!\n")

# --- Add Entry ---
def add_entry():
    title = input("Title: ")
    entry = input("Write your entry:\n")
    date = datetime.now().strftime("%Y-%m-%d %H:%M")
    c.execute("INSERT INTO diary (date, title, entry) VALUES (?, ?, ?)", (date, title, entry))
    conn.commit()
    print("✅ Entry saved successfully!\n")

# --- View Entries ---
def view_entries():
    c.execute("SELECT id, date, title FROM diary ORDER BY id DESC")
    rows = c.fetchall()
    if not rows:
        print("📝 No entries yet.\n")
        return
    for row in rows:
        print(f"{row[0]}. [{row[1]}] - {row[2]}")
    entry_id = input("Enter entry number to read or press Enter to skip: ")
    if entry_id:
        c.execute("SELECT * FROM diary WHERE id=?", (entry_id,))
        entry = c.fetchone()
        if entry:
            print(f"\n📝 Title: {entry[2]}\n📅 Date: {entry[1]}\n\n{entry[3]}\n")
        else:
            print("❌ Entry not found.\n")

# --- Delete Entry ---
def delete_entry():
    view_entries()
    entry_id = input("Enter entry number to delete: ")
    c.execute("DELETE FROM diary WHERE id=?", (entry_id,))
    conn.commit()
    print("🗑️ Entry deleted (if it existed).\n")

# --- Main Menu ---
def menu():
    login()
    while True:
        print("==== Digital Diary ====")
        print("1. Add Entry")
        print("2. View Entries")
        print("3. Delete Entry")
        print("4. Exit")
        choice = input("Choose an option: ")
        if choice == '1':
            add_entry()
        elif choice == '2':
            view_entries()
        elif choice == '3':
            delete_entry()
        elif choice == '4':
            print("👋 Exiting diary. Bye!")
            break
        else:
            print("❌ Invalid choice.\n")

menu()
