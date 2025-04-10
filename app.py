# 효인아 이거 보고나서 방문기록 삭제 해. 그리고. 주석도 다 삭제하구 알겠지? ctrl + h 누르면 방문기록 나와 그거에서 github만 삭제해 오키??

from flask import Flask, request, jsonify, abort
import os

app = Flask(__name__)

# 파일 저장 경로 설정
BASE_DIR = "files"  # 파일이 저장될 디렉토리
if not os.path.exists(BASE_DIR):
    os.makedirs(BASE_DIR)  # 디렉토리가 없으면 자동으로 생성

# 유효성 검사 함수: 파일명과 내용이 올바른지 확인
def validate_input(file_name, content=None):
    """
    파일명 및 내용에 대한 유효성 검사를 합니다.
    - 파일명이 비어 있으면 오류를 반환
    - 내용이 제공되었으면 내용도 검사
    """
    if not file_name or not file_name.strip():
        return "File name cannot be empty", 400
    if content is not None and not content.strip():
        return "Content cannot be empty", 400
    return None, None

# /create 경로: 파일 생성
@app.route('/create', methods=['POST'])
def create_file():
    """
    POST 요청으로 파일을 생성하는 API.
    요청 본문에 'file_name'과 'content'를 포함하여 파일을 생성하고 내용을 기록.
    """
    file_name = request.json.get('file_name', '').strip()
    content = request.json.get('content', '').strip()

    error_message, status_code = validate_input(file_name, content)
    if error_message:
        return jsonify({"error": error_message}), status_code

    file_path = os.path.join(BASE_DIR, file_name)

    try:
        with open(file_path, 'w') as file:
            file.write(content)
        return jsonify({"message": f"File '{file_name}' created successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# /delete 경로: 파일 삭제
@app.route('/delete', methods=['DELETE'])
def delete_file():
    """
    DELETE 요청으로 파일을 삭제하는 API.
    요청 본문에 'file_name'을 포함하여 해당 파일을 삭제.
    """
    file_name = request.json.get('file_name', '').strip()

    error_message, status_code = validate_input(file_name)
    if error_message:
        return jsonify({"error": error_message}), status_code

    file_path = os.path.join(BASE_DIR, file_name)

    if os.path.exists(file_path):
        try:
            os.remove(file_path)
            return jsonify({"message": f"File '{file_name}' deleted successfully!"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "File not found!"}), 404

# /read 경로: 파일 읽기
@app.route('/read', methods=['GET'])
def read_file():
    """
    GET 요청으로 파일 내용을 읽는 API.
    요청 본문에 'file_name'을 포함하여 해당 파일의 내용을 반환.
    """
    file_name = request.args.get('file_name', '').strip()

    error_message, status_code = validate_input(file_name)
    if error_message:
        return jsonify({"error": error_message}), status_code

    file_path = os.path.join(BASE_DIR, file_name)

    if os.path.exists(file_path):
        try:
            with open(file_path, 'r') as file:
                content = file.read()
            return jsonify({"content": content}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "File not found!"}), 404

# /write 경로: 파일 내용 쓰기
@app.route('/write', methods=['POST'])
def write_file():
    """
    POST 요청으로 파일에 내용을 추가하는 API.
    요청 본문에 'file_name'과 'content'를 포함하여 해당 파일에 내용을 추가.
    """
    file_name = request.json.get('file_name', '').strip()
    content = request.json.get('content', '').strip()

    error_message, status_code = validate_input(file_name, content)
    if error_message:
        return jsonify({"error": error_message}), status_code

    file_path = os.path.join(BASE_DIR, file_name)

    if os.path.exists(file_path):
        try:
            with open(file_path, 'a') as file:
                file.write(content)
            return jsonify({"message": f"Content added to '{file_name}'!"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "File not found!"}), 404

# /clear 경로: 파일 내용 삭제
@app.route('/clear', methods=['POST'])
def clear_file():
    """
    POST 요청으로 파일 내용을 삭제하는 API.
    요청 본문에 'file_name'을 포함하여 해당 파일의 내용을 지움.
    """
    file_name = request.json.get('file_name', '').strip()

    error_message, status_code = validate_input(file_name)
    if error_message:
        return jsonify({"error": error_message}), status_code

    file_path = os.path.join(BASE_DIR, file_name)

    if os.path.exists(file_path):
        try:
            with open(file_path, 'w') as file:
                file.write("")  # 파일 내용 삭제
            return jsonify({"message": f"Content of '{file_name}' cleared!"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "File not found!"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
