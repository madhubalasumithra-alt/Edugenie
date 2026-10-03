# EduGenie – Google Gemini Powered Learning Assistant

EduGenie is a FastAPI + HTML/CSS/JavaScript learning assistant with five features:

- Question answering
- Simple concept explanations
- 3-question MCQ quiz generation
- Educational text summarization
- Personalized learning-path recommendations

The app follows the supplied project document while using the current `google-genai` Python SDK. The explanation feature defaults to Gemini for easy installation; the LaMini-Flan-T5 local model described in the document remains available as an optional provider.

## 1. Requirements

- Python 3.10 or newer
- VS Code
- A Google Gemini API key for AI requests

## 2. Open in VS Code

Open the `EduGenie` folder itself as the VS Code workspace.

## 3. Create a virtual environment

### Windows PowerShell

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If `py` is unavailable, use `python -m venv .venv`.

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 4. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

For development tests:

```bash
pip install -r requirements-dev.txt
```

## 5. Configure Gemini

Copy `.env.example` to `.env`.

Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

macOS / Linux:

```bash
cp .env.example .env
```

Open `.env` and replace:

```env
GEMINI_API_KEY=replace_with_your_google_ai_studio_api_key
```

with your real key. Never commit `.env` to Git.

The model is controlled by:

```env
GEMINI_MODEL=gemini-3.8-flash
```

If that model is not available to your API account, set this to another text model shown in your Google AI Studio account.

## 6. Run the app

```bash
python -m uvicorn main:app --reload
```

Open:

- App: http://127.0.0.1:8000
- Swagger API docs: http://127.0.0.1:8000/docs
- Health check: http://127.0.0.1:8000/health

On Windows you can also double-click `run_windows.bat` after setup.

## 7. Run tests

```bash
pytest -q
```

The automated tests mock the AI calls, so they do not spend Gemini quota and do not need a real API response.

## 8. Optional: Local LaMini explanation model

The original documentation uses `MBZUAI/LaMini-Flan-T5-783M` for concept explanation. This is optional because it downloads a sizeable local model and PyTorch.

Install it with:

```bash
pip install -r requirements-local.txt
```

Then change `.env`:

```env
EXPLAINER_PROVIDER=local
```

The first explanation request downloads the model. Other features continue to use Gemini.

## API endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Frontend |
| GET | `/health` | Configuration/health status |
| POST | `/qa` | Question answering |
| POST | `/explain` | Concept explanation |
| POST | `/quiz` | MCQ quiz generation |
| POST | `/summarize` | Summarization |
| POST | `/learn/recommendations` | Learning path |
| POST | `/api/run` | Unified endpoint used by frontend |

## Example request

```bash
curl -X POST http://127.0.0.1:8000/qa \
  -H "Content-Type: application/json" \
  -d '{"question":"Which is the largest ocean?"}'
```

## Troubleshooting

### `GEMINI_API_KEY is not configured`
Create `.env` from `.env.example` and add the key.

### Model not found / unavailable
Change `GEMINI_MODEL` in `.env` to a Gemini text model available in your Google AI Studio account.

### VS Code is using the wrong Python
Press `Ctrl+Shift+P` → **Python: Select Interpreter** → select the interpreter inside `.venv`.

### Local model installation is too large
Keep `EXPLAINER_PROVIDER=gemini`; the local model is optional.
