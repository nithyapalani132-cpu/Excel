name=input("File  name: ")
name=name.strip().lower()
if name.endswith(".gif"):
    print("image/gif")
elif name.endswith(".jpg") or  name.endswith(".jpeg"):
    print("image/jpeg")
elif name.endswith(".pdf"):
    print("application/pdf")
elif name.endswith(".png"):
    print("image/png")
elif name.endswith(".zip"):
      print("application/zip")
elif name.endswith(".txt"):
      print("text/plain")
else:
    print("application/octet-stream")