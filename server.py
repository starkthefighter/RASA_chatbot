from fastapi import FastAPI
from pydantic import BaseModel
import requests
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Bạn có thể giới hạn bằng cách đặt danh sách các domain cụ thể thay vì "*"
    allow_credentials=True,
    allow_methods=["*"],  # Cho phép tất cả các phương thức (POST, GET, v.v.)
    allow_headers=["*"],  # Cho phép tất cả các header
)

# Định nghĩa model cho dữ liệu đầu vào
class QueryInput(BaseModel):
    query_text: str

@app.post("/query")
async def get_info(query: QueryInput):
    # NLP
    conver_text = query.query_text.lower()

    # Gửi yêu cầu POST đến Rasa Action Server
    response = requests.post('http://127.0.0.1:5005/webhooks/rest/webhook',
                             json={"sender": "test", "message": query.query_text}).json()

    # Kiểm tra phản hồi từ Rasa
    if response:
        results = []
        for message in response:
            text = message.get("text", "")
            if text == "LLM_predict" or len(text) == 0:
                results.append("Generated AI response")
            else:
                results.append(text)
        final_response = "\n".join(results)
    else:
        final_response = "Failed to get a response."

    return {"response": final_response}

# Chạy ứng dụng FastAPI
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)
