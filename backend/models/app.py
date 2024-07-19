import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
from openai import OpenAI
import json
import base64
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials
from io import BytesIO

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

# 配置日志记录
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# GPT API配置
client = OpenAI(
    api_key='',
    base_url=''
)

def generate_completion(prompt, conversation_history):
    # 格式化 conversation_history 以符合 API 要求
    # formatted_history = [{"role": "user" if msg["sender"] == "user" else "assistant", "content": msg["text"]} for msg in conversation_history]
    # messages = formatted_history + [{"role": "user", "content": prompt}]
    messages = conversation_history + [{"role": "user", "content": prompt}]
    
    response = client.chat.completions.create(
        messages=messages,
        model="gpt-4"
    )
    response_json = response.to_dict()
    return response_json['choices'][0]['message']['content'].strip()

def get_user_info(user_id):
    try:
        response = requests.get(f'http://project-backend:3000/api/user/{user_id}')
        response.raise_for_status()
        user_info = response.json()
        if user_info['success']:
            return user_info['data']
        else:
            logger.error(f"Failed to fetch user info: {user_info['message']}")
            return None
    except Exception as e:
        logger.error(f"Error fetching user info: {e}")
        return None

def update_user_info(phone, update_data):
    try:
        response = requests.put(f'http://project-backend:3000/api/user/{phone}', json=update_data)
        response.raise_for_status()
        updated_info = response.json()
        if updated_info['success']:
            logger.info("User information updated successfully")
            return updated_info['data']
        else:
            logger.error(f"Failed to update user info: {updated_info['message']}")
            return None
    except Exception as e:
        logger.error(f"Error updating user info: {e}")
        return None


def summarize_medical_history(existing_history, new_history):
    prompt = (
        f"以下是病人的历史病历和新上传的病历，请总结并分条说明，去除多余和重复项目：\n\n"
        f"历史病历：\n{existing_history}\n\n"
        f"新上传病历：\n{new_history}\n\n"
        f"总结，只要结果无需解释："
    )
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="gpt-4"
    )
    response_json = response.to_dict()
    return response_json['choices'][0]['message']['content'].strip()

# def ocr_interface(image):
#     # 这里是OCR处理代码的占位符
#     # 假设这个函数接受图片输入并返回提取的文字内容
#     return "患有高血压和糖尿病多年，每日定时服用降压药和降糖药物"

def ocr_interface(image_base64):
    subscription_key = "cd84538c377243eea5ae279419a9095e"
    endpoint = "https://hospital-test.cognitiveservices.azure.com/"
    
    client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))
    
    # Decode the base64 image
    if image_base64.startswith('data:image'):
        header, base64_data = image_base64.split(',', 1)
        image_bytes = base64.b64decode(base64_data)
    else:
        image_bytes = base64.b64decode(image_base64)
    
    # Read from byte stream
    image_stream = BytesIO(image_bytes)
    ocr_result = client.read_in_stream(image_stream, raw=True)
    
    operation_location = ocr_result.headers["Operation-Location"]
    operation_id = operation_location.split("/")[-1]

    while True:
        result = client.get_read_result(operation_id)
        if result.status not in [OperationStatusCodes.running, OperationStatusCodes.not_started]:
            break

    if result.status == OperationStatusCodes.succeeded:
        # Extract text from OCR results
        extracted_text = ""
        read_results = result.analyze_result.read_results
        for text_result in read_results:
            for line in text_result.lines:
                extracted_text += line.text + "\n"
        return extracted_text
    else:
        return None

def process_conversation(conversation_history, user_id):
    try:
        # 处理对话历史中的图片
        user_info = get_user_info(user_id)

        logger.info(f"User info: {user_info}")
        if not user_info:
            return "无法获取用户信息，请稍后再试。"

        new_medical_history = ""
        message = conversation_history[-1]
        if message['sender'] == 'user' and message['type'] == 'image-text':
            image_content = message['text'].get('image')
            extracted_text = ocr_interface(image_content)
            new_medical_history = f"{extracted_text}"  # 只处理最新的一张图片

            summarized_history = summarize_medical_history(user_info['medicalHistory'], new_medical_history)
            user_info['medicalHistory'] = summarized_history
            update_user_info(user_id, user_info)

            return "Medical history updated: " + summarized_history


        patient_info = {
            "name": user_info.get("name", ""),
            "age": user_info.get("age", ""),
            "gender": user_info.get("gender", ""),
            "contact": user_info.get("phone", ""),
            "department": "",
            "health_analysis": "",
            "medical_history": "",
            "main_symptoms": ""
        }

        if message['sender'] == 'user' and message['text'] == '挂号':
        
            required_fields = ["name", "age", "gender", "contact", "medical_history", "main_symptoms", "department", "health_analysis"]
            system_prompt = "你是一个智能助手，你的任务是帮助用户生成预挂号文档。请根据和用户的对话以及用户的资料生成以下信息：既往病史，主要症状和应挂号科室。如果信息较为充足的话，可以加入一段用户个人健康状况分析。"

            # 转换 conversation_history 格式
            formatted_conversation_history = [
                {
                    "role": "user" if message["sender"] == "user" else "assistant",
                    "content": message["text"]
                }
                for message in conversation_history
                if message.get('type') == 'text'
            ]
  
            formatted_conversation_history.insert(0, {"role": "system", "content": system_prompt})
        
            for field in required_fields:
                if not patient_info[field]:
                    # gpt_prompt = f"请询问用户关于{field}的信息。"
                    # gpt_response = generate_completion(gpt_prompt, formatted_conversation_history)
                    # logger.info(f"GPT: {gpt_response}")
                    # formatted_conversation_history.append({"role": "assistant", "content": gpt_response})

                    # extraction_prompt = f"请从以下对话中提取{field}信息：{[message['content'] for message in formatted_conversation_history]}"
                    extraction_prompt = f"请从以上对话中提取或推理出{field}信息，只需要信息的内容，不需要解释"
                    extraction_response = generate_completion(extraction_prompt, formatted_conversation_history)
                    patient_info[field] = extraction_response

            info_str = (
                "Registration Information:<br>"
                "-------------------<br>"
                f"Name            : {patient_info.get('name', '')}"
                f"Age             : {patient_info.get('age', '')}"
                f"Gender          : {patient_info.get('gender', '')}"
                f"Contact         : {patient_info.get('contact', '')}"
                f"Department      : {patient_info.get('department', '')}"
                f"Health Analysis : {patient_info.get('health_analysis', '')}"
                f"Medical History : {patient_info.get('medical_history', '')}"
                f"Main Symptoms   : {patient_info.get('main_symptoms', '')}"
            )
            return info_str


        system_prompt = "你是一个智能医学助手，你的任务是与用户（很可能是患者）进行一段愉快且积极的聊天，引导用户大概说明其主要症状、既往病史等医学情况，用以后续的辅助挂号和治疗，不用太过详细，问清楚大概情况后可以表示自己了解了，建议用户输入“挂号”。第一个回复可以介绍自己，告诉用户可以上传病历的图片，后面就不必说了。"

        # 转换 conversation_history 格式
        formatted_conversation_history = [
            {
                "role": "user" if message["sender"] == "user" else "assistant",
                "content": message["text"]
            }
            for message in conversation_history
            if message.get('type') == 'text'
        ]
        formatted_conversation_history.insert(0, {"role": "system", "content": system_prompt})
        response = generate_completion(message['text'], formatted_conversation_history)

        # 返回 GPT 生成的回复
        return response
    except Exception as e:
        logger.error(f"Error processing conversation: {e}")
        return None

@app.route('/python/api/process', methods=['POST'])
def process():
    try:
        data = request.json
        logger.info(f"Received data: {data}")
        conversation_history = data.get('conversation_history', [])
        user_id = data.get('user_id')
        response = {}
        processed_text = process_conversation(conversation_history, user_id)
        if processed_text:
            response['processed_text'] = processed_text
        else:
            response['processed_text'] = "No valid data processed"
        
        logger.info(f"Response: {response}")
        return jsonify(response)
    except Exception as e:
        logger.error(f"Error in process endpoint: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
