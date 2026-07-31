from datetime import datetime

# Keywords that mark an event as especially important in the timeline
KEY_MARKERS = ("SUCCESS LOGIN", ".locked", "READ_ME")

# Step 1: Read events from both log files
with open("auth_events.log", "r") as auth_file:
    auth_events = [line.strip() for line in auth_file if line.strip()]

with open("file_events.log", "r") as file_file:
    file_events = [line.strip() for line in file_file if line.strip()]

# Step 2: Merge all events into one list
events = auth_events + file_events

# Step 3: Sort events in chronological order (each line starts with date and time)
def event_time(line):
    return datetime.strptime(line[:19], "%Y-%m-%d %H:%M:%S")

events.sort(key=event_time)

# Step 4: Print the merged timeline, flagging key events
print("=== Timeline ===")
for event in events:
    if any(marker in event for marker in KEY_MARKERS):
        print(f"{event} *** KEY EVENT ***")
    else:
        print(event)

# Step 5: Calculate dwell time from first successful login to first encrypted file
first_login = next(event for event in events if "SUCCESS LOGIN" in event)
first_locked = next(event for event in events if ".locked" in event)

dwell_minutes = (event_time(first_locked) - event_time(first_login)).total_seconds() / 60

print()
print(f"Dwell time: {dwell_minutes:.1f} minutes")
print(f"  (from first SUCCESS LOGIN at {first_login[:19]}")
print(f"   to first .locked file at {first_locked[:19]})")
