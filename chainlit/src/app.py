#########################################################
# Basic example using LangChain with ChatOpenAI wrapper #
#########################################################

import chainlit as cl
from langchain_openai import ChatOpenAI
from langchain_core.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate
)

# Initialize LLM
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

prompt_template = ChatPromptTemplate.from_messages([
    # Provides instructions or context for the LLM e.g. I am a helpful assistant for suggesing books.
    SystemMessagePromptTemplate.from_template(
        "You are a helpful assistant that gives concise, friendly answers."
    ),
    # Pass user input to the prompt from Chainlit
    HumanMessagePromptTemplate.from_template("{user_input}")
])

@cl.on_chat_start
async def on_chat_start():
    cl.user_session.set("messages", [])

@cl.on_message
async def on_message(message: cl.Message):
    # Get previous messages from session - CHAT HISTORY DOESNT WORK
    messages = cl.user_session.get("messages") or []

    # Format prompt with user input
    formatted_messages = prompt_template.format_messages(user_input=message.content)

    # Call LLM
    response = await llm.ainvoke(formatted_messages)

    # Save user and assistant messages to session - CHAT HISTORY DOESNT WORK
    messages.append({"role": "user", "content": message.content})
    messages.append({"role": "assistant", "content": response.content})
    cl.user_session.set("messages", messages)

    await cl.Message(content=response.content).send()