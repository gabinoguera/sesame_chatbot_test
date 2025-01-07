import streamlit as st
import requests
import json
import sseclient

# Configuración de la página
st.set_page_config(page_title="ChatBot AI", page_icon="🤖")
st.title("ChatBot AI 🤖")

# Inicializar el historial de chat en la sesión
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar mensajes del chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input del usuario
if prompt := st.chat_input("Escribe tu mensaje aquí..."):
    # Agregar mensaje del usuario al chat
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Preparar contenedor para la respuesta streaming
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            with requests.post(
                "http://localhost:8000/chat/stream",
                json={"user_message": prompt},
                stream=True
            ) as response:
                client = sseclient.SSEClient(response)
                for event in client.events():
                    if event.data:
                        full_response += event.data
                        message_placeholder.markdown(full_response + "▌")
                
                message_placeholder.markdown(full_response)
                st.session_state.messages.append(
                    {"role": "assistant", "content": full_response}
                )

        except Exception as e:
            st.error(f"Error al comunicarse con el chatbot: {str(e)}") 