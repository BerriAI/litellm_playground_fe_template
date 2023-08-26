import streamlit as st
import threading
import requests

# Function to get model outputs
def get_model_output_thread(prompt, model_name, outputs, idx):
    url = "http://localhost:4000/chat/completions" ## REPLACE THIS WITH YOUR DEPLOYED ENDPOINT
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "model": model_name,
        "messages": [
            {
                "content": prompt,
                "role": "user"
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data)
    response_data = response.json()
  
    output = response_data['choices'][0]['message']['content']
    outputs[idx] = output

# Streamlit app
def main():
    st.title("My LLM API Playground")
    st.subheader("Powered by [LiteLLM]((https://github.com/BerriAI/litellm/))")

    # Sidebar for user input
    st.header("User Input")
    prompt = st.text_area("Enter your prompt here:")
    submit_button = st.button("Submit")
    
    # Main content area to display model outputs
    st.header("Model Outputs")
    
    # List of models to test
    model_names = ["gpt-3.5-turbo", "command-nightly", "j2-mid"]  # Add your model names here
    
    cols = st.columns(len(model_names))  # Create columns
    outputs = [""] * len(model_names)  # Initialize outputs list with empty strings

    threads = []

    if submit_button and prompt:
        for idx, model_name in enumerate(model_names):
            thread = threading.Thread(target=get_model_output_thread, args=(prompt, model_name, outputs, idx))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

    # Display text areas and fill with outputs if available
    for idx, model_name in enumerate(model_names):
        with cols[idx]:
            st.text_area(label=f"{model_name}", value=outputs[idx], height=300, key=f"output_{model_name}_{idx}")  # Use a unique key

if __name__ == "__main__":
    main()
