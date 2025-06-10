import google.generativeai as genai
from flask_app import app

def get_bot_reply(message):
    """Generates and returns a response from the chatbot."""
    genai.configure(api_key=app.config['GOOGLE_API_KEY'])
    print(app.config['GOOGLE_API_KEY'])
    model = genai.GenerativeModel('models/gemini-2.0-flash')
    for m in genai.list_models():
        print(m.name, m.supported_generation_methods)
    try:
        response = model.generate_content(f"Please provide a helpful message about how to use this calendar app for this question: [question start] {message}. [question end] If this question is not related to the calendar app, please respond with 'I don't know'. Do not add markdown formatting to your response.") # TODO: Make this more specific to the calendar app
        bot_reply = response.text.strip()
    except Exception as e:
        print(e)
        bot_reply = "Sorry, I couldn't process your request."
    return bot_reply