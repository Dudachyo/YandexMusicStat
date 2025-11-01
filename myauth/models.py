from django.contrib.auth.models import User
from django.db import models
from .utils import TokenEncryption

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/%Y/%m/%d/', default="avatars/images.png" , null=True, blank=True,)
    encrypted_token = models.TextField(blank=True,null=True,verbose_name='encrypted_token')
    bio = models.TextField(null=True, blank=True,verbose_name='bio')
    hidden = models.BooleanField(default=False,verbose_name='hidden')
    created_at = models.DateTimeField(auto_now_add=True,verbose_name='date of creation')
    updated_at = models.DateTimeField(auto_now=True,verbose_name='date of update')

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'Users Profiles'

    def __str__(self):
        return f"Profile {self.user.username}"

    def save_token(self, token: str):
        """Сохраняет токен в зашифрованном виде"""
        encryptor = TokenEncryption()
        self.encrypted_token = encryptor.encrypt(token)
        self.save()

    def get_token(self) -> str:
        """Получает расшифрованный токен"""
        if not self.encrypted_token:
            return None
        encryptor = TokenEncryption()
        return encryptor.decrypt(self.encrypted_token)

    def has_token(self) -> bool:
        """Проверяет наличие токена"""
        return bool(self.encrypted_token)


