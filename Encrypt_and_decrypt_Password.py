import random


def encrypt(message):
    '''
    This function encrypt the message

    **Parameters**

        message: *str*
                The password to encrypt

    **return**
        encryptcode: *int*
                    a list of int codes generated
    '''

    a = []
    for i in message:
        M = ord(i)
        a.append(M)
        encryptcode = [(element**E) % N for element in a]
    return encryptcode


def decrypt(code):
    '''
    This function encrypt the message

    **Parameters**

        code: *int*
            A list of code encrypted from encrypt()function

    **Print**
        A sting of words that is dencrypted by decrypt() function
    '''

    b = []
    for j in code:
        MM = (j ** D) % N
        b.append(chr(MM))
    print("Password:", ''.join(b))


def generate_key():
    '''
    A function to call that starts the key generation
        N = P ∗ Q (P, Q primes > 130).
        X =(P −1)(Q−1)
        E < X (prime divisors of E are not contained in X)
        Use "while True" loop to find the best fit number

    **return**
        N, E, D: *int*
                Keys for encrypt()function
    '''

    P = get_primes_in_range(131, 300)
    Q = get_primes_in_range(131, 300)
    N = P * Q
    X = (P-1)*(Q-1)
    XX = get_prime_divisors(X)
    while True:
        E = random.randint(0, X)
        EE = get_prime_divisors(E)
        if common_data(XX, EE) == 0:
            break

    while True:
        D = random.randint(0, 100000)
        if (D*E) % (X) == 1:
            break

    return N, E, D


def get_prime_divisors(N):
    '''
    A function that finds all prime divisors of a given number

    **Parameters**
        N: *int*
            The number for gettig all its divisors

    **return**
        q: *int*
            A list of num which are the prime divisors of N
    '''

    q = []
    l = 1
    while (l <= N):
        count = 0
        if (N % l == 0):
            m = 1
            while (m <= l):
                if(l % m == 0):
                    count = count+1
                m = m + 1
            if (count == 2):
                q.append(l)
        l = l + 1
    return q


def get_primes_in_range(low, high):
    '''
    A function that finds all prime numbers in the given range (low, high)

    **Parameters**
        low, high: *int*
            The value of range user set up to find a random prime number

    **return**
        g: *int*
            A random prime number
    '''

    while True:
        g = random.randint(low, high)
        if is_prime(g) == 1:
            break
    return g


def is_prime(p):
    '''
    A function that checks if a given number is prime or not

    **Parameters**
        p: *int*
            The num to check is prime or not

    **return**
        0 or 1: 0 means not a prime; 1 means a prime
    '''

    if p > 1:
        for i in range(2, p):
            if (p % i) == 0:
                return 0
        else:
            return 1


def common_data(list1, list2):
    '''
    A function I create to help check if the prime division number of E
    and X over lap, since X does not contain E prime devisors

    **Parameters**
        list1, list2: *int*
            The two list to compare, whether they share numbers

    **return**
        0 or 1: 0 means no overlap; 1 means overlap
    '''

    for x in list1:
        for y in list2:
            if x == y:
                return 1
    return 0


if __name__ == "__main__":
    N, E, D = generate_key()
    message = "Your Device Is Invaded"
    code = encrypt(message)
    print("Encrypted code:", encrypt(message))
    decrypt(code)
    print("N, E, D:", generate_key())
