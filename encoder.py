import base64

with open(f"faces/Alex Tucker/IMG_0657.jpg", "rb") as f:
    converted = base64.b64encode(f.read())

with open(f"faces/Alex Tucker/encoded.bin", "wb") as f:
    f.write(converted)