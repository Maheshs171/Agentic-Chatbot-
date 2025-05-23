# import requests

# API_URL = "http://127.0.0.1:5000/query"

# def chat():
#     print("🗨️ Chat with your Appointment Agent (type 'exit' to quit)")
#     while True:
#         user_input = input("You: ")
#         if user_input.lower() in ["exit", "quit"]:
#             print("Goodbye!")
#             break

#         response = requests.post(API_URL, json={"message": user_input})
#         if response.status_code == 200:
#             data = response.json()
#             print("Agent:", data.get("response", "No response"))
#         else:
#             print(f"Error: {response.status_code} - {response.text}")

# if __name__ == "__main__":
#     chat()


#===================================================================================


import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/query"

st.set_page_config(page_title="Appointment Agent", page_icon="🗨️")
st.title("🗨️ Jane - Appointment AI")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"**✔ You:** {msg['content']}")
    else:
        st.markdown(f"**🤖Agent:** {msg['content']}")
        st.markdown("-------------------------------------")

# Form to input and submit message
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("Your message:")
    submitted = st.form_submit_button("Send")

if submitted and user_input:
    # Append user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Send to backend
    try:
        response = requests.post(API_URL, json={"message": user_input})
        if response.status_code == 200:
            data = response.json()
            agent_reply = data.get("response", "No response")
        else:
            agent_reply = f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        agent_reply = f"Request failed: {str(e)}"

    # Append agent message
    st.session_state.messages.append({"role": "agent", "content": agent_reply})

    # Refresh to show new messages
    st.rerun()
