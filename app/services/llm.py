from groq import Groq
from groq import APIError, APIConnectionError, AuthenticationError
from app.config import settings


def get_chat_response(messages: list[dict], temperature: float, max_tokens: int, top_p: float) -> str:
    try:
        client = Groq(api_key=settings.groq_api_key)
        response = client.chat.completions.create(
            model=settings.groq_model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
        )
        return response.choices[0].message.content or ""
    except AuthenticationError:
        return "Blad autoryzacji API. Sprawdz klucz API Groq."
    except APIConnectionError:
        return "Blad polaczenia z API Groq. Sprawdz polaczenie internetowe."
    except APIError as e:
        return f"Blad API Groq: {e.message}"
    except Exception as e:
        return f"Blad: {str(e)}"
