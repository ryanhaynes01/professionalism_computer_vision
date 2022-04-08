import database_handler as db

# TODO:
# Add tokens for proof of id security
# Add encryption and decrpytion of data
# Add Data Classes to ensure security

class Authenticator:
    def __init__(self):
        self._token = ""
        self._db = db.DatabaseHandler()

    def users_info(self, id, reference, provided, password):
        try:
            user_info = self._db.get_user(id, reference, provided)
            user_info = list(user_info[0])
            other_temp = self._db.handler("view_specific", ["username"])
            other_info = []
            
            for user in other_temp:
                other_info.append(user[0])

            if user_info[0] in other_info:
                return self.authenticate_user(user_info[0], password)

        except Exception as e:
            print(e)

    def authenticate_user(self, username, password):
        hierarchy = self._db.get_user("Hierarchy", "username", username)
        name = self._db.get_user("Name", "username", username)
        info = self._db.get_user("password", "username", username)
        if info[0][0] == password:
            return [True, hierarchy[0][0], name[0][0]]
        else:
            return [False, hierarchy, name]

    def generate_token(self):
        pass

if __name__ == '__main__':
    a = Authenticator()
    a.users_info("username, password", "username", "ryanhaynes01")