import streamlit as st
from openai import OpenAI
import os



openai_api_key = os.getenv("OPENAI_API_KEY")
password = os.getenv("PASSWORD")

# add password protection for the streamlit app
if password != st.text_input("Password", type="password"):
    st.stop()


# Show title and description.
st.title("📄 Document Chat")
st.write(
    "Upload a document below and ask a question about it – "
)
# create a link to download a txt file
st.write(
    "or download a sample txt about Fake Vitamin"
)
# Load the file content
file_path = "sample.txt"
with open(file_path, "r") as file:
    file_content = file.read()


# Provide a download button
st.download_button(
    label="Download Sample Text File",
    data=file_content,
    file_name="sample.txt",
    mime="text/plain"
)


# Ask user for their OpenAI API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:

    # add button to clear chat
    # st.button("Clear Chat", on_click=lambda: st.session_state.messages.clear())
    
    # Create an OpenAI client.
    client = OpenAI(api_key=openai_api_key, base_url="https://api.groq.com/openai/v1")

    # Let the user upload a file via `st.file_uploader`.
    uploaded_file = st.file_uploader(
        "Upload a document (.txt or .md)", type=("txt", "md")
    )

    # Ask the user for a question via `st.text_area`.
    # question = st.text_area(
    #     "Now ask a question about the document!",
    #     placeholder="Can you give me a short summary?",
    #     disabled=not uploaded_file,
    # )



    if uploaded_file:

        # Process the uploaded file and question.
        document = uploaded_file.read().decode()
        # messages = [
        #     {
        #         "role": "user",
        #         "content": f"Here's a document: {document} \n\n---\n\n {question}",
        #     }
        # ]

        # Create a session state variable to store the chat messages. This ensures that the
        # messages persist across reruns.
        if "messages" not in st.session_state:
            st.session_state.messages = [
                {
                    "role": "user",
                    "content": f"Here's a document: {document}. Answer based on only the document. Any question that cannot find answer from the document will answer with 'I can't find answer from the given materials', including general questions.",
                }
            ]

        # Display the existing chat messages via `st.chat_message`.
        for message in st.session_state.messages[1:]:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        if prompt := st.chat_input("Ask anything about the document"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # Generate an answer using the OpenAI API.
            # stream = client.chat.completions.create(
            #     model="llama-3.3-70b-versatile",
            #     messages=messages,
            #     stream=True,
            # )
            stream = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )

            # Stream the response to the app using `st.write_stream`.
            # st.write_stream(stream)
            with st.chat_message("assistant"):
                response = st.write_stream(stream)
            st.session_state.messages.append({"role": "assistant", "content": response})
