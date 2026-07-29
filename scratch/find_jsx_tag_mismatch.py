with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Let's inspect lines 4145 to 4276
print("Lines 4145 to 4158:")
for i in range(4144, 4158):
    print(f"{i+1}: {lines[i].rstrip()}")

print("\nLines 4260 to 4276:")
for i in range(4259, 4276):
    print(f"{i+1}: {lines[i].rstrip()}")
