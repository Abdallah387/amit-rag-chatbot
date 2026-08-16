import gradio as gr
from test_api import chatbot_response   # استبدل بالمسار/الدالة اللي بترجع رد البوت عندك

# دالة الغلاف اللي Gradio هيستخدمها
def chatbot(message, history=[]):
    # هنا بستدعي دالة البوت الأساسية من مشروعك
    reply = chatbot_response(message)
    history.append((message, reply))
    return history, history

# واجهة Gradio
with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    msg = gr.Textbox(label="Type your message here...")

    def respond(message, history):
        response = chatbot_response(message)
        history = history or []
        history.append((message, response))
        return "", history

    msg.submit(respond, [msg, chatbot], [msg, chatbot])

demo.launch()
