from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Creating user manager
        Creates and saves a User with the given email, username, and password.
        """

        if not email:
            raise ValueError("Users must have an email address")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)

        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """Creating superuser mng
            Create and saves a superuser with the given email, username and password.
        """
        user = self.create_superuser(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user