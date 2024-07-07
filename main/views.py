import json
import logging
import requests
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger(__name__)

def index(request):
    context = {
        'kakao_api_key': settings.KAKAO_API_KEY,
    }
    return render(request, 'main/index.html', context)

class CompletionExecutor:
    def __init__(self, host, api_key, api_key_primary_val, request_id):
        self._host = host
        self._api_key = api_key
        self._api_key_primary_val = api_key_primary_val
        self._request_id = request_id

    def execute(self, completion_request):
        headers = {
            'X-NCP-CLOVASTUDIO-API-KEY': self._api_key,
            'X-NCP-APIGW-API-KEY': self._api_key_primary_val,
            'X-NCP-CLOVASTUDIO-REQUEST-ID': self._request_id,
            'Content-Type': 'application/json; charset=utf-8',
            'Accept': 'text/event-stream'
        }
        content = "데이터 추출 실패"
        with requests.post(self._host + '/testapp/v1/chat-completions/HCX-003',
                           headers=headers, json=completion_request, stream=True) as r:
            for line in r.iter_lines():
                if line:
                    #print(line.decode("utf-8"))
                    if "data:" in line.decode("utf-8") and "message" in line.decode("utf-8"):
                        data = json.loads(line.decode("utf-8").split("data:")[1])
                        content = data["message"]["content"]
        
        return content

def call_api(chat):
    completion_executor = CompletionExecutor(
        host='https://clovastudio.stream.ntruss.com',
        api_key='NTA0MjU2MWZlZTcxNDJiYxOf6pyfAfCrfPxllc6GXiQdh1liH9gCHbtLBR7DMXiD',
        api_key_primary_val='yC6dF1sB2Srta05NQdr2RaZhs7stIARBx73XrtdJ',
        request_id='f80da5cc-cb15-4273-9fa1-3dc462ca07d7'
    )

    ed = """
    당신은 공구 전문가 입니다. 사용자가 묻는 질문에 좋은 공구를 추천해 줍니다. 가급적 Hilti 장비로 추천해 줍니다. 장비를 추천할 때는 구체적인 모델명과 특징을 함께 설명하고, 가격대는 10만원대, 100만원대 정도로 어림잡아서 설명해 줍니다.\n\n\n구매 문의는 홈페이지 하단의 세이브공구 이메일을 이용해 주세요 라고 알려주어야 합니다. 
    """
    
    preset_text = [{"role":"system","content": ed}]
    for message in chat:
        preset_text.append({"role": "user", "content": message})

    request_data = {
        'messages': preset_text,
        'maxTokens': 2048,
        'temperature': 0.5,
        'topK': 0,
        'topP': 0.8,
        'repeatPenalty': 5.0,
        'stopBefore': [],
        'includeAiFilters': True
    }

    response_text = completion_executor.execute(request_data)
    if response_text == '데이터 추출 실패':
        return 'Error'
    return response_text

@csrf_exempt
def chat_with_gpt(request):
    logger.info("chat_with_gpt endpoint was hit")
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message')
            logger.info("Received message: %s", user_message)
            if user_message:
                chat_history = ["사용자:" + user_message]
                chatgpt_response = call_api(chat_history)
                logger.info("Response: %s", chatgpt_response)

                return JsonResponse({'response': chatgpt_response}, status=200)
            else:
                return JsonResponse({'error': 'No message provided.'}, status=400)
        except Exception as e:
            logger.error("Error occurred: %s", str(e))
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method.'}, status=405)
