import streamlit as st
import os
import google.generativeai as genai
from github_scraper import GitHubScraper  # Assuming you have this module
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
# Configure Generative AI
genai.configure(api_key=os.environ["API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")

def generate_readme(repo_url):
    # Initialize GitHubScraper with your GitHub token
    github_token = os.environ["GITHUB_API_TOKEN"]
    github_scraper = GitHubScraper(github_token)
    
    # Fetch repository details
    get_repo_details = github_scraper.get_repo_details(repo_url)
    
    # Extract repository information
    repo_name = get_repo_details.get('name', 'Unknown Repo')
    repo_description = get_repo_details.get('description', 'No description available.')
    repo_url = get_repo_details.get('html_url', 'No URL available.')

    # Create a prompt for the AI model
    prompt = f"""
    # {repo_name} 🎨
    
    ## Description 📜
    {repo_description}
    
    ## Repository URL 🌐
    [Link to Repository]({repo_url})
    
    ## Features 🚀
    - Feature 1
    - Feature 2
    - Feature 3
    
    ## Installation 🛠️
    ```bash
    # Installation commands
    ```
    
    ## Usage 📖
    ```python
    # Usage examples
    ```
    
    ## Contributing 🤝
    Contributions are welcome! Please refer to [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.
    
    ## License 📜
    This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
    """
    
    # Generate README content
    response = model.generate_content(prompt)
    readme_content = response.text
    
    return readme_content

# Streamlit app
st.title("GitHub README Generator ✨")

# Input field for GitHub repository URL
repo_url = st.text_input("Enter GitHub Repository URL:", "")

# Add a search button to trigger README generation
if st.button("Search and Generate README"):
    if repo_url:
        try:
            readme_content = generate_readme(repo_url)

            # Two-column layout for generated README and preview
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Generated README Text ✍️")
                st.text_area("Generated README", value=readme_content, height=400)
                st.download_button("Download README.md", readme_content, file_name="README.md")

            with col2:
                st.subheader("README Preview 👀")
                st.markdown(readme_content)
                
        except Exception as e:
            st.error(f"Error fetching repository data: {e}")
    else:
        st.warning("Please enter a valid GitHub repository URL")

# Apply padding between the two columns
st.markdown(
    """
    <style>
    div[data-testid="stHorizontalBlock"] > div {
        padding: 0 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)