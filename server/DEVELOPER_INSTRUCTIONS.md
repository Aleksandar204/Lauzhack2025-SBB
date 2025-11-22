**Quick Start — For teammates less familiar with backends**

This project is a small FastAPI app. These instructions assume you're in the Codespace or a Linux/macOS terminal with `git` and `python` available.

**Prerequisites**
- Python 3.11+ (3.12 is fine) is recommended.
- A terminal in the project root (the folder that contains `app.py`).

**1. Create and activate a virtual environment (one-time per machine)**
```bash
# from the project root
python -m venv .venv
source .venv/bin/activate
```

If your Codespace already has a `.venv` and the environment is configured, just activate it with the second command.

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

If you prefer pinning versions or reproducible installs, ask to generate a pinned `requirements.txt`.

**3. Run the API server**
You can run the app either by running the module directly (the project includes a small entrypoint) or by running Uvicorn directly.

Option A — run with Python (easy, recommended for Codespaces):
```bash
# starts the app at http://0.0.0.0:8000
python app.py
```

Option B — run Uvicorn directly:
```bash
# from the project root
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

Codespace forwarded URL (shared)
---------------------------------
Novak runuje ovo. ako novak ne zaustavi namerno app da bi uradio update, server se nece sam ugasiti. url ostaje isti cak iako ugasim app pa runujem ponovo.

If the running Codespace has forwarded port 8000 and the owner made it public, you can use the shared preview URL directly without running anything locally. Example (this Codespace URL was shared by the project owner):

```bash
curl -s "https://opulent-fishstick-6q7q69xqgpjhwwj-8000.app.github.dev/ping"
# Expected output: {"msg":"pong"}

curl -s "https://opulent-fishstick-6q7q69xqgpjhwwj-8000.app.github.dev/check"
# Expected output: {"id":"<some-uuid>"}
```

Note: the preview URL will stay accessible according to the Codespace's port visibility settings. If the owner later makes the port private, or another codespace is started and used for the backend, you will need them to re-share it, or run the app locally.

**5. Stop the server**
If you started `python app.py` or `uvicorn ...` in the foreground, press `Ctrl+C` in that terminal to stop it.

**Troubleshooting**
- "ImportError: No module named ..." — ensure the virtual environment is activated and you ran `pip install -r requirements.txt` in that environment.
- Port conflict (something already using port 8000) — either stop the other process or start with `--port 8001`. this will create a different URL for the frontend.
- If `python app.py` starts and exits immediately — make sure `app.py` contains the `if __name__ == "__main__"` block (it does in this repo) and that `uvicorn` is installed.


**Next steps I can help with**
- Pin package versions into `requirements.txt` for reproducible installs.
- Add a `Makefile` or simple `run.sh` to make start/test commands one-liners.
- Add a lightweight health-check or README with endpoint docs.

If anything above is unclear, tell me your OS/Codespace setup and I'll tailor the steps or run them for you.