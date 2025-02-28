from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def get_queryset(self):
        return super().get_queryset()

    def active_users(self):
        return self.get_queryset().filter(is_active=True)

    def admins(self):
        return self.get_queryset().filter(role="admin")

    def students(self):
        return self.get_queryset().filter(role="student")

    def staff(self):
        return self.get_queryset().filter(role="staff")

    # def create_user(self, email, password=None, **extra_fields):
    #     if not email:
    #         raise ValueError("The Email field must be set")
    #     if not password:
    #         raise ValueError("A password is required")

    #     email = self.normalize_email(email)
    #     extra_fields.setdefault("is_active", True)

    #     user = self.model(email=email, **extra_fields)
    #     user.set_password(password)
    #     user.save(using=self._db)
    #     return user

    # def create_superuser(self, email, password=None, **extra_fields):

    #     if not password:
    #         raise ValueError("Superuser must have a password")

    #     extra_fields["is_staff"] = True
    #     extra_fields["is_superuser"] = True

    #     return self.create_user(email, password, **extra_fields)
