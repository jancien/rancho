from app.models import ChatRequest, ChatResponse
from app.services.rag import ask_question


def register(app, rt):
    @rt("/api/chat")
    def post(req: ChatRequest):
        try:
            result = ask_question(
                user_message=req.message,
                system_prompt=req.system_prompt,
                temperature=req.temperature,
                max_tokens=req.max_tokens,
                top_p=req.top_p,
            )
            return ChatResponse(answer=result["answer"], sources=result["sources"])
        except Exception as e:
            return ChatResponse(answer=f"Blad serwera: {str(e)}", sources=[])
