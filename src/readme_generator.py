class ReadmeGenerator:
    def __init__(self, repo_data, gemini_api):
        self.repo_data = repo_data
        self.gemini_api = gemini_api

    def create_readme(self):
        prompt = self.build_prompt()
        generated_content = self.gemini_api.generate_text(prompt)
        return generated_content['choices'][0]['text']

    def build_prompt(self):
        repo_name = self.repo_data.get("name", "Unnamed Repo")
        description = self.repo_data.get("description", "No description available.")
        language = self.repo_data.get("language", "No language specified.")

        prompt = f"Generate a GitHub README for the repository '{repo_name}'. "
        prompt += f"The description is: '{description}'. "
        prompt += f"The primary language is {language}. Include sections like installation, usage, and contribution. "
        prompt += "Add suitable emojis where appropriate."
        return prompt
