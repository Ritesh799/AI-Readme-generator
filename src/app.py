import streamlit as st
import os
import google.generativeai as genai
from github_scraper import GitHubScraper  # Assuming you have this module
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
# Configure Google Gemini API key
genai.configure(api_key=os.getenv("API_KEY"))

# App Title
st.set_page_config(page_title="GitHub README Generator 📝✨", layout="wide")
st.title("GitHub README Generator 📝✨")

# Sidebar input for GitHub repo URL
st.sidebar.header("Enter the GitHub Repo URL")
repo_url = st.sidebar.text_input("GitHub Repo URL", placeholder="https://github.com/user/repo")

# Function to add Copy to Clipboard functionality using JS
def add_copy_to_clipboard_js(content):
    # Encode the content to be safely included in JS
    encoded_content = content.replace("\n", "\\n").replace("'", "\\'")
    copy_js = f"""
    <script>
        function copyToClipboard() {{
            var text = `{encoded_content}`;
            navigator.clipboard.writeText(text).then(function() {{
                // Display success message
                document.getElementById('copy-status').innerText = 'Copied to clipboard!';
                document.getElementById('copy-status').style.color = 'green';
            }}, function(err) {{
                // Display error message
                document.getElementById('copy-status').innerText = 'Failed to copy text: ' + err;
                document.getElementById('copy-status').style.color = 'red';
            }});
        }}
    </script>
    <button onclick="copyToClipboard()" style="
        background: linear-gradient(90deg, #4f9d9d, #2b6a6a);
        border: none;
        color: white;
        font-weight: bold;
        padding: 12px 24px;
        border-radius: 8px;
        cursor: pointer;
        transition: background 0.3s;
    ">📋 Copy to Clipboard</button>
    <p id="copy-status" style="margin-top: 8px; font-weight: bold;"></p>
    """
    return copy_js

# Button to generate the README
if st.sidebar.button("Generate README"):
    if repo_url:
        st.sidebar.write("Generating README... ✨")
        
        # Dummy prompt for Google Gemini API request based on GitHub URL
        prompt = f"Generate a README for the GitHub repository located at {repo_url}. Include installation instructions, usage, and a description."
        
        # Fetch README content using Google Gemini
        try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(prompt)
            readme_content = response.text
        except Exception as e:
            readme_content = "Error generating README: " + str(e)
        
        # Store the generated README content
        st.session_state['readme_content'] = readme_content
    else:
        st.sidebar.error("Please enter a valid GitHub repository URL.")

# Two-column layout: Generated README and Preview
if 'readme_content' in st.session_state:
    col1, col2 = st.columns(2)

    # Column 1: Generated README text
    with col1:
        st.subheader("Generated README Content 📝")
        st.text_area("Generated README", value=st.session_state['readme_content'], height=500)

        # Buttons below the generated README
        col1_1, col1_2 = st.columns(2)

        # Copy to Clipboard button (using JS)
        with col1_1:
            copy_js = add_copy_to_clipboard_js(st.session_state['readme_content'])
            st.markdown(copy_js, unsafe_allow_html=True)

        # Download README.md button
        with col1_2:
            readme_filename = "README.md"
            st.download_button(
                label="💾 Download README.md",
                data=st.session_state['readme_content'],
                file_name=readme_filename,
                mime="text/markdown",
                help="Click to download the README.md file."
            )

    # Column 2: README Preview
    with col2:
        st.subheader("README Preview 📄")
        st.markdown(st.session_state['readme_content'])

# Instructions for users
st.sidebar.markdown("### Instructions 📝")
st.sidebar.markdown("""
1. Enter the GitHub repository URL.
2. Click 'Generate README' to fetch the content.
3. Review the generated README in the preview.
4. Use the buttons below the generated README to copy or download it.
""")
