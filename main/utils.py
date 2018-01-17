def get_account_user_display(user):
    if user.extendsuser.nickname:
        return user.extendsuser.nickname
    else:
        return user.username
