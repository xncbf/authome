def get_account_user_display(user):
    if user.extends_user.nickname:
        return user.extends_user.nickname
    else:
        return user.username
