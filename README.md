Appointment Booking - Minimal FastAPI example

Run locally:

1. Create virtualenv and install requirements:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Start the server:

```bash
uvicorn app.main:app --reload
```

3. API endpoints:
- `POST /appointments` create appointment (JSON)
- `GET /appointments` list appointments
- `GET /appointments/{id}` get appointment
- `DELETE /appointments/{id}` delete appointment

4. Run tests:

```bash
pytest -q
```
# AppointmentBooking