import chainlit as cl
from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

@cl.on_chat_start
async def on_chat_start():
    cl.user_session.set("messages", [
        {"role": "system", "content": "You are a helpful assistant."}
    ])

@cl.on_message
async def on_message(message: cl.Message):
    messages = cl.user_session.get("messages") or []

    # Add user message
    messages.append({"role": "user", "content": message.content})

    # Call model
    response = await model.ainvoke(messages)

    # Add assistant response
    messages.append({"role": "assistant", "content": response.content})

    # Save back to session
    cl.user_session.set("messages", messages)

    await cl.Message(content=response.content).send()