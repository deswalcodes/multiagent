from flask import Flask, request, jsonify
from agents.support_agent import support_agent
from agents.dashboard_agent import dashboard_agent
from deep_translator import GoogleTranslator
from langdetect import detect

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False  

support_executor = support_agent()
dashboard_executor = dashboard_agent()

@app.route("/")
def home():
    return "✅ Multi-Agent Assignment Server is running!"

@app.route("/support", methods=["POST"])
def support_route():
    user_input = request.json.get("query")
    if not user_input:
        return jsonify({"error": "query required"}), 400
    
    detected_lang = detect(user_input)
    
    # translate to English if the input is not English
    if detected_lang != "en":
        translated_input = GoogleTranslator(source="auto", target="en").translate(user_input)
    else:
        translated_input = user_input

    # invoke agent with translated input
    result = support_executor.invoke({"input": translated_input})

    # always return agent's response in English
    return jsonify({"response": result["output"]})


@app.route("/dashboard", methods=["POST"])
def dashboard_route():
    user_input = request.json.get("query")
    if not user_input:
        return jsonify({"error": "query required"}), 400
    
    detected_lang = detect(user_input)
    
    if detected_lang != "en":
        translated_input = GoogleTranslator(source="auto", target="en").translate(user_input)
    else:
        translated_input = user_input

    # call the dashboard agent
    result = dashboard_executor.invoke({"input": translated_input})

    # always return agent's response in English
    return jsonify({"response": result["output"]})


if __name__ == "__main__":
    app.run(debug=True)
