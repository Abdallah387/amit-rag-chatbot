
# TODO: Write tests for API endpoints
# TODO: Test root endpoint
# TODO: Test /chat endpoint
# TODO: Test /chat/history endpoint
import sqlite3
import gradio as gr
from spellchecker import SpellChecker

# اتصال بقاعدة البيانات
db_path = "C:/Users/saram/Downloads/my_database.db"  
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Spell checker
spell = SpellChecker()

# إعدادات
greetings = ["hello", "hi", "hey"]
bot_name = "Gminia"
user_name = None

# دوال مساعدة
def correct_text(text):
    words = text.split()
    corrected = [spell.correction(word) or word for word in words]
    return " ".join(corrected)

def is_greeting(text):
    return any(greet in text.lower() for greet in greetings)

def is_status_question(text):
    keywords = ["how are you", "اخبارك", "عامل ايه", "ايه الاخبار"]
    return any(kw in text.lower() for kw in keywords)

def is_name_question(text):
    return "your name" in text.lower() or "اسمك" in text.lower()

def is_name_introduction(text):
    return text.lower().startswith("my name is ") or text.startswith("اسمي ")

def extract_name(text):
    text = text.strip()
    if text.lower().startswith("my name is "):
        return text[11:].strip().capitalize()
    if text.startswith("اسمي "):
        return text[5:].strip()
    return None

def is_user_name_question(text):
    keywords = ["who am i", "my name?", "اسمي ايه", "مين انا"]
    return any(kw in text.lower() for kw in keywords)

def query_database(query, params=()):
    try:
        cursor.execute(query, params)
        rows = cursor.fetchall()
        return rows if rows else None
    except Exception as e:
        return f"❌ Database error: {str(e)}"

def is_database_question(text):
    keywords = ["student", "department", "course", "table", "عدد", "اسماء", "data"]
    return any(kw in text.lower() for kw in keywords)

# الردود
def chatbot_response(user_question):
    global user_name
    user_question = user_question.strip()
    if not user_question:
        return "🟢 Please write something so I can help you."

    user_question = correct_text(user_question)

    # تعريف الاسم
    if is_name_introduction(user_question):
        user_name = extract_name(user_question)
        return f"🟢 Welcome, {user_name}!" if user_name else "🟢 Welcome!"

    # سؤال عن اسم المستخدم
    if is_user_name_question(user_question):
        return f"🟢 Your name is {user_name}!" if user_name else "🟢 I don't know your name yet."

    # سؤال عن الحال
    if is_status_question(user_question):
        return f"🟢 I'm fine, {user_name}!" if user_name else "🟢 I'm fine!"

    # تحيات
    if is_greeting(user_question):
        return f"🟢 Hello {user_name}!" if user_name else "🟢 Hello!"

    # سؤال عن اسم البوت
    if is_name_question(user_question):
        return f"🟢 My name is {bot_name}, {user_name}." if user_name else f"🟢 My name is {bot_name}."

    # أسئلة مرتبطة بالداتابيز
    if is_database_question(user_question):
        if "عدد الطلبة" in user_question or "how many students" in user_question:
            result = query_database("SELECT COUNT(*) FROM Students")
            return f"🟢 عدد الطلبة هو: {result[0][0]}" if result else "❌ No data."

        if "اسماء الطلبة" in user_question or "list students" in user_question:
            result = query_database("SELECT name FROM Students")
            if result:
                names = ", ".join([r[0] for r in result])
                return f"🟢 أسماء الطلبة: {names}"
            else:
                return "❌ No students found."

    return "❌ Sorry, I couldn't understand your question."

# تجربة Gradio
demo = gr.Interface(fn=chatbot_response, inputs="text", outputs="text")
demo.launch()
