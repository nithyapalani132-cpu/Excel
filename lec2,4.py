def is_valid(s):
    if len(s) < 2 or len(s) > 6:
        return False

    if not s[0].isalpha() or not s[1].isalpha():
        return False

    if not s.isalnum():
        return False

    digit_started = False

    for char in s:
        if char.isdigit():
            if not digit_started:
                if char == "0":
                    return False
                digit_started = True
        else:
            if digit_started:
                return False

    return True