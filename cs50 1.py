text = input("what is the answer to the great question of life,the universe,& everything?")
text = text.strip().lower()
if text == "42":
   print("Yes")
elif text == "forty-two":
   print("Yes")
elif text == "forty two":
   print("Yes")
else:
   print("no")
