strings = ["khokho", "amaama"]


def is_symmetrical(string: str) -> None:
    # string must be even length to potentially be symmetrical
    string_len = len(string)
    if string_len % 2 == 0:
        first_half = string[: int(string_len / 2)]
        second_half = string[int(string_len / 2) :]
        if first_half == second_half:
            print(f"{string} is symmetrical!")
        else:
            print(f"{string} is NOT symmetrical!")
    else:
        print(f"{string} is NOT symmetrical!")


def is_palindrome(string: str) -> None:
    rev_string = string[::-1]
    if string == rev_string:
        print(f"{string} is a palindrome!")
    else:
        print(f"{string} is NOT a palindrome!")


for s in strings:
    is_symmetrical(s)
    is_palindrome(s)
