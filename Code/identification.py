
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
import uuid
import sqlite3

ph = PasswordHasher()

def register(username,password):
    password_hash = ph.hash(password)
    player_id = str(uuid.uuid4())
    conn = sqlite3.connect("user_database.sqlite")
    cursor = conn.cursor()
    try:
        cursor.execute("""INSERT INTO user_table (user_uuid, user_id, user_password) VALUES (?, ?, ?)""", (player_id, username, password_hash))
        conn.commit()
        return player_id
    except sqlite3.IntegrityError:
        print("Erreur : identifiant déjà utilisé")
        return None
    finally:
        conn.close()

def login(username,password):
    conn = sqlite3.connect("user_database.sqlite")
    cursor = conn.cursor()
    stored_user = cursor.execute("""SELECT user_uuid, user_password FROM user_table WHERE user_id = ?""", (username,)).fetchone()
    conn.close()
    if stored_user:
        stored_password = stored_user[1]
    else:
        print("Erreur : identifiant incorrect")
        return None
    try:
        ph.verify(stored_password,password)
        print(f"Utilsateur {username} connecté avec succès")
        return stored_user[0] 
    except VerifyMismatchError:
        print("Erreur : mot de passe incorrect")
        return None

if __name__ == "__main__":
    register("Odeline","BestPersonEver")
    login("Odeline","BestPersonEver")
    login("Odelin","BestPersonEver")
    login("Odeline","WorstPersonEver")
