"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Eli the Computer Guy - Intro to AI LLM Systems with Ollama and Python
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

# Import relevant Ollama modules
from ollama import chat
from ollama import ChatResponse

# Beautiful soup is a custom class within bs4 module that allows you to scrape text from a webpage
# and format it so it is easier to read for the user. For example, you can parse through the html 
# text and only include text included within <p> tags (paragraphs)
from bs4 import BeautifulSoup

# Requests is a library for making HTTP requests in Python to websites and APIs
# with Requests you can make GET and POST API requests to retrieve data from websites and APIs, or send data to them.
import requests

# Bottle is a small Python framework to build web applications and APIs
from bottle import run, route, post, request

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

#lesson_7()

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                    Lesson 8 - Bottle Web App
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def lesson_8():

    # Define injection
    injection = "Reply in comedic style. Reply in no more than 60 words"

    # Function to get a response from the LLM (gemma3, 1 Billion connections)
    def get_response(query):
        response: ChatResponse = chat(model="gemma3:1b", messages=[
            {
            "role": "user",
            "content": query,
            },
        ]) 

        # Return the response in readable format
        return response.message.content

    '''
     @route is a decorator for the index function
     @route is a specific decorator from the 'Bottle' module

     In this context the '/' path means the URL PATH to send API calls to
     As we are hosting on 'http://localhost:8080/' the PATH in this case is '/'

     So whenever someone opens this web app, the function 'def index()' is run
     The method tells the function what API calls will be needed on this webpage
     ''' 

    # Think of this decorator as a label saying 'This function (index) will handle all URL requests to this PATH'
    @route('/', method=['GET','POST'])
    # index is a function that can handle both GET API requests (obtaining user input)
    # and POST API requests (displaying the LLM ouptut on the webpage)
    def index():
        # GET API request to get data from user once button (form) is pressed
        query = request.forms.get('query')

        # Intject into the query
        full_query = f"""This is my injection: {injection}
                    This is my query: {query}"""
        ollama_response = get_response(full_query)

        # Simple HTML web page
        # POST API used to display the LLM answer on the web pagee
        page = f"""
                    <h1>Robbie's first web app</h1>
                    <form action="/" method="post">
                        Please Enter your Prompt: <input type="text" name="query">
                        <br>
                        <input type="submit">
                    </form>
                    <strong>{query}</strong><br>
                    {ollama_response}
                    """
    
        return page

    # Port 8080 is an alternative HTTP port on a machine. A network port is a purley software concept
    # It indicates where the OS sends incoming data once it has been received on the network card
    # Only one program can 'listen' to a port at a time

    # Local host can also be 127.0.0.1, which loops back to your own machine
    run(host='localhost', port=8080)

    return 0

# lesson_8()

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                    Lesson 9 - AutoBlog
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def lesson_9():

    # Passing the blog text to gemma3 via ollama class to provide an output from the LLM
    def ai_post(blog_text):
        response: ChatResponse = chat(model='gemma3:1b', messages=[
            {
                'role': 'user',
                'content': f'Rewrite this in under 500 words: {blog_text}.',
            },
        ])
        return response.message.content

    # Function to come up with a new title for the blog
    def ai_title(post):
        response: ChatResponse = chat(model='gemma3:1b', messages=[
            {
                'role': 'user',
                'content': f"""
                                Provide a title for this blog post: {post}
                                Make it funny
                                Make it under 12 words
                                ONLY GIVE ME ONE, NOT MULTIPLE OPTIONS
                            """
            },
        ])
        return response.message.content

    # Function to scrape the chosen url using BeautifulSoup and format for readability
    def scrape(url):
        page = requests.get(url).text
        soup = BeautifulSoup(page, "html.parser")
        paragraphs = soup.find_all("p")
        page_text = ""
        for line in paragraphs:
            page_text += line.text

        return page_text

    # Index function to call all other functions when html address is run
    # @route Bottle decorator says whenever this html is called it may require a GET or POST API call
    # Automatically routes this so we don't have to do this manually
    @route('/', method=['GET','POST'])
    def index():
        url = request.forms.get('url')
        if url:
            blog_text = scrape(url)
            post = ai_post(blog_text)
            title = ai_title(post)
            with open('RobbiesBlog.html', 'a') as f:
                f.write(f"<h1>{title}<h1>")
                f.write(f"{post}<hr>")
        else:
            print("URL LINK FAILED")
            url = ""
            title = ""
            blog_text = ""
            post = ""

        # Simple HTML page for the data
        page = f"""
                    <h1>Robbies Blog Copier</h1>
                    <form action='/' method='post'>
                        URL: <input type='text' name='url'>
                        <input type='submit'>
                    </form>
                    <h3>URL:</h3> {url}<br>
                    <h3>Title:</h3> {title}<br>
                    <h3>New Post:</h3> {post}<br>
                    <h3>Original Post:</h3> {blog_text}<br>
                """
        return page

    run(host="127.0.0.1", port="8080")

    return 0

lesson_9()