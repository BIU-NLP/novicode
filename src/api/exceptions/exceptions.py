from exceptions import recovery as recovery_commands


def exception_handler(func):
    def inner_function(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except NoSuchValueException as e:
            user_response = recovery_commands.recover_prompter(prompt=e.recovery_prompt)
            kwargs = {**kwargs, **user_response.payload}
            return func(*args, **kwargs)
        except UnderspecificationException as e:
            user_response = recovery_commands.recover_prompter(prompt=e.recovery_prompt)
            kwargs = {**kwargs, **user_response.payload}
            return func(*args, **kwargs)
    return inner_function


class NoSuchValueException(Exception):
    recovery_prompt: str
    
    def __init__(self, payload, recovery_prompt, message="No such value exception") -> None:
        super().__init__(message)
        self.recovery_prompt = recovery_prompt
        self.payload = payload

class UnderspecificationException(Exception):
    recovery_prompt: str
    
    def __init__(self, payload, recovery_prompt, message="UnderspecificationException exception") -> None:
        super().__init__(message)
        self.recovery_prompt = recovery_prompt
        self.payload = payload

    