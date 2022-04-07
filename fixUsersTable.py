from cryptography.fernet import Fernet

def keyLoader():
    with open('key.bin', 'r') as keyFile:
        key = keyFile.read()
    fernet = Fernet(key)
    return fernet

def fixUsers():
    with open("usersBackup.json", 'r') as file:
        data = file.read()
    fernet = keyLoader()
    print(data)
    encMess = fernet.encrypt(data.encode())

    with open('users.bin', 'wb') as file:
        file.write(encMess)

if __name__ == '__main__':
    fixUsers()
    # with open("users.bin", 'rb') as file:
    #     data = file.read()
    # fernet = keyLoader()
    # decMess = fernet.decrypt(data)
    # print(decMess)