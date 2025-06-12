def get_bot_reply(message):
    """Generates and returns a response from the chatbot."""
    try:
        # Temporarily disabled Google Gemini integration for testing
        # import google.generativeai as genai
        # genai.configure(api_key=app.config['GOOGLE_API_KEY'])
        # model = genai.GenerativeModel('models/gemini-2.0-flash')
        # response = model.generate_content(f"Please provide a helpful message about how to use this calendar app for this question: [question start] {message}. [question end] If this question is not related to the calendar app, please respond with 'I don't know'. Do not add markdown formatting to your response.")
        # bot_reply = response.text.strip()
        
        # Simple echo response for testing form clearing
        bot_reply = f"I received your message: '{message}'. This is a test response to verify the form clears properly."
    except Exception as e:
        print(e)
        bot_reply = "Sorry, I couldn't process your request."
    return bot_reply