from fasthtml.common import *
from app.prompts.system import DEFAULT_SYSTEM_PROMPT
from app.config import settings


def register(app, rt):
    @rt("/")
    def get():
        return Html(
            Head(
                Title("Ranczo Dziki Sad - Chat"),
                Style("""
                    * { margin: 0; padding: 0; box-sizing: border-box; }
                    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f5f5f5; color: #333; }
                    .container { max-width: 800px; margin: 0 auto; padding: 16px; }
                    .header { text-align: center; padding: 20px 0; }
                    .header h1 { font-size: 1.5rem; color: #2d5016; }
                    .settings { background: #fff; border-radius: 8px; padding: 16px; margin-bottom: 16px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
                    .settings label { display: block; font-weight: 600; margin-bottom: 4px; font-size: 0.85rem; color: #555; }
                    .settings textarea { width: 100%; height: 80px; border: 1px solid #ddd; border-radius: 4px; padding: 8px; font-size: 0.85rem; resize: vertical; font-family: inherit; }
                    .settings-row { display: flex; gap: 12px; margin-top: 12px; flex-wrap: wrap; }
                    .settings-row > div { flex: 1; min-width: 120px; }
                    .settings input[type="range"] { width: 100%; }
                    .settings input[type="number"] { width: 100%; border: 1px solid #ddd; border-radius: 4px; padding: 6px; }
                    .chat-box { background: #fff; border-radius: 8px; height: 400px; overflow-y: auto; padding: 16px; margin-bottom: 16px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
                    .msg { margin-bottom: 12px; padding: 10px 14px; border-radius: 12px; max-width: 80%; word-wrap: break-word; }
                    .msg-user { background: #2d5016; color: #fff; margin-left: auto; border-bottom-right-radius: 4px; }
                    .msg-bot { background: #e8f0e0; color: #333; margin-right: auto; border-bottom-left-radius: 4px; }
                    .msg-sources { font-size: 0.75rem; color: #888; margin-top: 4px; }
                    .input-area { display: flex; gap: 8px; }
                    .input-area input { flex: 1; border: 1px solid #ddd; border-radius: 8px; padding: 12px; font-size: 1rem; }
                    .btn { padding: 10px 20px; border: none; border-radius: 8px; cursor: pointer; font-weight: 600; font-size: 0.9rem; }
                    .btn-primary { background: #2d5016; color: #fff; }
                    .btn-primary:hover { background: #3a6b1c; }
                    .btn-secondary { background: #ddd; color: #333; }
                    .btn-secondary:hover { background: #ccc; }
                    .actions { display: flex; gap: 8px; align-items: center; margin-bottom: 12px; }
                    .status { font-size: 0.8rem; color: #666; }
                """),
            ),
            Body(
                Div(
                    Div(
                        H1("Ranczo Dziki Sad - Asystent"),
                        P("Zadaj pytanie o nasze ranczo, odpowiedz bazuje na stronie internetowej.", style="color:#666;font-size:0.9rem;"),
                        cls="header",
                    ),
                    Div(
                        Label("System prompt:"),
                        Textarea(DEFAULT_SYSTEM_PROMPT, id="system-prompt"),
                        Div(
                            Div(Label("Temperature: ", id="temp-label"), Input(type="range", id="temperature", min="0", max="2", step="0.1", value=str(settings.groq_temperature), oninput="document.getElementById('temp-label').textContent='Temperature: '+this.value")),
                            Div(Label("Max tokens:"), Input(type="number", id="max-tokens", value=str(settings.groq_max_tokens), min="1", max="4096")),
                            Div(Label("Top-p:"), Input(type="number", id="top-p", value=str(settings.groq_top_p), min="0", max="1", step="0.1")),
                            cls="settings-row",
                        ),
                        cls="settings",
                    ),
                    Div(
                        Button("Przeladuj dokumenty", cls="btn btn-secondary", id="scrape-btn", onclick="scrapeSite()"),
                        Span(id="scrape-status", cls="status"),
                        cls="actions",
                    ),
                    Div(id="chat-box", cls="chat-box"),
                    Div(
                        Input(type="text", id="user-input", placeholder="Napisz pytanie...", onkeydown="if(event.key==='Enter')sendMessage()"),
                        Button("Wyslij", cls="btn btn-primary", onclick="sendMessage()"),
                        cls="input-area",
                    ),
                    Script("""
                        async function sendMessage() {
                            const input = document.getElementById('user-input');
                            const msg = input.value.trim();
                            if (!msg) return;
                            input.value = '';
                            addMessage(msg, 'user');
                            const body = {
                                message: msg,
                                system_prompt: document.getElementById('system-prompt').value,
                                temperature: parseFloat(document.getElementById('temperature').value),
                                max_tokens: parseInt(document.getElementById('max-tokens').value),
                                top_p: parseFloat(document.getElementById('top-p').value)
                            };
                            try {
                                const res = await fetch('/api/chat', {
                                    method: 'POST',
                                    headers: {'Content-Type': 'application/json'},
                                    body: JSON.stringify(body)
                                });
                                const data = await res.json();
                                addMessage(data.answer, 'bot', data.sources);
                            } catch (e) {
                                addMessage('Blad polaczenia z serwerem.', 'bot');
                            }
                        }
                        function addMessage(text, role, sources) {
                            const box = document.getElementById('chat-box');
                            const div = document.createElement('div');
                            div.className = 'msg msg-' + (role === 'user' ? 'user' : 'bot');
                            div.textContent = text;
                            if (sources && sources.length) {
                                const src = document.createElement('div');
                                src.className = 'msg-sources';
                                src.textContent = 'Zrodla: ' + sources.join(', ');
                                div.appendChild(src);
                            }
                            box.appendChild(div);
                            box.scrollTop = box.scrollHeight;
                        }
                        async function scrapeSite() {
                            const btn = document.getElementById('scrape-btn');
                            const status = document.getElementById('scrape-status');
                            btn.disabled = true;
                            btn.textContent = 'Ladowanie...';
                            status.textContent = 'Przetwarzanie dokumentow...';
                            try {
                                const res = await fetch('/api/scrape', {method: 'POST'});
                                const data = await res.json();
                                status.textContent = data.message;
                            } catch (e) {
                                status.textContent = 'Blad ladowania dokumentow';
                            }
                            btn.disabled = false;
                            btn.textContent = 'Przeladuj dokumenty';
                        }
                    """),
                    cls="container",
                ),
            ),
        )
