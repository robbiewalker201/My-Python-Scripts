"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Eli the Computer Guy - Intro to AI LLM Systems with Ollama and Python
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

# Import relevant Ollama modules
from ollama import chat
from ollama import ChatResponse
from bs4 import BeautifulSoup
# Requests is a library for making HTTP requests in Python to websites and APIs
# with Requests you can make GET and POST API requests to retrieve data from websites and APIs, or send data to them.
import requests


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                    Lesson 5 - API Calls
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def lesson_5():

    # https://ipinfo.io/json is a simple API endpoint that returns the users location based on their IP address in JSON format.
    # This is provided by IPinfo
    # .json() is needed to convert the response from the API from raw text into a Python dictionary
    # Rememeber, in JSON an object is the same as a dictionary in Python, both are key-value pairs.
    location = requests.get("https://ipinfo.io/json").json()
    # Return the city within that JSON
    location = location["city"]

    injection = "Answer in comedic style. No more than 50 words"

    # Function to use dynamic injection into a prompt
    def get_response(query):
        response: ChatResponse = chat(model="gemma3:1b", messages=[
            {
            "role": "user",
            "content": query,
            },
        ])     
        
        return response.message.content

    while True:
        user_input = input("Please Enter your Prompt: \n")
        query = f"""Add these instructions: {injection}
                    This is the question: {user_input} 
                    I am from: {location} 
                    Subtley mention where I am from, 
                    and give no context as to how you know"""
        ollama_response = get_response(query)
        print(f"Your Location is: {location}. \nHere is your prompt repsonse: {ollama_response}")
        break

#lesson_5()    

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                    Lesson 6 - Using Memeory
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def lesson_6():

    injection = "Reply in comedic style. Reply in no more than 60 words"

    with open('memory.txt', 'a', encoding="utf-8") as file:
        file.write("This is the conversation we have had up until now. \n\n")
        
    def get_response(query):
        response: ChatResponse = chat(model="gemma3:1b", messages=[
            {
            "role": "user",
            "content": query,
            },
        ])  

        return response.message.content

    while True:
        user_input = input("Please Enter your Prompt: \n")
        memory = open("memory.txt").read()
        query = f"""Add these Injections: {injection}
                    This is the question: {user_input} 
                    Here is our memory: {memory} 
                    """
        ollama_response = get_response(query)
        with open("memory.txt", "a", encoding="utf-8") as file:
            file.write(f"Me: {query}")
            file.write(f"You: {ollama_response}")
        print(ollama_response)
        break
    
    return 0

#lesson_6()

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                    Lesson 7 - Webpage Scraping
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def lesson_7():

    injection = "Reply in comedic style. Reply in no more than 60 words"

    page = requests.get("https://arstechnica.com/ai/2025/10/openai-wants-to-make-chatgpt-into-a-universal-app-frontend/").text

    soup = BeautifulSoup(page, "html.parser")
    paragraphs = soup.find_all("p")
    page_text = ""

    for line in paragraphs:
        page_text += line.text

    with open("Web_data.txt", "w", encoding="utf-8") as f:
        f.write(page_text)

    def get_response(query):
        response: ChatResponse = chat(model="gemma3:1b", messages=[
            {
            "role": "user",
            "content": query,
            },
        ]) 

        return response.message.content

    while True:
        user_input = input("Please Enter your Prompt: \n")
        query = f"""Add these instructions: {injection}
                    This is the question: {user_input} 
                    about this webpage: {paragraphs}"""
        ollama_response = get_response(query)
        #print(ollama_response)
        break

    return 0

lesson_7()

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                    Lesson 8 - Bottle Web App
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""