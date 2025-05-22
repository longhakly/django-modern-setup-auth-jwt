from datetime import datetime, timedelta


class UserUtils:
    @staticmethod
    def update_user_login_attemp(user_instance):
        login_attempt = user_instance.login_attempt + 1
        if login_attempt > 3:
            user_instance.punish_datetime = datetime.now() + timedelta(
                minutes=login_attempt * login_attempt // 3
            )

        user_instance.login_attempt = login_attempt
        user_instance.save()

    @staticmethod 
    def reset_user_login_attempt(user):
        user.login_attempt = 0
        user.save()