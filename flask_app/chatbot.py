import google.generativeai as genai
from flask_app import app
import datetime

def get_bot_reply(message):
    """Generates and returns a response from the chatbot."""
    genai.configure(api_key=app.config['GOOGLE_API_KEY'])
    print(app.config['GOOGLE_API_KEY'])
    model = genai.GenerativeModel('models/gemini-2.0-flash')
    try:
        response = model.generate_content(f"Please provide a helpful message about how to use this calendar app for this question: [question start] {message}. [question end] If this question is not related to the calendar app, please respond with the message 'Please ask a question relating to this calendar app'. Do not add markdown formatting to your response. Here is a description of my application. It is a calendar app, with additional features. Once logged in, there is a navigation bar at the top, which has links to the Calendar, Analysis, Chatbot, Settings pages, and a Logout button. Firstly, let's look at the calendar page. The calendar allows for month/week/day views, and you can navigate between these views using buttons at the top-right of the calendar page, and you can also navigate to the day view of a specific date, by clicking on the day numbers in the month view, or by clicking on the day headings in the week view. You can add events through using the 'Add new event' form at the bottom of the calendar page, which lets you choose event's name, start date and time. You can click on the mini-calendar icon on the inputs for start/end date and time, to access a calendar widget that can be used to easily input times. You may delete events by clicking on them on the calendar, which may either reuslt in a confirmation prompt or the immediate deletion of your event depending on the user's 'Require confirmation when deleting events' setting. You may also delete all events on the calendar by navigating to the settings page, where there is a button to delete all events. There is automated event addition feature on the calendar page below the event addition form, which involves a prompt for how the event will be created, and a submission box. The AI will then automatically insert an event into the calendar. On the Analysis page, there is a button called 'Productivity analysis' - once pressed, the AI will give an analysis of your productivity and ways it can be improved. On the Chatbot page, the user can ask the chatbot questions relating to the calendar app, through a form. The page consists of a box where the user's questions and the chatbot responses are displayed, which can be scrolled up and down to access previous/newer responses. To submit a question, type it into the input form below this box, and either press enter or the 'Submit' button to ask the chatbot a question. Note that it will take a few seconds for the chatbot response to be generated, and for the page to refresh - hence the user's input form will not clear immediately after submission. On the Settings page, the user is able to change the configurations of their account, and delete all events. They can update the 'Require confirmation when deleting events' by clicking the checkbox next to the option to modify their setting, then clicking 'Save Settings' to save their choice. The user may also change their password with the form below this: they must enter their old password, and their new password twice, and this new password must follow the same password rules of: at least 8 characters, and needs at least one lowercase letter, one uppercase letter, one number and one special character. They may also click the red 'Delete all events' button in the 'Danger Zone' section of the settings to delete all events: this will require a confirmation prompt to proceed. To log out of your account, click the Logout button on the top-right - this will redirect the user to the login page. A new account can be created from the Signup page, where an email, username, and password will need to be specified. The password needs at least 8 characters, and needs at least one lowercase letter, one uppercase letter, one number and one special character. The login page requires you to enter your username and password, which can be used to login. You can navigate between the login/signup pages through clicking the link at the bottom of their respective forms.")
        bot_reply = response.text.strip()
    except Exception as e:
        print(e)
        bot_reply = "Sorry, I couldn't process your request."
    return bot_reply

def get_ai_event_string(prompt):
    """Generates an event string from the AI based on the user's prompt."""
    genai.configure(api_key=app.config['GOOGLE_API_KEY'])
    model = genai.GenerativeModel('models/gemini-2.0-flash')
    try:
        response = model.generate_content(f"Please try to generate a calendar event string based on this description here: [event description start] {prompt} [event description end]. The format should be 'Title | Start Time | End Time', where Start Time and End Time are in ISO 8601 format (e.g., 2025-07-23T10:00), without any additional text or formatting. The date today is {datetime.datetime.now()} - make sure the event occurs soon after the time right now. If the user's message is too unspecific (for example gibberish like 'a'), please respond with the exact message 'Could not generate event string.'. Only respond with one of these two things.")
        ai_event_str = response.text.strip()
    except Exception as e:
        print(e)
        ai_event_str = "Could not generate event string."
    return ai_event_str

def get_productivity_analysis(events):
    """Generates a productivity analysis from the AI based on user's events."""
    genai.configure(api_key=app.config['GOOGLE_API_KEY'])
    model = genai.GenerativeModel('models/gemini-2.0-flash')
    # Format events for prompt
    event_list = '\n'.join([
        f"Title: {e.title}, Start: {e.start_time}, End: {e.end_time}" for e in events
    ])
    prompt = (
        "Here is a list of calendar events for a user. Please analyze their productivity, "
        "give insights, and suggest improvements. Only respond with your analysis, no markdown or formatting. "
        "If the list is empty, say 'No events found.'\n\nEvents:\n" + event_list
    )
    try:
        response = model.generate_content(prompt)
        analysis = response.text.strip()
    except Exception as e:
        print(e)
        analysis = "Sorry, I couldn't process your request."
    return analysis