from google.cloud import storage
import json

# Hardcoded service account credentials
service_account_json = """
{
  "type": "service_account",
  "project_id": "able-stock-428615-n4",
  "private_key_id": "830353631691195f3e8133f404fa8c8a4e37e1d3",
  "private_key": "-----BEGIN PRIVATE KEY-----\\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDOgmOtTVyX+Ieo\\nL4wqTqTWBXpU4vOt/V3i392ZRlm8MC7uHALI4+zZ35VS7/kE4lAplnN8Wi25lR0d\\n01KCBgHLpsf64BxufIcTmgpqBUUhaZk1tVPOavl0qqXrTIPEqBh2nifgBHgwlsXj\\nqHj5408FUGZGODJffmcMa47cyKni/XBzbhTdwi0wDmJmiKmnpBZCl4OPlw57lJdo\\nGDZ/AKVO7UASaANaIQMHFku4HXSngLciVmWFpGOYBWTCO/gbkAhNMGPbhtsMoGru\\nlPfIuRHLsBG5is3LtsqqkKRTRqQz77eOh3KfvP+ITZ+Unpr7b6aihUqyYRH/QedD\\nYuqVefLzAgMBAAECggEAAzgCELnzdwTvLF5tW111cUaNlRQigzQ/SeF+ZTy0+ltv\\n59M08eenke/Ltoq6AWr7n+JR836+VrWtygC4uQEZ9xAm7tCecNRtEI+mmOdzH+Wy\\n9yTX5RBCyiA8zNGY/jA2jWbCrVm0e+FlvTorhI2X9je+GFsY4eco+QcWJ3fTOg/9\\nC7cZGaAydlakm2ol5ckR4845IYOaCikBcBibTt3HLAV9PQJJmiLjbPReKc1qR33b\\nn95raBI6F72mGYb2/9uybs6QGn/2WzHnGpGLbAvytYTfyqqIwee9UQa2LZA4MlD8\\nP68Z7q/T4VXMpjOq/wJcR0XVS+oFcIf85/9BdaUTsQKBgQDvqNzuczEB4GnY2AtP\\nC75DbYojm5CdF9oLvYYPrvRo/G+DeqX7Kj1lPqy582jSvACDcCxgcOZ9fso5KUoB\\nQNpEiJ2nm07PSY2H6CUoazyYnpM/TZg21gg0413B7l69bWQ/HWAkVenS+IXW1g0K\\nm/LyCgdMTt3dFCHKPoB/VhPkwwKBgQDclueoTWvuZ0yWEp+cCQwfjPkXV3WzfEb9\\nKv+RVFlqG/FUNqOuHHgWnfxF6mcsR/Ey4yXQ1K1RPkLamw8nZF87DuFzLojHbk1U\\nbyfC7+BHL/lIUw4tF2PY4CCp8AVolWEZyykn/3QM0YVgPSxkeLWlxrO7iebckIwk\\niouXwZUWEQKBgE88oW8lHrrkG5raM0L7OvjIKrgDIxkNXcYr7zsYOS7M54Gs91vH\\nZ20l/62rUKj8B59tYv6v1UUAupOTlyg67O9jy9wyeSgHxYd9tWtbqTk8lKqFWSIo\\nOaZi1gjcau5uUIqdh7/7t8dM69NQChfL39MuhaMxICGMGm/nokx3hTRJAoGAFpMv\\nBA9gU1apBNbFFN/sKLJxr4zY09SNI02qOAJM4EoZyYeJ+sCZHZ9veOxDQMngClgq\\nv5N0ZVMc3mhuBZcFE/My6WnCv74vFcwGYrHP3xkuxtMRKVYydriBP0L8Grbm6A/d\\nl2VSSBmNL8sy5tlfpaaPMEstoDb+0KKJJK/ABTECgYEAxu2ed4VMCopc3LV+gHvj\\nphT/8bIQ4DYoPoDABBUEoGzfGuRcsoO4WLI40nPfdrScAFx6RmkXhfZDiBOYQzFy\\n/ghTeTGg/GOWXFgKF15sxpvIRxgZaY9rE1uWj9laYmjbauu+TR9WbwCV2yUPTssB\\n4LR1k/VJsZDk4NivQj08Fqg=\\n-----END PRIVATE KEY-----\\n",
  "client_email": "my-service-account@able-stock-428615-n4.iam.gserviceaccount.com",
  "client_id": "110925674836167317764",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/my-service-account%40able-stock-428615-n4.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}
"""

# Parse the JSON string
credentials = json.loads(service_account_json)

# Use the credentials in the client
client = storage.Client.from_service_account_info(credentials)

# List all buckets
buckets = client.list_buckets()
print("Buckets:")
for bucket in buckets:
    print(f"- {bucket.name}")
