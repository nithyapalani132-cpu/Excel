from jar import Jar

def test_init():
    jar = Jar()
    assert jar.size == 0
    assert jar.capacity == 12

    jar2 = Jar(5)
    assert jar2.size == 0
    assert jar2.capacity == 5

def test_str():
    jar = Jar()
    assert str(jar) == ""
  
    jar.deposit(1)
    assert str(jar) == "🍪"

    jar.deposit(11)
    assert str(jar) == "🍪" * 12

def test_deposit():
    jar = Jar(5)
    jar.deposit(3)
    assert jar.size == 3

    try:
        jar.deposit(3)
    except ValueError:
        pass
    else:
        assert False, "Overfilling should raise ValueError"

    try:
        jar.deposit("a")
    except ValueError:
        pass
    else:
        assert False, "Non-int deposit should raise ValueError"


def test_withdraw():
    jar = Jar()
    jar.deposit(3)
    jar.withdraw(2)
    assert jar.size == 1


    try:
        jar.withdraw(5)
    except ValueError:
        pass
    else:
        assert False, "Over-withdraw should raise ValueError"

if __name__ == "__main__":
    test_init()
    test_str()
    test_deposit()
    test_withdraw()
    print("All tests passed!")