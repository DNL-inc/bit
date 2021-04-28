def get_current_user():
    def decorator(func):
        setattr(func, 'get_current_user', True)
        return func
    return decorator