from langchain.tools import tool
from .calendly_launcher import launch_calendly_popup
from state import appointment_submitted, submitted_data, history  # shared import


# def book_appointment(details: str) -> str:
@tool
def book_appointment(details: str = "") -> str:
    """
    Books an appointment. Always launches Calendly. Ignores details.
    """
    appointment_submitted.clear()

# GOOGLE CALENDAR FORM URL >>
    # base_url = "https://calendar.app.google/juYLFkGs75TpADP87"

# CALENDLY URLS >>
    base_url = "https://calendly.com/d/cndz-npf-kc6"
    # base_url = "https://calendly.com/maheshs-first-insight/eyecare-appointment-booking"

    launch_calendly_popup(base_url)

    print("🕒 Waiting for user to finish booking...")
    if not appointment_submitted.wait(timeout=300):
        return "⚠️ Booking timed out. Please try again."

    # Grab the submitted data
    name = submitted_data.get("name")
    email = submitted_data.get("email")
    submission_uuid = submitted_data.get("submission_uuid")
    
    print(f"Inside book_appointment:\n Name: {name},\n Email: {email},\n ID: {submission_uuid}")
    history.append({"role": "assistant", "content": f"Appointment booked successfully for-->>  Name: {name} | Email: {email}"})
    return f"""✅ Appointment booked successfully for-->>  Name: {name} | Email: {email}"""


