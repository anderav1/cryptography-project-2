# Cryptography Project 2: Coding with a Cryptographic Library
## Task 1
The goal of this task was to choose a programming environment and a cryptographic library. I decided to use Python and its associated `cryptography` module for this project since I had some previous knowledge of Python and `cryptography` was easy to implement. I installed the `cryptography` and `gpg` modules, then tested the functionality by writing some simple code that generated a key, encrypted some plaintext, and decrypted the resulting ciphertext.

---

## Task 2
The goal of the second task was to test the randomness of two pseudorandom number generators, a linear congruential generator and a cryptographic random number generator, by estimating the value of pi. Given two randomly chosen integers *x* and *y*, the probability that gcd(*x*, *y*) = 1 is 6/pi^2, so for each PRNG, I generated a number of random integer pairs and calculated what fraction of the pairs had a GCD of 1, then used this value to solve for pi.
For the LCG, I used Python's `random` module, which has a `randint(a, b)` function that generates a pseudorandom integer within the range [a, b]. I set the range from 0 to my OS's maximum number size. 
For the cryptographic random number generator, I used the secrets module's `randbelow(x)` function, where x is the maximum value of a generated integer. I set the maximum value to my OS's max number size again.
I wrote an `estimate_pi` function that took in an integer parameter to determine the amount of number pairs to generate, then tested the function on both generators with various sample sizes. One sample output was as follows:

    LCG pi estimate from  1000  random ints:  3.143990895015552
    Crypto RNG pi estimate from  1000  random ints:  3.1517891481565017


    LCG pi estimate from  10000  random ints:  3.139597498005517
    Crypto RNG pi estimate from  10000  random ints:  3.1429554953843066


    LCG pi estimate from  100000  random ints:  3.1426450749161794
    Crypto RNG pi estimate from  100000  random ints:  3.1462204738180137


    LCG pi estimate from  1000000  random ints:  3.138550973210049
    Crypto RNG pi estimate from  1000000  random ints:  3.1394505089387197


    LCG pi estimate from  10000000  random ints:  3.141173640718133
    Crypto RNG pi estimate from  10000000  random ints:  3.1414776830825177

For the smaller input sizes, the LCG and the cryptographic RNG seemed to perform similarly. As the sample size input increased, the pi estimate for both generators became more accurate; however, the cryptographic RNG became much more precise in its estimation for larger sample sizes.

---

## Task 3
The **first goal** of the third task was to determine, for files of various sizes, how many times AES encryption and decryption could be performed within a second using a 128-bit key and using a 256-bit key. I generated the keys using the `token_bytes` function from the `secrets` module, which provides functionality for securely generating random values. Then I wrote a function that would read a file's binary contents, then use AES to encrypt the contents and decrypt the result. I used this function in a loop that executed until the elapsed time reached 1.0 s.
Sample output from the first goal:

    file0 was encrypted & decrypted with AES 128 bits 66 times in 1 sec
    file0 was encrypted & decrypted with AES 256 bits 64 times in 1 sec
    file1 was encrypted & decrypted with AES 128 bits 77 times in 1 sec
    file1 was encrypted & decrypted with AES 256 bits 49 times in 1 sec
    file2 was encrypted & decrypted with AES 128 bits 25 times in 1 sec
    file2 was encrypted & decrypted with AES 256 bits 35 times in 1 sec
    file3 was encrypted & decrypted with AES 128 bits 54 times in 1 sec
    file3 was encrypted & decrypted with AES 256 bits 43 times in 1 sec
    file4 was encrypted & decrypted with AES 128 bits 27 times in 1 sec
    file4 was encrypted & decrypted with AES 256 bits 41 times in 1 sec

In general, AES encryption with a 256-bit key took longer than AES encryption with a 128-bit key, but this was not true for every instance. In this case, the 256-bit key processed more data than the 128-bit key. 

The **second goal** of this task was to determine the maximum size of a file that could be encrypted/decrypted with AES in one second. I utilized my AES file encryption function again in a loop that would increase the file size each time it executed until the elapsed time of the encryption and decryption of the file reached 1.0 s.
The **third goal** of this task was to repeat the second goal for RSA encryption. I generated the public-private key pair from the `rsa` module in the `cryptography` library. I wrote an RSA file encryption function and used it in a loop identical to the loop from the second goal.
One instance of output from the second and third goals:

    15766400 bytes maximum were encrypted & decrypted with AES_128 within 1 sec
    20540800 bytes maximum were encrypted & decrypted with AES_256 within 1 sec
    1 bytes maximum were encrypted & decrypted with RSA within 1 sec

RSA encryption took significantly longer than AES. I did several trials, and each time, 1 to 8 bytes of data were processed by RSA within 1 second, whereas several megabytes of data were processed by AES.