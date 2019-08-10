from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
import math
import os
import random
import secrets
import sys
import time


# task 1: testing cryptography module
key = Fernet.generate_key()
cipher_suite = Fernet(key)

ciphertext = cipher_suite.encrypt(b"Sample message")
plaintext = cipher_suite.decrypt(ciphertext)


# task 2
def estimate_pi(is_crypto_rng: bool, num_of_samples: int):
    times_gcd_is_one: int = 0
    for i in range(num_of_samples):
        x, y = generate_random_numbers(is_crypto_rng)
        # the probability that gcd(x, y) = 1 is 6/pi^2

        gcd = math.gcd(x, y)
        if gcd == 1:
            times_gcd_is_one += 1
    ratio = float(times_gcd_is_one / num_of_samples)
    pi: float = math.sqrt(6 / ratio)
    return pi


def generate_random_numbers(is_crypto_rng: bool):
    if is_crypto_rng:
        x = secrets.randbelow(sys.maxsize)
        y = secrets.randbelow(sys.maxsize)
    else:
        x = random.randint(0, sys.maxsize)
        y = random.randint(0, sys.maxsize)
    return x, y


# task 3
def aes_file_encryption(file_name: str, key_size: int):
    with open(file_name + '.txt', 'rb') as file:
        file_contents = file.read()

    secret_key = secrets.token_bytes(int(key_size / 8))
    init_vector = secrets.token_bytes(16)
    cipher = Cipher(algorithms.AES(secret_key), modes.CBC(init_vector), default_backend())

    encryptor = cipher.encryptor()
    encryption = encryptor.update(file_contents) + encryptor.finalize()

    encrypted_file_name = file_name + '_aes_encrypted.txt'
    with open(encrypted_file_name, 'wb') as file:
        file.write(encryption)

    decryptor = cipher.decryptor()
    decryption = decryptor.update(encryption) + decryptor.finalize()

    decrypted_file_name = file_name + '_aes_decrypted.txt'
    with open(decrypted_file_name, 'wb') as file:
        file.write(decryption)


def rsa_file_encryption(file_name: str, key_size_input: int):
    key_size = 8 * key_size_input
    if key_size < 1024:
        key_size = 1024

    with open(file_name + '.txt', 'rb') as file:
        file_contents = file.read()

    # generate private-public key pair
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=key_size,
                                           backend=default_backend())
    public_key = private_key.public_key()
    encrypted_file = public_key.encrypt(file_contents, padding.OAEP(padding.MGF1(hashes.SHA256(

    )), hashes.SHA256(), None))

    with open(file_name + '_rsa_encrypted.txt', 'wb') as file:
        file.write(encrypted_file)

    decrypted_file = private_key.decrypt(encrypted_file, padding.OAEP(padding.MGF1(hashes.SHA256(

    )), hashes.SHA256(), None))

    with open(file_name + '_rsa_decrypted.txt', 'wb') as file:
        file.write(decrypted_file)


def generate_file(file_name: str, file_size: int):
    with open(file_name + '.txt', 'wb') as file:
        file.write(os.urandom(file_size))


def aes_encryptions_in_1_sec(key_size, file_name):
    num_of_encryptions = 0
    elapsed_time = 0
    start_time = time.time()
    while elapsed_time < 1.0:
        aes_file_encryption(file_name, key_size)
        num_of_encryptions += 1
        elapsed_time = time.time() - start_time
    print(file_name, "was encrypted & decrypted with AES", key_size, "bits", num_of_encryptions,
          "times in 1 sec")


def max_byte_encryption_in_1_sec(encryption_name, increment, initial_size):
    size = initial_size
    elapsed_time = 0.0
    while elapsed_time < 1.0:
        size += increment
        file_name = encryption_name + '_file'
        generate_file(file_name, size)
        start_time = time.time()
        if encryption_name == "AES_128":
            aes_file_encryption(file_name, 128)
        if encryption_name == "AES_256":
            aes_file_encryption(file_name, 256)
        if encryption_name == "RSA":
            rsa_file_encryption(file_name, 258 + size)
        elapsed_time = time.time() - start_time
    print(size, "bytes maximum were encrypted & decrypted with", encryption_name, "within 1 sec")


def main():
# task 2
    sample_sizes = [1000, 10000, 100000, 1000000, 10000000]
    for size in sample_sizes:
        print("LCG pi estimate from", size, "random ints:", estimate_pi(False, size))
        print("Crypto RNG pi estimate from", size, "random ints:", estimate_pi(True, size))
        print("\n")

# task 3
    file_names = ["file0", "file1", "file2", "file3", "file4"]
    file_sizes = [16, 1024, 15600, 141312, 1000000]

    for index in range(len(file_names)):
        generate_file(file_names[index], file_sizes[index])

    for file_name in file_names:
        aes_encryptions_in_1_sec(128, file_name)
        aes_encryptions_in_1_sec(256, file_name)

    print("\n")

    max_byte_encryption_in_1_sec("AES_128", 12800, 6000000)
    max_byte_encryption_in_1_sec("AES_256", 12800, 6000000)
    max_byte_encryption_in_1_sec("RSA", 1, 0)


main()
