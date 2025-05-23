from fastapi import FastAPI, Request, HTTPException, Query
from fastapi.responses import JSONResponse, HTMLResponse
from pydantic import BaseModel
from state import appointment_submitted, submitted_data, history
from agent.appointment_agent import agent_executor

app = FastAPI()

# Pydantic model for request body
class QueryRequest(BaseModel):
    message: str

@app.post("/query")
async def handle_query(request_data: QueryRequest):
    user_input = request_data.message
    if not user_input:
        raise HTTPException(status_code=400, detail="No input message provided")
    
    history.append({"role": "user", "content": user_input})
    
    try:
        response = agent_executor.run(history)
        history.append({"role": "assistant", "content": response})
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/success", response_class=HTMLResponse)
async def success(
    email: str = Query(...),
    name: str = Query(...),
    submission_uuid: str = Query(...)
):
    print(f"✅ Appointment Process Done!")
    print(f"📧 Email: {email}")
    print(f"🙍 Name: {name}")
    print(f"🆔 Submission UUID: {submission_uuid}")

    submitted_data['email'] = email
    submitted_data['name'] = name
    submitted_data['submission_uuid'] = submission_uuid

    global submitted
    submitted = True
    appointment_submitted.set()

    print("✅ Process done successfully!")

    return """
    <html>
    <head>
        <title>Appointment Confirmed</title>
        <style>
            body {
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                background-color: #f9f9f9;
                font-family: Arial, sans-serif;
                margin: 0;
            }
            .message-box {
                text-align: center;
                padding: 30px 40px;
                border-radius: 12px;
                background-color: white;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
            }
            h2 {
                color: #2e7d32;
            }
        </style>
    </head>
    <body>
        <div class="message-box">
            <h2>✅ Thank you for your Time!</h2>
            <p>You may now close this window.</p>
        </div>
    </body>
    </html>
    """

