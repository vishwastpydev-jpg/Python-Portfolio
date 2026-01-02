import time
from datetime import datetime as dt
import os

# --- SYSTEM DETECTION ---
Linux_host = "/etc/hosts"
Window_host = r"C:\Windows\System32\drivers\etc\hosts"
redirect = "127.0.0.1"

if os.name == 'posix':
    default_hoster = Linux_host
elif os.name == 'nt':
    default_hoster = Window_host
else:
    print("OS Unknown. Exiting.")
    exit()

def get_user_config():
    """Gathers blocking details from the user."""
    print("--- 🛡️ Website Blocker Configuration ---")
    
    # 1. Get Websites
    raw_sites = input("Enter websites to block separated by commas (e.g. facebook.com, youtube.com): ")
    # Clean the input: strip spaces and add 'www.' versions automatically
    sites = []
    for s in raw_sites.split(","):
        clean_s = s.strip().lower()
        if clean_s:
            sites.append(clean_s)
            if not clean_s.startswith("www."):
                sites.append(f"www.{clean_s}")
    
    # 2. Get Hours
    try:
        start = int(input("Enter start hour (0-23, e.g., 9 for 9 AM): "))
        end = int(input("Enter end hour (0-23, e.g., 17 for 5 PM): "))
        if not (0 <= start <= 23 and 0 <= end <= 23):
            raise ValueError("Hours must be between 0 and 23.")
    except ValueError as e:
        print(f"Invalid input: {e}. Defaulting to 9 AM - 5 PM.")
        start, end = 9, 17

    return list(set(sites)), start, end

def block_websites(sites_to_block, start_hour, end_hour):
    print(f"\n✅ Monitor active for: {', '.join(sites_to_block)}")
    print(f"⏰ Blocking window: {start_hour}:00 to {end_hour}:00")
    print(f"📂 Modifying: {default_hoster}\n")

    while True:
        try:
            # Check if current time is within the blocking window
            current_time = dt.now()
            is_blocking_time = (
                dt(current_time.year, current_time.month, current_time.day, start_hour)
                < current_time
                < dt(current_time.year, current_time.month, current_time.day, end_hour)
            )

            if is_blocking_time:
                print("--- 🔒 Working Hours: Sites Blocked ---")
                with open(default_hoster, "r+") as hostfile:
                    hosts = hostfile.read()
                    for site in sites_to_block:
                        if site not in hosts:
                            hostfile.write(redirect + " " + site + "\n")
            else:
                print("--- 🔓 Free Time: Sites Unblocked ---")
                with open(default_hoster, "r+") as hostfile:
                    lines = hostfile.readlines()
                    hostfile.seek(0)
                    for line in lines:
                        if not any(site in line for site in sites_to_block):
                            hostfile.write(line)
                    hostfile.truncate()

            time.sleep(300) # Check every 5 minutes
            
        except PermissionError:
            print("🛑 ERROR: You MUST run this as Administrator/Root!")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            break

if __name__ == "__main__":
    sites, start, end = get_user_config()
    block_websites(sites, start, end)