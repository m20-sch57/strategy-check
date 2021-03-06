import server.storage as storage
from app.forms import LoginForm

def Login(form: LoginForm) -> list:
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = storage.storage.getUserByName(username)
        if user == None:
            return [0, ("There is no registred user with this username", 'message red'), "Guest", "-1"]
        if user.password != password:
            return [0, ("Incorrect password", 'message red'), "Guest", "-1"]
        return [1, ("Logged in successfully", 'message green'), username, str(user.id)]
    return [0, ("You must fill all fields", 'message blue'), "Guest", "-1"]

