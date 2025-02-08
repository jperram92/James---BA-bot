import requests
from dotenv import load_dotenv
import os
import streamlit as st
import time

load_dotenv()  # Load environment variables

BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = "fc5863d6-b718-4ba7-9158-d43ea09066fd"
FLOW_ID = "e5e837db-ff19-45a1-ae69-4d1df9d262da"
APPLICATION_TOKEN = os.environ.get('APP_TOKEN')  # Ensure the token is loaded
ENDPOINT = "Customer"

def run_flow(message: str) -> dict:
    if not APPLICATION_TOKEN:
        raise ValueError("Application token is not set in the environment variables.")
    
    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{ENDPOINT}"
    
    payload = {
        "input_value": message,
        "output_type": "chat",
        "input_type": "chat",
    }
    
    headers = {
        "Authorization": f"Bearer {APPLICATION_TOKEN}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(api_url, json=payload, headers=headers)
    
    # Check if the response is successful
    if response.status_code != 200:
        raise Exception(f"Error: {response.status_code} - {response.text}")
    
    return response.json()

def main():
    # Apply custom CSS for styling
    st.markdown("""
        <style>
        .stTextArea>div>textarea {
            background-color: #f0f0f5;
            border: 2px solid #4a90e2;
            border-radius: 5px;
            padding: 10px;
        }
        .css-1d391n6 {
            color: white;
            font-size: 2em;
        }
        .stButton>button {
            background-color: #4a90e2;
            color: white;
            font-size: 1.2em;
            padding: 10px 20px;
            border-radius: 5px;
        }
        .stButton>button:hover {
            background-color: #357ab7;
        }
        </style>
    """, unsafe_allow_html=True)

    # Title of the interface
    st.title("James Chat Interface")

    # File upload feature with multiple file support
    uploaded_files = st.file_uploader("Upload files", type=["txt", "csv", "xlsx"], accept_multiple_files=True)
    
    if uploaded_files:
        for uploaded_file in uploaded_files:
            # For example, reading a CSV file
            if uploaded_file.type == "text/csv":
                import pandas as pd
                df = pd.read_csv(uploaded_file)
                st.write(f"Contents of {uploaded_file.name}:", df)

            # Add more file handling logic if necessary for other file types
            st.success(f"File {uploaded_file.name} uploaded successfully!")

    # Text area for user input with placeholder and styling
    message = st.text_area("Enter your message", placeholder="Ask a question", height=150)

    # Add a condition to run flow when button is clicked
    if st.button("Run Flow"):
        if not message.strip():
            st.error("Please enter a message before running the flow!")
            return

        try:
            # Show a loading spinner while the flow runs
            with st.spinner("Running the flow..."):
                # Simulate flow processing time (e.g., API call or logic execution)
                time.sleep(3)  # Simulate processing time, remove in production
                
                # Fetch response from the API
                response = run_flow(message)
                
                # Assuming the response structure
                response_text = response.get("outputs", [{}])[0].get("outputs", [{}])[0].get("results", {}).get("message", {}).get("text", "")
                
                # Display the response
                if response_text:
                    st.markdown("**Response:**")
                    st.markdown(response_text)
                else:
                    st.warning("No valid response received.")

                # Provide success feedback
                st.success("Flow executed successfully!")

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
