import base64

with open(f"faces/Alexandros Aspiotis/WIN_20220221_10_35_27_Pro.jpg", "rb") as f:
    converted = base64.b64encode(f.read())

with open(f"faces/Alexandros Aspiotis/encoded.bin", "wb") as f:
    f.write(converted)