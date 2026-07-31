from collections import defaultdict

# Step 1: Open and read the network traffic log file
with open("network_traffic.log", "r") as log_file:
    lines = log_file.readlines()

# Step 2: Parse each line and group timestamps by (source -> destination:port)
pair_timestamps = defaultdict(list)
for line in lines:
    line = line.strip()
    if not line:
        continue

    # Each line: time, source IP, '->', destination IP:port, and bytes
    left, right = line.split(" -> ")
    timestamp, source_ip = left.split()
    destination = right.split()[0]  # IP:port (ignore trailing byte count)

    pair = (source_ip, destination)
    pair_timestamps[pair].append(timestamp)

# Step 3: Find the pair with the most connections
top_pair = max(pair_timestamps, key=lambda pair: len(pair_timestamps[pair]))
timestamps = pair_timestamps[top_pair]
connection_count = len(timestamps)

# Step 4: Compute average seconds between consecutive connections
def to_seconds(timestamp):
    hours, minutes, seconds = map(int, timestamp.split(":"))
    return hours * 3600 + minutes * 60 + seconds

if connection_count > 1:
    times_in_seconds = [to_seconds(ts) for ts in timestamps]
    gaps = [
        times_in_seconds[i + 1] - times_in_seconds[i]
        for i in range(len(times_in_seconds) - 1)
    ]
    avg_seconds_between = sum(gaps) / len(gaps)
else:
    avg_seconds_between = 0.0

# Step 5: Print the beaconing suspect summary
print("=== Beaconing Suspect ===")
print(f"{top_pair[0]} -> {top_pair[1]}")
print(f"Connections: {connection_count}")
print(f"Average seconds between connections: {avg_seconds_between:.1f}")
print("Timestamps:")
for ts in timestamps:
    print(f"  {ts}")
