"""
Dynamic outbound calling script for Vapi.

This script is based on the user's provided `outbound-calling.py`, but it has been
refactored to remove the hard‑coded customer phone number. Instead, the phone
number can be passed as a command‑line argument or programmatically when
imported as a module. This makes it easy to trigger calls for different reps
based on a schedule (e.g., from a CSV file).

Usage (command line):

    python outbound_call_dynamic.py --phone +14085551234

When run, the script will read the Vapi API key from the environment variable
`VAPI_API_KEY`; if not set, it falls back to the API key defined in the
constant `DEFAULT_API_KEY`. It then creates a call using the provided phone
number, along with the configured `PHONE_NUMBER_ID` and `ASSISTANT_ID` values.

You can import this module in another script and call the `create_call`
function directly, e.g.:

    from outbound_call_dynamic import create_call
    create_call("+14085551234")
"""

import os
import argparse
from dotenv import load_dotenv
from vapi import Vapi

# Load environment variables from .env file if present
load_dotenv()

# Fallback API key used if VAPI_API_KEY is not set in the environment
DEFAULT_API_KEY = "151677fc-bf97-435c-a381-de2cdc1c5876"

# Static identifiers for Vapi (should not change per call)
PHONE_NUMBER_ID = "dce2c662-f43e-477d-ba2b-3e38f4f37510"
ASSISTANT_ID = "343ccd2f-7ca9-40f3-8da7-1ba53254553a"

def get_api_key() -> str:
    """Retrieve the Vapi API key from environment or fallback."""
    return os.getenv("VAPI_API_KEY", DEFAULT_API_KEY)

def create_call(phone_number: str) -> None:
    """Create an outbound call for the given phone number.

    Args:
        phone_number: The customer's phone number, including country code
                      (e.g., '+14085551234').
    """
    api_key = get_api_key()
    if not api_key:
        raise ValueError("❌ VAPI_API_KEY not found. Please set it in the environment or DEFAULT_API_KEY.")

    # Initialize Vapi client
    vapi = Vapi(token=api_key)

    # Create an outbound call
    call = vapi.calls.create(
        phone_number_id=PHONE_NUMBER_ID,
        customer={"number": phone_number},
        assistant_id=ASSISTANT_ID,
    )
    print(f"Call created: {call.id} for number {phone_number}")

def main() -> None:
    parser = argparse.ArgumentParser(description="Create a Vapi outbound call with a dynamic phone number")
    parser.add_argument(
        "--phone",
        required=True,
        help="Customer phone number, including country code (e.g. +14085551234)",
    )
    args = parser.parse_args()
    create_call(args.phone)

if __name__ == "__main__":
    main()
