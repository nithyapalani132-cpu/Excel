def main():
  meal= convert(input("What time is it?"))
  if 7.0 <= meal <= 8.0:
      print("breakfast time")
  elif 12.0 <= meal <= 13.0:
      print("lunch time")
  elif 18.0 <= meal <= 19.0:
      print("dinner time")
  else:
      print("close time")



def convert(time):
    hours,minutes = time.split(":")
    h = float(hours)
    m = float(minutes)
    return h+(m/60)


if __name__ == "__main__":
    main()