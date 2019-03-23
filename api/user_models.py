class User:
    # specifies user details
    def __init__(self, **kwargs):
        self.user_id = kwargs["user_id"]
        self.first_name = kwargs["first_name"]
        self.last_name = kwargs["last_name"]
        self.email = kwargs["email"]
        self.password = kwargs["password"]
    
        
