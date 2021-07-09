

name = "COOPER_IS_COOL_32"
i = len(name) - 1
while i >= 0:
    if name[i] == "_":
        name = name[0:i]
        break
    i -= 1

print(name)

# Convert result to text format and then difference them in excel

# 2.6.9