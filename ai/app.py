from flask import Flask, request, jsonify
import openai
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Create client lazily
def get_client():
    return openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

@app.route('/review', methods=['POST'])
def review_code():
    code = request.data.decode('utf-8')
    client = get_client()
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a code review assistant. Analyze the provided code and provide detailed feedback including time complexity, space complexity, potential bugs, and suggestions for improvement."},
                {"role": "user", "content": f"Review this code:\n\n{code}"}
            ],
            max_tokens=500,
            temperature=0.5
        )
        feedback = response.choices[0].message.content.strip()
    except openai.RateLimitError as e:
        feedback = "AI Review (Demo Mode - Quota Exceeded):\n\nTime Complexity: O(n)\nSpace Complexity: O(1)\nSuggestions:\n- Consider optimizing loops.\n- Add error handling.\n- Improve code readability with comments.\n\nPlease check your OpenAI billing or use a valid API key for full AI reviews."
    except Exception as e:
        feedback = f"Error in AI review: {str(e)}"
    return jsonify({"feedback": feedback})

if __name__ == '__main__':
    app.run(port=5001)