text = input("Greeting: ").strip().lower()
match text:
    case "hello" | "hello, newman":
          print("$0")
    case "hey" | "how you doing?" | "how's it going?":
          print("$20")
    case "what's happening?" | "what's up?":
          print("$100")
    case _:
          print("$200")