data = {"a": 10, "b": 25, "c": 15}

max_key = max(data, key=data.get)
print(max_key, data[max_key])