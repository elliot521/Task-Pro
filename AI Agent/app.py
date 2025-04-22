from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os
from dotenv import load_dotenv

# 加载 .env 中的 API Key
load_dotenv()

# 初始化 Flask 应用
app = Flask(__name__)
CORS(app)  # 允许跨域访问

# 设置 OpenAI API Key
client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com")

@app.route('/optimize', methods=['POST'])
def optimize():
    try:
        data = request.get_json()
        user_input = data.get('text', '')

        prompt = f"请根据优先级优化以下待办事项：\n{user_input}"

        response = client.chat.completions.create(
            model="deepseek-chat",  # 使用 DeepSeek 的对话模型
            messages=[{"role": "user", "content": prompt}]
        )

        optimized_text = response.choices[0].message['content'].strip()
        return jsonify({"result": optimized_text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 启动应用
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
