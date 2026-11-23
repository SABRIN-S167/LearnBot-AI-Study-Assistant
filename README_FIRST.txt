LEARNBOT — QUICK START (WINDOWS)
=================================

WHAT IS INCLUDED?
- app.py: the LearnBot application
- requirements.txt: packages the app needs
- START_LEARNBOT.bat: one-click setup and launcher
- This guide

FASTEST WAY TO RUN
1. Extract the entire ZIP file to a normal folder, for example Desktop\LearnBot.
2. Make sure Python 3.10 or newer is installed.
   Download: https://www.python.org/downloads/
   During installation, tick "Add Python to PATH" if that option appears.
3. Open the extracted LearnBot folder.
4. Double-click START_LEARNBOT.bat.
5. The first launch installs packages and may take a few minutes. Keep the black
   command window open. Streamlit should open LearnBot in your browser.
6. If the browser does not open automatically, look in the command window for
   a Local URL such as http://localhost:8501 and open it yourself.

TRY IT IN DEMO MODE
- No API key is needed to open the app.
- Open Ask & Explain and try: "What is an algorithm?"
- Try Summarize Notes by pasting a paragraph.
- Try Create a Quiz by pasting a few lines of notes.
NOTE: Demo mode uses sample/basic logic. It is for checking that the app runs,
not a full AI service.

ENABLE REAL GEMINI AI (OPTIONAL)
1. Visit https://aistudio.google.com/app/apikey
2. Sign in and create an API key.
3. Copy the key privately.
4. In LearnBot's left sidebar, paste it into "Gemini API key".
5. Choose a model and use the tools. Your key is used for this app session.
Do NOT send your key to anyone or upload it to GitHub.
Google may apply usage limits or billing depending on the account, model and
current API terms. Check Google AI Studio before using paid services.

STOP THE APP
- Return to the black command window and press Ctrl+C.
- Close the browser tab.

TROUBLESHOOTING
- "'python' is not recognized": install Python and enable Add Python to PATH.
- Browser did not open: manually visit http://localhost:8501.
- Port 8501 busy: close another Streamlit app or restart the PC.
- Package installation failed: check internet, then double-click the BAT file again.
- AI request failed: check the API key, internet, selected model and Google AI Studio limits.
- Do not delete the .venv folder while LearnBot is running.

IMPORTANT
- Extract the ZIP before running. Do not try to run the BAT file from inside the ZIP preview.
- This is a local student project. It is not a medical, legal or professional advice tool.
- Verify exam answers with your official notes and textbooks.
