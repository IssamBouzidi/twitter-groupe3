class Tweet:


    def __init__(self
                , id
                , user_name
                , user_location
                , language
                , entities
                , created_at):
        self.id = id
        self.user_name = user_name
        self.user_location = user_location
        self.language = language
        self.entities = entities
        self.created_at = created_at


    def to_json(self):

        return {"id": str(self.id)
                , "user_name": self.user_name
                , "user_location": self.user_location
                , "language" : self.language
                , "created_at" : self.created_at
                , "entities" : self.entities
                }

