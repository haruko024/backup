import mysql.connector

# ==== Database Config ====
DB_HOST = "localhost"
DB_USER = "root"
DB_PASS = "falconwizard"
DB_NAME = "paul_data"

# ==== Connect to DB ====
def get_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME
    )

# ==== Create ====
def insert_user(name, email):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
        conn.commit()
        print("[+] User added successfully.")
    except Exception as e:
        print("[-] Error:", e)
    finally:
        cursor.close()
        conn.close()

# ==== Read ====
def list_users():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, name, email FROM users")
        rows = cursor.fetchall()
        print("\n--- User List ---")
        for row in rows:
            print(f"ID: {row[0]} | Name: {row[1]} | Email: {row[2]}")
    except Exception as e:
        print("[-] Error:", e)
    finally:
        cursor.close()
        conn.close()

# ==== Update ====
def update_user_email(user_id, new_email):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE users SET email=%s WHERE id=%s", (new_email, user_id))
        conn.commit()
        if cursor.rowcount:
            print("[~] Email updated.")
        else:
            print("[-] User not found.")
    except Exception as e:
        print("[-] Error:", e)
    finally:
        cursor.close()
        conn.close()

# ==== Delete ====
def delete_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM users WHERE id=%s", (user_id,))
        conn.commit()
        if cursor.rowcount:
            print("[x] User deleted.")
        else:
            print("[-] User not found.")
    except Exception as e:
        print("[-] Error:", e)
    finally:
        cursor.close()
        conn.close()

# ==== Menu ====
def menu():
    while True:
        print("""
--- CRUD Menu ---
1. Add User
2. Show Users
3. Update User Email
4. Delete User
5. Exit
        """)
        choice = input("Enter choice: ").strip()

        if choice == "1":
            while True:
                name = input("Name: ").strip()
                email = input("Email: ").strip()
                if not name or not email:
                    print("[-] Name and Email cannot be empty.")
                    continue
                insert_user(name, email)
                again = input("Add another? (y/n): ").lower()
                if again != "y":
                    break

        elif choice == "2":
            list_users()

        elif choice == "3":
            user_id = input("User ID: ").strip()
            new_email = input("New Email: ").strip()
            if user_id.isdigit() and new_email:
                update_user_email(int(user_id), new_email)
            else:
                print("[-] Invalid input.")

        elif choice == "4":
            user_id = input("User ID to delete: ").strip()
            if user_id.isdigit():
                delete_user(int(user_id))
            else:
                print("[-] Invalid ID.")

        elif choice == "5":
            print("Goodbye.")
            break

        else:
            print("[-] Invalid choice.")

# ==== Entry Point ====
if __name__ == "__main__":
    menu()
