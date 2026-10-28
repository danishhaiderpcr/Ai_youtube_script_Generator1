AI YouTube Script Generator
A beginner-friendly web app built with Python, Streamlit, and the Google Gemini API. Enter a topic, channel niche, and target audience to generate YouTube title ideas, opening hooks, a video script, a description, hashtags, thumbnail concepts, and calls to action.
Features
- Accepts a video topic, channel niche, and target audience.
- Supports several output languages, video lengths, and tones.
- Generates 5 title ideas and 3 opening hooks.
- Creates an original draft script with optional visual cues.
- Generates a description, hashtags, thumbnail concepts, and calls to action.
- Downloads the generated content as a .txt file.
- Validates required inputs and handles missing keys and API errors.
- Keeps the API key outside the source code.
Project files
ai-youtube-script-generator/
├── app.py
├── README.md
└── requirements.txt
Requirements
- Python 3.10 or newer (Python 3.11 or 3.12 recommended).
- A Google Gemini API key with API access enabled.
- Internet access when generating content.
Run locally
1. Download or clone this repository.
2. Open a terminal in the project folder.
3. Create and activate a virtual environment (recommended).
   Windows PowerShell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   macOS/Linux
   python3 -m venv .venv
   source .venv/bin/activate
4. Install dependencies:
   python -m pip install -r requirements.txt
5. Get a Gemini API key from Google AI Studio.
6. Set the key as an environment variable.
   Windows PowerShell (current terminal only)
   $env:GEMINI_API_KEY="paste_your_key_here"
   macOS/Linux
   export GEMINI_API_KEY="paste_your_key_here"
7. Start the app:
   streamlit run app.py
Keep your API key private. Do not paste it into app.py, README.md, screenshots, or a public GitHub repository.
Alternative local secret configuration
You can also create .streamlit/secrets.toml locally:
GEMINI_API_KEY = "paste_your_key_here"
Do not commit this file. Add .streamlit/secrets.toml to .gitignore if you create it.
How to use the app
1. Enter a video topic, niche, and target audience.
2. Choose the output language, target duration, and tone in the sidebar.
3. Optionally add instructions such as “use simple English” or “include scene suggestions.”
4. Click Generate YouTube Content.
5. Review and edit the result, then download it as a text file.
Upload files to GitHub using the website UI
1. Sign in to GitHub.
2. Click New repository and give it a name, such as ai-youtube-script-generator.
3. Choose Public or Private, then click Create repository.
4. In the repository, choose Add file → Create new file.
5. Create app.py, paste the code, and commit the new file.
6. Repeat Add file → Create new file for README.md and requirements.txt.
7. Check that all three files appear in the repository root.
8. Never upload your API key or a populated secrets.toml file.
Deploy to Streamlit Community Cloud
1. Open Streamlit Community Cloud and sign in with GitHub.
2. Click Create app.
3. Select your GitHub repository, branch (usually main), and main file path app.py.
4. Open Advanced settings before deploying.
5. In the Secrets field, add:
   GEMINI_API_KEY = "paste_your_key_here"
6. Save the settings and click Deploy.
7. Wait for the app to build, then open the generated streamlit.app URL.
8. If deployment fails, open the app's logs and review the error.
Official guides:
- Deploy an app
- Secrets management
- Gemini API documentation
Troubleshooting
- API key not found: Check the GEMINI_API_KEY environment variable or Streamlit Secrets. Restart the app after changing local environment variables.
- Invalid API key / permission error: Confirm the key is correct and the Gemini API is enabled for the project.
- Model not found: The default is gemini-flash-latest. If that model alias is unavailable for your account, choose a supported Flash model from Google's current model documentation and enter its ID in the sidebar.
- Quota or rate-limit error: Check your Gemini API usage and quota, wait if needed, or try again later.
- Dependency/build error: Check the Streamlit Cloud logs and ensure requirements.txt is in the repository root.
- Empty response: Try again with a clearer topic or shorter additional instructions.
Privacy and content note
The topic and prompt are sent to Google's Gemini API to generate the requested output. Do not submit confidential or personal information. This app does not intentionally save generated content to a database; the current session retains the generated text for display and download.

Generated scripts may contain inaccurate claims or unsuitable suggestions. Fact-check the output, respect copyright, and review all content before publishing. AI-generated content cannot guarantee views, engagement, or monetization.
