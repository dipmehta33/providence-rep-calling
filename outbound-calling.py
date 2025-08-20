import os
from dotenv import load_dotenv
from vapi import Vapi

# Load environment variables from .env file
load_dotenv()

# Get the API key
#api_key = os.getenv("VAPI_API_KEY")
api_key = "151677fc-bf97-435c-a381-de2cdc1c5876"

print(api_key)

if not api_key:
    raise ValueError("❌ VAPI_API_KEY not found. Please set it in the .env file.")

# Initialize Vapi
vapi = Vapi(token=api_key)

# Create an outbound call
call = vapi.calls.create(
    phone_number_id="dce2c662-f43e-477d-ba2b-3e38f4f37510",
    customer={"number": "+14084250666"},
    assistant_id="343ccd2f-7ca9-40f3-8da7-1ba53254553a"
)
print(f"Call created: {call.id}")

