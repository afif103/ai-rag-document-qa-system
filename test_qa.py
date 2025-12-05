import subprocess
import time
import requests

# Start backend
proc = subprocess.Popen(
    ["uvicorn", "backend.main:app", "--host", "127.0.0.1", "--port", "8001"]
)
time.sleep(5)  # Wait for startup

try:
    # Upload PDF
    with open("data/test_sample.pdf", "rb") as f:
        files = {"file": f}
        response = requests.post("http://127.0.0.1:8001/upload", files=files)
    print(
        "Upload response:",
        response.status_code,
        response.json() if response.status_code == 200 else response.text,
    )

    # Ask questions
    questions = [
        "What is TechCorp's mission?",
        "How do I report a bug?",
        "What are the pricing plans?",
        "What is the response time for support?",
        "Can I cancel my subscription anytime?",
    ]

    for q in questions:
        data = {"question": q}
        response = requests.post("http://127.0.0.1:8001/ask", json=data)
        print(f"Q: {q}")
        print(
            "A:",
            response.json()["answer"] if response.status_code == 200 else response.text,
        )
        print("---")

except Exception as e:
    print("Error:", e)

finally:
    # Stop backend
    proc.terminate()
    proc.wait()
