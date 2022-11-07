class User:
    all_users = dict()

    def __init__(self, user_id: int) -> None:
        self.user_id = user_id
        User.add_user(user_id=user_id, user=self)
        self.command: str = ""
        self.flag = False
        self.city: str = ""
        self.hotels_number_to_show: str = ""
        self.photos_num: str = ""
        self.arrival_date: str = ""
        self.departure_date: str = ""
        self.min_price: str = ""
        self.max_price: str = ""
        self.range: str = ""
        self.request_time: str = ""

    @classmethod
    def add_user(cls, user_id, user):
        cls.all_users[user_id] = user

    @classmethod
    def get_user(cls, user_id):
        if user_id in cls.all_users:
            return cls.all_users[user_id]
        User(user_id=user_id)
        return cls.all_users[user_id]
