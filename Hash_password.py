import hashlib
import os


def hash_password(passwd, salt):
    return hashlib.pbkdf2_hmac('sha512', passwd.encode('utf-8'), salt, 100000)


'''
    Create a function to hash pasword
'''


login_credentials = {"hherbol1": "Fifa", "dungyiwu": 'Guww'}
database = {}
for (key, value) in login_credentials.items():
    salt = os.urandom(8)  # Randomized data
    passwd = hash_password(value, salt)
    database[key] = [passwd, salt]

'''
    1. Create a database to store usernames,
    2. Use ForLoop to salt the password and store the username(Key) 
    and corresponding password and salt(Value) in the dictionary   
'''


def encrypt(msg, N=17947, E=7):
    return [pow(ord(s), E, N) for s in msg]


def password(msg, usr, passwd):
    def decrypt(msg, N=17947, D=10103):
        return ''.join([chr(pow(s, D, N)) for s in msg])

    # Your code that checks the username/password combination goes here
    # Store your usernames, salted password hashes and corresponding salts appropriately
    # Check if the username and password passed to it are correct # Return decrypted message

    if usr in database.keys():
        if database.get(usr)[0] == hash_password(passwd, database.get(usr)[1]):
            return decrypt(msg)
        else:
            return "Incorrect password"
    else:
        return "User not exists"


'''
    Compare if the usr name is in the dictionary and confirm the password   
    **return**
        The result of the comparison *str*
'''


def start_messenger(msg_fptr, N=17947, E=7):

    # code starts the messenger
    # reads in each line of messages input by the user , encrypts each line
    # and stores them in a list
    # Each line of encrypted text is then written to a file , the name of which
    # is stored in msg fptr and is passed to the function when the function
    # is called

    # Write the encrypted messages into file
    with open(msg_fptr, 'w') as file:
        while True:
            msg = input('Write the messages: ')
            encrypted_msg = ' '.join(map(str, encrypt(msg, N, E)))
            if msg == 'STOP':
                break
            file.write(encrypted_msg + '\n')


'''
    1. open a txt file using write mode
    2. imput the message
    3. using map function to encrypt messages and seperarte messages with space
'''


def read_messages(msg_fptr, N=17947, D=10103):

    # starts off by asking the user for a username and password
    # start reading the encrypted text stored in the passed text file
    # if the correct username and password combination is entered
    # decrypt the text file

    # Ask the user's username and password
    usr = input('Enter your user name: ')
    passwd = input('Entre your password: ')

    # Create a LineList to store decrypted messages
    decrypted_msg = []

    # Decrypte
    encrypted_msg = [line.rstrip('\n')for line in open(msg_fptr)]
    for line in encrypted_msg:
        line = line.split(" ")  # Convert string into list
        line = password(map(int, line), usr, passwd)  # Decrypte messages
        decrypted_msg.append(line)  # Store the decrypted messages

    # Convert the LineList into String
    decrypted_msg = '\n'.join(line for line in decrypted_msg)

    return decrypted_msg


'''
    1. Input the user name and password
    2. read the message in the file 
    3. split the message
    4. decrypt the message and store it in a list
    **return**
        Tdecrypted_msg *str*
'''

if __name__ == '__main__':

    message = "This is a secret message"
    encrypted_message = encrypt(message)
    decrypted_message = password(encrypted_message, "hherbol1", "Fifa")
    assert message == decrypted_message, "Error − Decryption failed!"

    # This will start a messaging app that will allow me to add in as many messages
    # as I want. It will encrypt it with a default N and E, and save it to the specified
    # file (in this case , messages.txt).
    start_messenger("messages.txt")

    # This will prompt the user for a valid username-password combination.
    # It will then attempt to unencrypt the file for me (assuming username/password is valid), and
    # print out the results here.
    messages = read_messages("messages.txt", N=17947, D=10103)
    print(messages)
