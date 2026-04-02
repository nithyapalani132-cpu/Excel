expression = input("expression")
x,y,z = expression.split()
x = float(x)
z = float(z)
if y == "+":
    result = x + zexpression
elif y == "/":
    result = x / z
elif y == "-":
    result = x - z
else :
     result = x * z
print(f"{result:.1f}")
