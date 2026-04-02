import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional


# -------------------------------
# Utility Functions
# -------------------------------

def parse_time(ts: str) -> datetime:
    """
    Convert ISO timestamp string → Python datetime object
    Example: "2026-03-31T07:00:00"
    """
    return datetime.fromisoformat(ts)


def load_events(file_path: str) -> List[Dict]:
    """
    Load events from JSON file and:
    - parse timestamps into datetime objects
    - sort events chronologically

    Why sorting?
    → Prediction depends on latest events
    """
    with open(file_path, "r") as f:
        events = json.load(f)

    # Convert string timestamps → datetime objects
    for event in events:
        event["timestamp"] = parse_time(event["timestamp"])

    # Ensure events are processed in time order
    events.sort(key=lambda x: x["timestamp"])
    return events


def get_latest_event(events: List[Dict], event_type: str) -> Optional[Dict]:
    """
    Fetch the most recent event of a given type.

    Example:
    → latest 'feed' event
    → latest 'potty' event

    This is important because rules depend on latest activity.
    """
    filtered = [e for e in events if e["eventType"] == event_type]
    return filtered[-1] if filtered else None


def minutes_between(t1: datetime, t2: datetime) -> float:
    """
    Calculate time difference in minutes between two timestamps.
    Used for rule checks like:
    → "Did potty happen recently?"
    """
    return abs((t2 - t1).total_seconds()) / 60


# -------------------------------
# Core Prediction Logic
# -------------------------------

def predict_next_potty_window(events: List[Dict]) -> Optional[Dict]:
    """
    Core rule-based prediction engine.

    Goal:
    → Estimate next potty window based on recent activity

    Rules implemented:
    1. After wake → potty likely in 15–30 minutes
    2. After water → potty likely in 30–90 minutes
    3. After feed → potty likely in 90–180 minutes
    4. If potty happened in last 45 mins → suppress alert
    5. Choose the earliest upcoming valid window

    NOTE:
    This is intentionally simple (prototype).
    Real system would include ML + personalization.
    """

    # Treat latest event timestamp as "current time"
    now = max(e["timestamp"] for e in events)

    # Get latest events for each type
    latest_wake = get_latest_event(events, "wake")
    latest_feed = get_latest_event(events, "feed")
    latest_water = get_latest_event(events, "water")
    latest_potty = get_latest_event(events, "potty")

    # -------------------------------
    # Rule 4: Suppress if potty recent
    # -------------------------------
    if latest_potty and minutes_between(latest_potty["timestamp"], now) <= 45:
        return None  # No alert needed

    # Store candidate windows
    candidate_windows = []

    # -------------------------------
    # Rule 1: Wake-based prediction
    # -------------------------------
    if latest_wake:
        start = latest_wake["timestamp"] + timedelta(minutes=15)
        end = latest_wake["timestamp"] + timedelta(minutes=30)

        # Only consider future or active windows
        if end >= now:
            candidate_windows.append(("wake-rule", start, end))

    # -------------------------------
    # Rule 2: Water-based prediction
    # -------------------------------
    if latest_water:
        start = latest_water["timestamp"] + timedelta(minutes=30)
        end = latest_water["timestamp"] + timedelta(minutes=90)

        if end >= now:
            candidate_windows.append(("water-rule", start, end))

    # -------------------------------
    # Rule 3: Feed-based prediction
    # -------------------------------
    if latest_feed:
        start = latest_feed["timestamp"] + timedelta(minutes=90)
        end = latest_feed["timestamp"] + timedelta(minutes=180)

        if end >= now:
            candidate_windows.append(("feed-rule", start, end))

    # No valid predictions
    if not candidate_windows:
        return None

    # -------------------------------
    # Choose earliest upcoming window
    # -------------------------------
    candidate_windows.sort(key=lambda x: x[1])
    chosen_rule, window_start, window_end = candidate_windows[0]

    # -------------------------------
    # Alert logic
    # -------------------------------
    # Notify user 10 minutes before window start
    alert_time = window_start - timedelta(minutes=10)

    # If alert time already passed → trigger immediately
    if alert_time < now:
        alert_time = now

    return {
        "ruleUsed": chosen_rule,
        "windowStart": window_start,
        "windowEnd": window_end,
        "alertTime": alert_time
    }


# -------------------------------
# Output Formatting
# -------------------------------

def format_dt(dt: datetime) -> str:
    """
    Format datetime for human-readable output
    """
    return dt.strftime("%Y-%m-%d %I:%M %p")


# -------------------------------
# Main Execution
# -------------------------------

def main() -> None:
    """
    Entry point for prototype.

    Flow:
    1. Load events
    2. Run prediction engine
    3. Print results
    """

    events = load_events("sample_events.json")
    prediction = predict_next_potty_window(events)

    print("=== PottyIQ Prototype ===")
    print()

    print("Recent events:")
    for event in events:
        print(f"- {event['eventType']:>5} at {format_dt(event['timestamp'])}")

    print()

    # If no prediction → nothing to alert
    if not prediction:
        print("No potty alert needed right now.")
        return

    # Print prediction details
    print("Prediction result:")
    print(f"- Rule used: {prediction['ruleUsed']}")
    print(f"- Next potty window: {format_dt(prediction['windowStart'])} to {format_dt(prediction['windowEnd'])}")
    print(f"- Alert owner at: {format_dt(prediction['alertTime'])}")


# Run script
if __name__ == "__main__":
    main()
