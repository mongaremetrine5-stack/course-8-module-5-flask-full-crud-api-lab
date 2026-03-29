from flask import Flask, jsonify, request

app = Flask(__name__)


class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        """Serialize the Event to a plain dictionary for JSON responses."""
        return {"id": self.id, "title": self.title}


# ---------------------------------------------------------------------------
# In-memory data store — acts as a lightweight "database"
# ---------------------------------------------------------------------------
events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop"),
]

# Auto-incrementing ID counter (simulates a DB sequence)
next_id = 3


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------
def find_event(event_id):
    """Return the Event whose id matches event_id, or None if not found."""
    return next((e for e in events if e.id == event_id), None)


# ---------------------------------------------------------------------------
# POST /events — Create a new event
# ---------------------------------------------------------------------------
@app.route("/events", methods=["POST"])
def create_event():
    global next_id

    data = request.get_json()

    # Validate that a body was sent and that 'title' is present
    if not data or "title" not in data:
        return jsonify({"error": "Missing required field: 'title'"}), 400

    title = data["title"].strip()
    if not title:
        return jsonify({"error": "'title' must not be empty"}), 400

    # Create and store the new event
    new_event = Event(next_id, title)
    events.append(new_event)
    next_id += 1

    # 201 Created — return the newly created resource
    return jsonify(new_event.to_dict()), 201


# ---------------------------------------------------------------------------
# PATCH /events/<id> — Partially update an existing event's title
# ---------------------------------------------------------------------------
@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    event = find_event(event_id)

    # 404 if the event doesn't exist
    if event is None:
        return jsonify({"error": f"Event with id {event_id} not found"}), 404

    data = request.get_json()

    # Validate that 'title' was provided in the request body
    if not data or "title" not in data:
        return jsonify({"error": "Missing required field: 'title'"}), 400

    title = data["title"].strip()
    if not title:
        return jsonify({"error": "'title' must not be empty"}), 400

    # Apply the update
    event.title = title

    # 200 OK — return the updated resource
    return jsonify(event.to_dict()), 200


# ---------------------------------------------------------------------------
# DELETE /events/<id> — Remove an event from the list
# ---------------------------------------------------------------------------
@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    event = find_event(event_id)

    # 404 if the event doesn't exist
    if event is None:
        return jsonify({"error": f"Event with id {event_id} not found"}), 404

    events.remove(event)

    # 200 OK with a confirmation message (use 204 if you prefer no body)
    return jsonify({"message": f"Event {event_id} deleted successfully"}), 200


# ---------------------------------------------------------------------------
# GET /events — Bonus: list all events (handy for manual testing)
# ---------------------------------------------------------------------------
@app.route("/events", methods=["GET"])
def list_events():
    return jsonify([e.to_dict() for e in events]), 200


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)