import bcrypt
password = "uwu".encode('utf-8')
hashed = bcrypt.hashpw(password, bcrypt.gensalt()).decode('utf-8')
print(openssl rand -hex 12)

'''check = input()
if bcrypt.checkpw(check.encode('utf-8'), bytes(hashed, 'utf-8')):
    print("Yep!")
else:
    print("Nope :(")'''