
# TODO: Implement database connection using psycopg3
# TODO: Initialize the vector database schema using pgvector
import psycopg2

def get_connection():
    conn = psycopg2.connect(
        dbname="chatbot_db",   
        user="postgres", 
        password="12345",      
        host="localhost",       
        port="5432"            
    )
    return conn


from connection import get_connection

def create_tables():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id SERIAL PRIMARY KEY,
                user_input TEXT NOT NULL,
                bot_response TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.commit()
        print(" Tables created successfully!")

        cursor.close()
        conn.close()

    except Exception as e:
        print(" Error while creating tables:", e)

if __name__ == "__main__":
    create_tables()
