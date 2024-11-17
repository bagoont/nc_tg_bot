from sqlalchemy import UUID


class UserBaseError(Exception):
    def __init__(self, user_id: UUID):
        self.user_id = user_id
        super().__init__(self.message)


class UserNotFoundError(UserBaseError):
    """Exception raised when a user is not found in the system."""

    def __init__(self, user_id: UUID):
        self.message = f"User with ID {self.user_id} not found."
        super().__init__(user_id)


class UserAlreadyExistsError(UserBaseError):
    """Exception raised when a user already exists in the system."""

    def __init__(self, user_id: UUID):
        self.message = f"User with ID {self.user_id} already exists."
