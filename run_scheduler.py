"""
Schedule outbound calls based on a CSV of reps, phone numbers and call times.

This script reads a CSV file with columns `rep_name`, `phone_number` and
`time_of_call`, then schedules calls for each entry at the specified time
(America/Los_Angeles timezone). At the scheduled time, it invokes the
`create_call` function from `outbound_call_dynamic.py` to initiate the call.

Usage:

    python run_scheduler.py --csv sample_call_schedule.csv

The script runs indefinitely, checking for pending jobs every 30 seconds.
Make sure you have installed the required packages: pandas, schedule,
python-dotenv, vapi, pytz. You should also place `outbound_call_dynamic.py`
in the same directory or ensure it is importable.
"""

import argparse
from datetime import datetime
import time

import pandas as pd
import schedule
import pytz

from outbound_call_dynamic import create_call

def schedule_calls(csv_path: str) -> None:
    tz = pytz.timezone("America/Los_Angeles")
    df = pd.read_csv(csv_path)

    # Validate required columns
    required = {"rep_name", "phone_number", "time_of_call"}
    if not required.issubset(df.columns):
        raise ValueError(f"CSV must contain columns: {', '.join(required)}")

    for _, row in df.iterrows():
        rep_name = row["rep_name"]
        phone_raw = str(row["phone_number"]).strip()
        # Ensure phone number has a '+' prefix (assume US country code if missing)
        phone = phone_raw if phone_raw.startswith("+") else "+1" + phone_raw

        # Parse the call time (assumed PST) and format for schedule library
        call_time = datetime.strptime(row["time_of_call"], "%Y-%m-%d %H:%M")
        call_time_local = tz.localize(call_time)
        time_str = call_time_local.strftime("%H:%M")

        def job(number=phone, name=rep_name):
            print(f"[{datetime.now()}] Initiating call to {name} at {number}")
            create_call(number)

        # Schedule the job for every day at the specified time (PST)
        schedule.every().day.at(time_str).do(job)
        print(f"Scheduled call for {rep_name} at {time_str} PST")

    # Run the scheduler indefinitely
    print("Scheduler running. Press Ctrl+C to exit.")
    try:
        while True:
            schedule.run_pending()
            time.sleep(30)
    except KeyboardInterrupt:
        print("Scheduler stopped by user")

def main() -> None:
    parser = argparse.ArgumentParser(description="Schedule outbound calls from a CSV")
    parser.add_argument("--csv", required=True, help="Path to the call schedule CSV file")
    args = parser.parse_args()
    schedule_calls(args.csv)

if __name__ == "__main__":
    main()
