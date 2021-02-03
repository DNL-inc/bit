def get_current_admin():
    def decorator(func):
        setattr(func, 'get_current_admin', True)
        return func
    return decorator
