import streamlit as st
import requests

st.title("AI RAG Document Q&A System")

uploaded_file = st.file_uploader("Upload a PDF document", type="pdf")

if uploaded_file is not None:
    if st.button("Process Document"):
        files = {
            "file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")
        }
        response = requests.post("http://localhost:8001/upload", files=files)
        if response.status_code == 200:
            st.success("Document processed successfully!")
        else:
            st.error(f"Failed to process document: {response.text}")

question = st.text_input("Ask a question about the document")

if st.button("Ask"):
    if question:
        data = {"question": question}
        response = requests.post("http://localhost:8001/ask", json=data)
        if response.status_code == 200:
            data = response.json()
            answer = data["answer"]
            confidence = data.get("confidence", None)
            st.write("Answer:", answer)
            if confidence is not None:
                st.write(f"Confidence: {confidence}")
        else:
            st.error("Failed to get answer")
    else:
        st.warning("Please enter a question")
