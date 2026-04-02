import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional


def parse_time(ts: str) -> datetime:
    return datetime.fromisoformat(ts)


def load_events(file_path: str) -> List[Dict]:
    with open(file_path, "r") as f:
        events = json.load(f)

    for event in events:
        event["timestamp"] = parse_time(event["timestamp"])

    events.sort(key=lambda x: x["timestamp"])
    return events


def get_latest_event(events: List[Dict], event_type: str) -> Optional[Dict]:
    filtered = [e for e in events if e["eventType"] == event_type]
    return filtered[-1] if filtered else None


def minutes_between(t1: datetime, t2: datetime) -> float:
    return abs((t2 - t1).total_seconds()) / 60


def predict_next_potty_window(events: List[Dict]) -> Optional[Dict]:
    """
    Very simple rule-based predictor.

    Rules:
    - After wake: potty likely in 15-30 mins
    - After feed: potty likely in 90-180 mins
    - After water: potty likely in 30-90 mins
    - If potty happened in last 45 mins, suppress alert
    - Choose the earliest reasonable upcoming window
    """
    now = max(e["timestamp"] for e in events)

    latest_wake = get_latest_event(events, "wake")
    latest_feed = get_latest_event(events, "feed")
    latest_water = get_latest_event(events, "water")
    latest_potty = get_latest_event(events, "potty")

    if latest_potty and minutes_between(latest_potty["timestamp"], now) <= 45:
        return None

    candidate_windows = []

    if latest_wake:
        start = latest_wake["timestamp"] + timedelta(minutes=15)
        end = latest_wake["timestamp"] + timedelta(minutes=30)
        if end >= now:
            candidate_windows.append(("wake-rule", start, end))

    if latest_water:
        start = latest_water["timestamp"] + timedelta(minutes=30)
        end = latest_water["timestamp"] + timedelta(minutes=90)
        if end >= now:
            candidate_windows.append(("water-rule", start, end))

    if latest_feed:
        start = latest_feed["timestamp"] + timedelta(minutes=90)
        end = latest_feed["timestamp"] + timedelta(minutes=180)
        if end >= now:
            candidate_windows.append(("feed-rule", start, end))

    if not candidate_windows:
        return None

    candidate_windows.sort(key=lambda x: x[1])
    chosen_rule, window_start, window_end = candidate_windows[0]

    alert_time = window_start - timedelta(minutes=10)
    if alert_time < now:
        alert_time = now

    return {
        "ruleUsed": chosen_rule,
        "windowStart": window_start,
        "windowEnd": window_end,
        "alertTime": alert_time
    }


def format_dt(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d %I:%M %p")


def main() -> None:
    events = load_events("sample_events.json")
    prediction = predict_next_potty_window(events)

    print("=== PottyIQ Prototype ===")
    print()

    print("Recent events:")
    for event in events:
        print(f"- {event['eventType']:>5} at {format_dt(event['timestamp'])}")

    print()

    if not prediction:
        print("No potty alert needed right now.")
        return

    print("Prediction result:")
    print(f"- Rule used: {prediction['ruleUsed']}")
    print(f"- Next potty window: {format_dt(prediction['windowStart'])} to {format_dt(prediction['windowEnd'])}")
    print(f"- Alert owner at: {format_dt(prediction['alertTime'])}")


if __name__ == "__main__":
    main()
