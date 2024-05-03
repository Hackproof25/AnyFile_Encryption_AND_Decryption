import base64
import os
from colorama import init, Fore, Style
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

init(autoreset=True)  # Initialize colorama with auto-reset


def derive_key(password):
    # Salt is added to the password for added security
    salt = b'salt_'  # You can customize the salt value
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,  # You can adjust the number of iterations as needed
    )
    key = kdf.derive(password.encode())
    return base64.urlsafe_b64encode(key)


def encrypt_file(filename, password):
    key = derive_key(password)
    fernet = Fernet(key)
    with open(filename, 'rb') as file:
        file_data = file.read()
    encrypted_data = fernet.encrypt(file_data)
    encrypted_filename = filename + '.encrypted'
    with open(encrypted_filename, 'wb') as file:
        file.write(encrypted_data)
    print(Fore.GREEN + Style.BRIGHT + f"File encrypted successfully. Encrypted file saved as: {encrypted_filename}")


def decrypt_file(filename, password):
    key = derive_key(password)
    fernet = Fernet(key)
    with open(filename, 'rb') as file:
        encrypted_data = file.read()
    try:
        decrypted_data = fernet.decrypt(encrypted_data)
        decrypted_filename = os.path.splitext(filename)[0]  # Remove the '.encrypted' extension
        with open(decrypted_filename, 'wb') as file:
            file.write(decrypted_data)
        print(Fore.GREEN + Style.BRIGHT + f"File decrypted successfully. Decrypted file saved as: {decrypted_filename}")
    except Exception as e:
        print(Fore.RED + Style.BRIGHT + "Decryption error:", e)


def increase_text_size(text):
    return f"\033[1m{text}\033[0m"


def main():
    print(Fore.CYAN + increase_text_size("""
    
  ______ _   _  _____ _______     _______ _______             _____  ______ _____ _______     _______ _______ 
 |  ____| \ | |/ ____|  __ \ \   / /  __ \__   __|   ___     |  __ \|  ____/ ____|  __ \ \   / /  __ \__   __|
 | |__  |  \| | |    | |__) \ \_/ /| |__) | | |     ( _ )    | |  | | |__ | |    | |__) \ \_/ /| |__) | | |   
 |  __| | . ` | |    |  _  / \   / |  ___/  | |     / _ \/\  | |  | |  __|| |    |  _  / \   / |  ___/  | |   
 | |____| |\  | |____| | \ \  | |  | |      | |    | (_>  <  | |__| | |___| |____| | \ \  | |  | |      | |   
 |______|_| \_|\_____|_|  \_\ |_|  |_|      |_|     \___/\/  |_____/|______\_____|_|  \_\ |_|  |_|      |_| 
    
    """))

    while True:
        file_location = input(
            Fore.YELLOW + "Enter the full path of the file you want to work with (or 'exit' to quit): ").strip().replace(
            'file://', '')

        file_location = file_location.strip('"')  # Remove leading and trailing double quotes from the path

        if file_location.lower() == 'exit':
            print(Fore.YELLOW + "Exiting the program.")
            break

        password = input(Fore.YELLOW + "Enter your password for encryption/decryption: ")

        action_choice = input(Fore.YELLOW + "Do you want to encrypt (E) or decrypt (D) the file? (E/D): ").upper()

        if action_choice == 'E':
            encrypt_file(file_location, password)
        elif action_choice == 'D':
            decrypt_file(file_location, password)
        else:
            print(Fore.RED + Style.BRIGHT + "Invalid choice. Please choose 'E' for encryption or 'D' for decryption.")


if __name__ == "__main__":
    main()
