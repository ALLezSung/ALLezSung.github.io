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
        "frequency_penalty": 0.5,
        "stream": True
    }
    
    response = requests.post(BASE_URL, json=payload, headers=headers, stream=True)
    thinking_seq = []
    responing_seq = []
    if response.status_code == 200:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                decoded_chunk = chunk.decode('utf-8')
                decoded_chunk = decoded_chunk.strip('data:')
                try:
                    json_chunk = json.loads(decoded_chunk)
                except:
                    break
                thinking = json_chunk['choices'][0]['delta']['reasoning_content']
                responing = json_chunk['choices'][0]['delta']['content']
                if thinking:
                    thinking_seq.append(thinking)
                if responing:
                    responing_seq.append(responing)
    else:
        return jsonify({'error': 'Request failed with status code: ' + str(response.status_code)})

    return jsonify({'thinking': thinking_seq, 'responing': responing_seq})

if __name__ == '__main__':
    app.run(debug=True)