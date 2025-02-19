from flask import Flask, request, render_template, jsonify
import requests
import json

app = Flask(__name__)

BASE_URL = "https://api.siliconflow.cn/v1/chat/completions"
MODEL = "deepseek-ai/DeepSeek-R1-Distill-Llama-8B"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    content_seq = []
    thinking_seq = []
    responsing_seq = []

    api_key = request.json.get('api_key')
    content_seq = request.json.get('content_seq')

    headers = {
        "content-type": "application/json",
        "authorization": f"Bearer {api_key}"
    }
    
    payload = {
        "model": MODEL,
        "messages": content_seq,
        "max_tokens": 8192,
        "temperature": 0.6,
        "top_p": 0.7,
        "top_k": 50,
        "frequency_penalty": 0.5
    }
    
    response = requests.post(BASE_URL, json=payload, headers=headers)

    if response.status_code == 200:
        response_json = response.json()

        try:
            thinking = response_json['choices'][0]['message'].get('reasoning_content', "No reasoning")
            responsing = response_json['choices'][0]['message']['content']

            content_seq.append({"role": "assistant", "content": responsing})
            thinking_seq.append(thinking)
            responsing_seq.append(responsing)

            print(content_seq)
            
            return jsonify({'thinking': thinking, 'responsing': responsing})
        
        except KeyError:
            return jsonify({'error': 'Error processing response', 'response': response_json}), 400

    else:
        return jsonify({'error': 'Request failed with status code: ' + str(response.status_code)})


if __name__ == '__main__':
    app.run(debug=True)