import re

data = """user=admin
password=Example123
email=test@example.com
token=not_a_match
passwd:qwerty456
pwd=hello789
"""

pattern_wrong = r"(password|passwd|pwd)[=:]\S+"
pattern_fixed = r"(?:password|passwd|pwd)[=:]\S+"

print("=== SAMPLE DATA ===")
print(data)

print("=== WRONG PATTERN ===")
print("Pattern:", pattern_wrong)
print("Matches:", re.findall(pattern_wrong, data))

print("\n=== FIXED PATTERN ===")
print("Pattern:", pattern_fixed)
print("Matches:", re.findall(pattern_fixed, data))
