#!/usr/bin/env python3

from random import randint
from string import digits, ascii_letters, punctuation
from ast import literal_eval

SYMBOLS = digits + ascii_letters + punctuation

DISCLAIMER = """scrambler.py - This tool is made for entertainment purposes only and is
NOT intented for secure communication.
If you wish to communicate privately, use PGP"""

def create_dictionary():
    decrypt_dict = {}
    encrypt_dict = {}
    for letter in SYMBOLS:
        keep_finding = True
        while keep_finding:
            r = randint(0, len(SYMBOLS)-1  )
            cipher = SYMBOLS[r]
            if decrypt_dict.get(cipher) is None:
                decrypt_dict[cipher] = letter
                encrypt_dict[letter] = cipher
                keep_finding = False
            #print("Duplicate cipher " + cipher)
    return decrypt_dict, encrypt_dict

def input_to_eot():
    continue_input = True
    text = ""
    while continue_input:
        try:
            line = str(input(">"))
            text += line
        except EOFError:
            print()
            continue_input = False
    return text

def decrypt(cipher_text, decrypt_dict):
    cleartext = ""
    for ch in cipher_text:
        #TODO Validate that char is supported
        cleartext += decrypt_dict.get(ch, "")
    return cleartext

def cli_decrypt(decrypt_dict):
    cipher_text = input_to_eot()
    return decrypt(cipher_text, decrypt_dict)

def encrypt(cleartext, encrypt_dict):
    cipher_text = ""
    for c in cleartext:
        #TODO Validate that char is supported
        cipher_text += encrypt_dict.get(c, "")
    return cipher_text

def cli_encrypt(encrypt_dict):
    cleartext = input_to_eot()
    return encrypt(cleartext, encrypt_dict)

def cli_import_mapping():
    mapping = input_to_eot()
    encrypt_dict = literal_eval(mapping)
    decrypt_dict = {}
    for (k, v) in encrypt_dict.items():
        decrypt_dict[v] = k
    return encrypt_dict, decrypt_dict

def main():
    print(DISCLAIMER)
    decrypt_dict, encrypt_dict = create_dictionary()
    run = True
    while run:
        try:
            command = str(input("scrambler> "))
            if command in ("?", "h", "help"):
                print("encrypt, decrypt, help, end, export, import, regenerate, disclaimer")
            elif command == "end":
                print("Exiting!")
                run = False
            elif command == "decrypt":
                print("CTRL+D to end transmittion")
                output = cli_decrypt(decrypt_dict)
                print(output)
            elif command == "encrypt":
                print("CTRL+D to end transmittion")
                output = cli_encrypt(encrypt_dict)
                print(output)
            elif command == "export":
                print(encrypt_dict)
            elif command == "import":
                encrypt_dict, decrypt_dict = cli_import_mapping()
            elif command == "regenerate":
                decrypt_dict, encrypt_dict = create_dictionary()
                print("Scrambler regenerated")
            elif command == "disclaimer":
                print(DISCLAIMER)
            else:
                print("Invalid command. type 'help' for usage")
        except KeyboardInterrupt:
            print("CTRL+C Pressed. type 'end' to quit!")
        except EOFError:
            print("CTRL+D Pressed. type 'end' to quit!")

if __name__ == "__main__":
    from sys import version
    if version.startswith('2'):
        print("Python 2 is not supported. Please use Python 3!")
        from sys import exit
        exit(1)
    main()


