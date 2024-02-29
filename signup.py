

def signup(username, password, email, first_name):

    if len(username) == 5 and len(password) == 3 and "@" in email and len(first_name) ==8:
        return True
    else:
        return False
