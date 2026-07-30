from collections import Counter

# Step 1: Open and read the log file
with open("server_access.log", "r") as log_file:
    lines = log_file.readlines()

# Step 2 & 3: Find FAILED LOGIN lines and extract IP addresses
failed_ips = []
for line in lines:
    if "FAILED LOGIN" in line:
        # IP appears after "from " (may have extra text like "(Moscow)" after it)
        ip = line.split("from ")[1].split()[0]
        failed_ips.append(ip)

# Step 4: Count how many times each IP appears
ip_counts = Counter(failed_ips)

# Step 5: Print summary sorted from most to fewest failed attempts
print("=== Failed Login Summary ===")
for ip, count in ip_counts.most_common():
    line = f"{ip}: {count} failed attempt(s)"
    # Flag IPs with 3+ failures as likely brute force
    if count >= 3:
        line += " ⚠ LIKELY BRUTE FORCE"
    print(line)
