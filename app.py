from flask import Flask, request, jsonify, render_template
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import spacy

app = Flask(__name__)

# Load NLP model and FAQ data
nlp = spacy.load("en_core_web_sm")

# Preempted answers dictionary
preempted_answers = {
    "hello": "Hi there! How are you?",
    "hi": "Hey! What can I help you with today?",
    "how are you": "I'm just a bunch of code, but I'm ready to help you! How are you doing?",
    "what questions can i ask you": "Here are some questions you can ask me: \n1. What are your office hours? \n2. How can I make an appointment? \n3. Where is the library? \n4. What courses are available? \n5. How can I get help with my academic advising? \n6. What is the student portal used for? \n7. How do I contact my academic advisor? \n8. What should I do if I miss a class? \n9. How can I check my grades? \n10. What extracurricular activities are available?",
    "what is your name": "I’m PAL Bot! You can call me PAL. How can I help you today?",
    "what is your purpose": "I’m here to help you with academic advice, resources, and anything else you need. Let’s get learning!",
    "help": "I’m all ears! You can ask me about classes, assignments, tutoring, or anything else related to school.",
    "goodbye": "Goodbye! It was a pleasure helping you. Don’t hesitate to reach out if you need anything else.",
    "how do I register for classes": "To register for classes, log in to your student portal and follow the registration guide. If you need help, I can walk you through it.",
    "how do I check my grades": "You can check your grades through the student portal or learning management system, Log in to Sakai. Let me know if you need a hand navigating it.",
    "where can I find course materials": "Course materials are usually available through your course's LMS. If you're having trouble accessing them, let me know and I can guide you.",
    "how can I contact a professor": "You can email your professor using the contact information in the course syllabus. Want tips on how to write an email? I can help!",
    "how do I get a tutor": "To get a tutor, head to the tutoring center’s website or ask your advisor about peer tutoring options. I can help you find the right contact.",
    "what is the policy for late assignments": "The late assignment policy varies by professor. It’s best to check your syllabus or ask your instructor directly. Need help with an assignment?",
    "what resources are available for academic support": "There are tutoring services, writing centers, study groups, and even workshops. Let me know what you need help with, and I can point you to the right resource.",
    "how do I apply for a scholarship": "To apply for scholarships, visit the financial aid office or check the student portal for opportunities. I can also help you find deadlines.",
    "what extracurricular activities are available": "There are clubs, sports teams, volunteer opportunities, and more! Let me know your interests, and I can suggest some activities you might enjoy.",
    "what is the grading scale": "The grading scale typically follows a standard format like A (90-100%), B (80-89%), etc. Check with your course syllabus for specifics.",
    "how do I drop a class": "To drop a class, log in to your student portal and follow the drop process. You can also reach out to your academic advisor if you need help.",
    "how can I access library resources": "You can access library resources online or in person. Check the library’s website for e-books, articles, and other materials. Let me know if you need help.",
    "what are the requirements for graduation": "Check your degree audit or ask your advisor to go over the graduation requirements. Each program has specific criteria, like course credits and GPA.",
    "how do I set up my student email account": "You can set up your student email by visiting the IT services portal. If you run into any issues, I can guide you step by step.",
    "how do I submit my final project": "Final project submission varies by course. Check the assignment guidelines on your LMS, or ask your professor directly. Need help with the project itself? I’ve got your back.",
    "what are office hours for academic advising": "Office hours for academic advising can be found on the advising website or by emailing your advisor. Need help scheduling an appointment?",
    "what are the general education requirements": "The general education requirements can be found in the student handbook or on the registrar's website. I can help you find that info if you need it."
}

# Load FAQ data and process it for cosine similarity
with open("C:/Users/odegb/OneDrive/Documents/Visual Studio 2022/venv/Lib/faq.json") as f:
    faq_data = json.load(f)

questions = list(faq_data.keys())
tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(questions)

# Mental health keywords to filter
mental_health_keywords = ["depressed", "anxious", "mental health", "counseling"]

def check_for_mental_health(query):
    return any(word in query.lower() for word in mental_health_keywords)

def get_response(user_query):
    user_vec = tfidf_vectorizer.transform([user_query])
    similarities = cosine_similarity(user_vec, tfidf_matrix).flatten()
    closest_match = similarities.argmax()
    if similarities[closest_match] > 0.3:
        return faq_data[questions[closest_match]]
    return "I'm here for academic help. For other support, please contact the relevant services."

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/chat", methods=["POST"])
def chat():
    user_query = request.json["query"].lower()

    # Check if the query matches any of the preempted answers
    if user_query in preempted_answers:
        response = preempted_answers[user_query]
    else:
        if check_for_mental_health(user_query):
            response = "For mental health support, please reach out to counseling services."
        else:
            response = get_response(user_query)

    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)