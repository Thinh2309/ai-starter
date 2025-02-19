import os
import  gradio as gr
from groq import Groq


client = Groq(api_key="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")

def chatlogic(message, chat_history):
    messages = []
    for user_message, bot_message in chat_history:
        messages.append({"role": "user", "content": user_message})
        messages.append({"role": "assistant", "content": bot_message})

    messages.append({"role": "user", "content": message})

    stream = client.chat.completions.create(
        messages = messages,
        model = "gemma2-9b-it",
        stream = True
    )
    chat_history.append([message, ""])
    yield "", chat_history
    # chat_history[-1][1]
    for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta is None:
            delta = ""
        chat_history[-1][1] += delta
        yield "", chat_history
    return "",chat_history

with gr.Blocks() as demo:
    gr.Markdown("#demo chat gpt")
    chatbox = gr.Chatbot(label="cháu nội của gpt!")
    message = gr.Textbox(label="nhắn tin cho cháu nội gpt:")
 
    message.submit(chatlogic, inputs=[message, chatbox], outputs=[message, chatbox])
demo.launch(share=True)