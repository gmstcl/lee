from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/create', methods=['POST'])
def create_file():
    filename = request.json.get('filename')
    
    if not filename:
        return jsonify({"error": "파일명이 제공되지 않았습니다."}), 400
    
    folder = os.path.dirname(filename)
    if folder and not os.path.exists(folder):
        os.makedirs(folder)  # 폴더가 없으면 자동으로 생성
    
    # 파일이 이미 존재하면 새로 생성하지 않고, 기존 파일을 재사용하도록 수정
    if not os.path.exists(filename):
        with open(filename, 'w') as file:
            pass  # 빈 파일 생성
    
    return jsonify({"message": f"파일 '{filename}'이(가) 이미 존재하거나 새로 생성되었습니다."}), 200

# 파일 삭제 API
@app.route('/delete', methods=['POST'])
def delete_file():
    filename = request.json.get('filename')
    
    if not filename:
        return jsonify({"error": "파일명이 제공되지 않았습니다."}), 400
    
    if not os.path.exists(filename):
        return jsonify({"error": "파일이 존재하지 않습니다."}), 400
    
    os.remove(filename)
    
    return jsonify({"message": f"파일 '{filename}'이(가) 성공적으로 삭제되었습니다."}), 200

# 파일 읽기 API
@app.route('/read', methods=['POST'])
def read_file():
    filename = request.json.get('filename')
    
    if not filename:
        return jsonify({"error": "파일명이 제공되지 않았습니다."}), 400
    
    if not os.path.exists(filename):
        return jsonify({"error": "파일이 존재하지 않습니다."}), 400
    
    with open(filename, 'r') as file:
        content = file.read()
    
    return jsonify({"filename": filename, "content": content}), 200

# 파일 내용 쓰기 API
@app.route('/write', methods=['POST'])
def write_file():
    filename = request.json.get('filename')
    content = request.json.get('content')
    
    if not filename or not content:
        return jsonify({"error": "파일명이나 내용이 제공되지 않았습니다."}), 400
    
    with open(filename, 'w') as file:
        file.write(content)
    
    return jsonify({"message": f"파일 '{filename}'에 내용이 성공적으로 작성되었습니다."}), 200

# 파일 내용 삭제 API
@app.route('/delete_content', methods=['POST'])
def delete_content():
    filename = request.json.get('filename')
    content_to_remove = request.json.get('content_to_remove')
    
    if not filename or not content_to_remove:
        return jsonify({"error": "파일명이나 삭제할 내용이 제공되지 않았습니다."}), 400
    
    if not os.path.exists(filename):
        return jsonify({"error": "파일이 존재하지 않습니다."}), 400
    
    with open(filename, 'r') as file:
        content = file.read()
    
    new_content = content.replace(content_to_remove, "")
    
    with open(filename, 'w') as file:
        file.write(new_content)
    
    return jsonify({"message": f"파일 '{filename}'에서 내용이 성공적으로 삭제되었습니다."}), 200

# 서버 실행
if __name__ == '__main__':
    app.run(debug=True)
