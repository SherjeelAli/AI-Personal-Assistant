from flask import Flask, render_template, url_for, request, jsonify, redirect
import os
import requests
from dotenv import load_dotenv
from google import genai


load_dotenv()
api_key = os.getenv("API_KEY")

app = Flask(__name__)
client = genai.Client(api_key=api_key)  # <-- API key goes HERE



@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/ask", methods=["POST"])
def ask():

    question = request.form.get("question")

    if not question:
        return "Please ask a question.", 400

    try:
        interaction = client.interactions.create(
            model="gemini-3.6-flash",           
            
            system_instruction="Act like a helpful personal assistant",
            
            input=question,
            
            generation_config={
                "temperature": 0.7,             
                "max_output_tokens": 512,       
            }
        )
        
        return interaction.output_text.strip()
        
    except Exception as e:
        return f"Error: {str(e)}", 500



if __name__ == "__main__":
    app.run(debug=True)
