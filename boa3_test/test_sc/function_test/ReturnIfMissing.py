def Main(number: int) -> int:
    if number % 2 == 1:
        number -= 1  # the function doesn't have return in this case
    else:
        return number
