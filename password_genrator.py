import random
import string

def generate_password(length):
    # Define the character sets to use
    lower = string.ascii_lowercase
    upper = string.ascii_uppercase
    digits = string.digits
    symbols = string.punctuation

    # Combine all sets
    all_chars = lower + upper + digits + symbols

    # Ensure the password has at least one of each type
    password = [
        random.choice(lower),
        random.choice(upper),
        random.choice(digits),
        random.choice(symbols)
    ]

    # Fill the rest of the password length with random choices
    if length > 4:
        password += [random.choice(all_chars) for _ in range(length - 4)]

    # Shuffle the list to ensure randomness and convert to string
    random.shuffle(password)
    return ''.join(password)

def main():
    print("--- Password Generator ---")
    
    while True:
        try:
            length_input = input("Enter the desired length of the password (min 4): ")
            length = int(length_input)

            if length < 4:
                print("Password length should be at least 4 characters for better security.")
            else:
                password = generate_password(length)
                print(f"\nGenerated Password: {password}")
                break
        except ValueError:
            print("Invalid input! Please enter a numeric value.")

if __name__ == "__main__":
    main()