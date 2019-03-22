messages = []


class Message:
    def __init__(self, message_id, subject, message, created_on, status):
        self.message_id = message_id
        self.subject = subject
        self.message = message
        self.created_on = created_on
        self.status = status

    def get_details(self):
        return {
            "message_id": self.message_id,
            "subject": self.subject,  
            "message": self.message,
            "created_on": self.created_on,
            }



