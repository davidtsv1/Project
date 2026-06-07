import random
import string

try:
    import pyperclip
    HAS_PYPERCLIP = True
except ImportError:
    HAS_PYPERCLIP = False


def generate_password(length, use_upper, use_digits, use_symbols):
    chars = list(string.ascii_lowercase)
    required = [random.choice(string.ascii_lowercase)]

    if use_upper:
        chars += list(string.ascii_uppercase)
        required.append(random.choice(string.ascii_uppercase))
    if use_digits:
        chars += list(string.digits)
        required.append(random.choice(string.digits))
    if use_symbols:
        symbols = "!@#$%^&*()-_=+[]{}|;:,.<>?"
        chars += list(symbols)
        required.append(random.choice(symbols))

    remaining = [random.choice(chars) for _ in range(length - len(required))]
    password = required + remaining
    random.shuffle(password)
    return "".join(password)


def ask_yes_no(prompt):
    return input(prompt + " (y/n): ").strip().lower() == "y"


def main():
    print("\n=== Password Generator ===\n")

    while True:
        try:
            length = int(input("Password length (8-64): ").strip())
            if not 8 <= length <= 64:
                print("  Must be between 8 and 64.")
                continue
            break
        except ValueError:
            print("  Enter a number.")

    use_upper = ask_yes_no("Include uppercase letters?")
    use_digits = ask_yes_no("Include numbers?")
    use_symbols = ask_yes_no("Include symbols?")

    passwords = [generate_password(length, use_upper, use_digits, use_symbols) for _ in range(5)]
    print("\n" + "=" * 40)
    for i, pw in enumerate(passwords, 1):
        print(f"  {i}. {pw}")
    print("=" * 40)

    choice = input("\nCopy which password to clipboard? (1-5, or skip): ").strip()
    if choice in {"1", "2", "3", "4", "5"}:
        selected = passwords[int(choice) - 1]
        if HAS_PYPERCLIP:
            pyperclip.copy(selected)
            print(f"  Copied to clipboard: {selected}")
        else:
            print(f"  pyperclip not installed. Run: pip install pyperclip")
            print(f"  Your password: {selected}")

    print("\nGenerate another? ", end="")
    if input().strip().lower() == "y":
        main()
    else:
        print("Goodbye!")


if __name__ == "__main__":
    main()