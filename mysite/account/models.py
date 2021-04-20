from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class CustomAccountManager(BaseUserManager):
    def create_user(self, email, username, first_name, last_name, password=None):
        if not email:
            raise ValueError(u"Введите эл.почту")
        if not username:
            raise ValueError(u"Введите имя пользователя")
        if not first_name:
            raise ValueError(u"Введите имя")
        if not last_name:
            raise ValueError(u"Введите фамилию")

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, first_name, last_name, password):
        user = self.create_user(
            username=username,
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            password=password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    objects = CustomAccountManager()
    email = models.EmailField(verbose_name=u"эл. почта", max_length=60, unique=True)
    username = models.CharField(verbose_name=u"имя пользователя", max_length=30, unique=True)
    first_name = models.CharField(verbose_name=u"имя", max_length=30)
    last_name = models.CharField(verbose_name=u"фамилия", max_length=30)
    middle_name = models.CharField(verbose_name=u"отчество", max_length=30)
    phone_number = models.CharField(verbose_name=u"номер телефона", max_length=20)
    school = models.CharField(verbose_name="учебное заведение", max_length=100, blank=True, null=True)
    city = models.CharField(verbose_name="город", max_length=100, blank=True, null=True)
    date_joined = models.DateTimeField(verbose_name=u"дата регистрации", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name=u"последний вход", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
