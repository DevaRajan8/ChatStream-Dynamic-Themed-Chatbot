import streamlit as st
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from datetime import datetime
from zoneinfo import ZoneInfo
template = """
You are a helpful assistant. Respond to the user's question in a concise and informative manner.
Here is the conversation history:{context}
User question: {question}
Your answer:
"""
model = OllamaLLM(model="llama3.1")
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model
def main():
    st.sidebar.title("Theme")
    theme_option=st.sidebar.radio(
        "Select Theme",
        ["🌞 Light", "🌜 Dark"],
        index=0
    )
    if theme_option=="🌜 Dark":
        st.markdown("""
            <style>
            .main {
                background-color: #2e2e2e;
                color: #ffffff;
            }
            .stButton>button {
                color: #ffffff;
                background-color: #4a4a4a;
            }
            .stSelectbox>div>div>div {
                color: #ffffff;
            }
            h1, h2, h3, h4, h5, h6 {
                color: #ffffff;
            }
            .stChatMessage[data-testid="stChatMessage"] {
                background-color: #1f1f1f !important; /* Even darker gray */
                color: #ffffff !important;
                border-radius: 5px;
                padding: 10px;
                margin: 5px 0;
            }
            .stChatMessage[data-testid="stChatMessage"][data-testid="assistant"] {
                background-color: #161616 !important; /* Even darker */
                color: #ffffff !important;
            }
            .stChatMessage[data-testid="stChatMessage"][data-testid="user"] {
                background-color: #2a2a2a !important; /* Even darker gray for user */
                color: #ffffff !important;
            }
            </style>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <style>
        .main {
            background-color: #ffffff;
            color: #000000;
        }
        .stButton>button {
            color: #000000;
            background-color: #f0f0f0;
        }
        .stSelectbox>div>div>div {
            color: #000000;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #000000;
        }
        .stChatMessage[data-testid="stChatMessage"] {
            background-color: #a0a0a0 !important; /* Darker gray */
            color: #000000 !important;
            border-radius: 5px;
            padding: 10px;
            margin: 5px 0;
        }
        .stChatMessage[data-testid="stChatMessage"][data-testid="assistant"] {
            background-color: #808080 !important; /* Even darker */
            color: #000000 !important;
        }
        .stChatMessage[data-testid="stChatMessage"][data-testid="user"] {
            background-color: #909090 !important; /* Even darker gray for user */
            color: #000000 !important;
        }
        </style>
        """, unsafe_allow_html=True)
    if 'context' not in st.session_state:
        st.session_state.context=""
    if 'messages' not in st.session_state:
        st.session_state.messages=[]
    def get_greeting():
        now=datetime.now(ZoneInfo("Asia/Kolkata"))
        current_hour=now.hour
        if current_hour < 12:
            return "Good Morning"
        elif 12 <= current_hour < 15:
            return "Good Afternoon"
        else:
            return "Good Evening"
    greeting = get_greeting()
    st.write(f"### {greeting}! I'm here to assist you with your queries.")
    st.write("**This chatbot is designed to provide you with accurate and helpful responses based on the information available. Feel free to ask any questions you may have!**")
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    if prompt := st.chat_input("You:"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        result = chain.invoke({"context": st.session_state.context, "question": prompt})
        st.session_state.context += f"\nUser: \n{prompt}  \n    AI: \n{result}\n"  # Append the conversation to context
        with st.chat_message("assistant"):
            st.markdown(result)
        st.session_state.messages.append({"role": "assistant", "content": result})
    if st.button("History"):
        st.sidebar.write("Conversation History:")
        st.sidebar.write(st.session_state.context)
if __name__ == "__main__":
    main()
