keywords = ["telegram", "tiktok", "github", "instagram"]

with open("akado.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

print("\n=== CLEAN RESULTS ===\n")

for line in lines:
    for key in keywords:
        if key.lower() in line.lower():
            print(line.strip())