from flask import Flask, request, jsonify
from flask_cors import CORS
from translate import translate_to_chinese
from image import get_image_for_word

app = Flask(__name__)
CORS(app)

@app.route('/translate', methods=['POST'])
def translate():
    data = request.get_json()
    english_text = data.get('text', '').strip()

    hanzi, pinyin = translate_to_chinese(english_text)
    image_url = get_image_for_word(english_text)

    return jsonify({
        'hanzi': hanzi,
        'pinyin': pinyin,
        'image': image_url
    })

if __name__ == '__main__':
    app.run(debug=True)