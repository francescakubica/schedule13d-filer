import streamlit as st
from openai import OpenAI
import processor
#  streamlit run frontend.py
    

# Configure the page
st.set_page_config(
    page_title="Transactions DataEntry Filer",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for API key and validation status
if "api_key" not in st.session_state:
    st.session_state.api_key = ""
if "api_key_validated" not in st.session_state:
    st.session_state.api_key_validated = None  # None means no validation yet

# Sidebar Input for OpenAI API Key
st.sidebar.text_input(
    "OpenAI API Key",
    value=st.session_state.api_key,  # Keep the previous value if entered
    type="password",
    key="api_key_input"
)

# Validate API Key Button
if st.sidebar.button("Validate API Key"):
    st.session_state.api_key = st.session_state.api_key_input  # Update the session state
    if processor.is_valid_api_key(st.session_state.api_key):
        st.session_state.api_key_validated = True
        st.sidebar.success("API key is valid!")
    else:
        print('the api key printed', st.session_state.api_key)
        st.session_state.api_key_validated = False
        st.sidebar.error("Invalid API key. Please try again.")

# Handle Clearing the Input on Invalid Key
if st.session_state.api_key_validated is False:
    st.session_state.api_key = ""  # Clear the session state for re-entry



client = OpenAI(api_key=st.session_state.api_key) # Client
# Sidebar navigation
st.sidebar.title("📚 Navigation")
nav_option = st.sidebar.radio("Go to:", ["🏠 Data Entry", "ℹ️ About"])

# Main Page / Data Entry
if nav_option == "🏠 Data Entry":
    st.header("Automatic Data Entry Filer")

    # Collect user input from uploaded txt files 
    # test_string_array 
    uploaded_files = st.file_uploader(
        "Upload your text files",
        type = "txt",
        accept_multiple_files=True
    )
    # I want it to stop here : Challenge: runs everytime without stopping
    # Create a button that says "submit"
    submit_button = st.button("Submit")

    if submit_button:

        # They want to continue
        if uploaded_files: # Non empty

            text_string_list = []
            # Debugging: Check if the files are uploaded
            
            for uploaded_file in uploaded_files:
                # Read the content of each file
                file_content = uploaded_file.read().decode("utf-8")  # Decode to string
                text_string_list.append(file_content)

            # With those uploaded files, call the run_pipeline function to analyze  
            st.write("Running the pipeline...")
            transactionsDF = processor.run_pipeline(text_string_list, client) 

            # Then, make the user able to download the csv file 
            csv = transactionsDF.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="Download Processed Data as CSV",
                data=csv,
                file_name="processed_data.csv",
                mime="text/csv"
            )
        else:
            st.write("Upload a text file to get started.")
    else:
        st.error("No files uploaded. Please upload text files before clicking Submit.")



elif nav_option == "ℹ️ About":
    st.header("About")
    st.write("This is a Streamlit app that uses OpenAI's GPT-4o-mini to automatically extract data from text files.")

    st.subheader("How to Use")
    st.write(
        "1. Enter your OpenAI API Key in the sidebar.\n"
        "2. Go to the Data Entry page and upload a text file.\n"
        "3. The app will automatically extract data from the text file and display it in a table.\n"
        "4. You can then download the extracted data as a CSV file."
    )

    st.subheader("About OpenAI")
    st.write(
        "OpenAI is an artificial intelligence research lab consisting of the for-profit OpenAI LP and the non-profit OpenAI Inc.\n"
        "The company aims to ensure that artificial general intelligence benefits all of humanity."
    )

    st.subheader("About Streamlit")
    st.write(
        "Streamlit is an open-source Python library that makes it easy to create web apps for machine learning and data science."
    )

    st.subheader("About the Developer")
    st.write(
        "This app was developed by Francesca Kubica.\n"
        "You can find the source code on GitHub"
    )
else:
    st.subheader("🚫 Apologizes there was an error loading your files")


