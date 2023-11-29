from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, username, email, password):
        if not email:
            raise ValueError("The Email must be set")
        if not username:
            raise ValueError("The Username must be set")
        if not password:
            raise ValueError("The Password name must be set")
        user = self.model(
            email=self.normalize_email(email),
            password=password,
            username=username,
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(
            email=self.normalize_email(email), password=password, username=username
        )
        user.set_password(password)
        user.is_superuser = True
        user.is_active = True
        user.is_staff = True
        user.role = "ADMIN"
        user.save()
        return user
