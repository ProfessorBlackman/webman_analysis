from django.contrib.auth.base_user import BaseUserManager

from webman_analysis.loggers import auth_logger


class CustomUserManager(BaseUserManager):
    def create_user(self, email: str, password: str = None, first_name: str = None, last_name: str = None,
                    **extra_fields):

        if not first_name:
            raise ValueError("The First Name field must be set")
        if not last_name:
            raise ValueError("The Last Name field must be set")
        if not password:
            raise ValueError("The Password field must be set")
        if not email:
            raise ValueError("The Email field must be set")

        email = self.normalize_email(email)
        try:
            user = self.model(first_name=first_name, last_name=last_name, email=email, **extra_fields)
            user.set_password(password)
            user.save(using=self._db)
            return user
        except Exception as e:
            auth_logger.error(f"Error creating user: {e}")
            raise e

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_verified', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        # Ensure default values for first_name and last_name if required
        extra_fields.setdefault('first_name', 'Admin')
        extra_fields.setdefault('last_name', 'User')
        extra_fields.setdefault('is_verified', True)

        return self.create_user(email=email, password=password, **extra_fields)
