from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser, BaseUserManager
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings

#use to send verification
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_text
from django.template.loader import get_template
from django.core.mail import EmailMessage
from todo.helpers.generateToken import account_activation_token
from tenants.models import TenantAwareModel

class PersonManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password, site, send_email = False):
        #create user
        if not email:
            raise ValueError("User must have email or password")
            
        user = self.model(
            email = self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)
        user.is_active = False
        user.save(using=self._db)
        if send_email:
            user.send_verification(user, site)
        
        return user

    def create_superuser(self, email, first_name, last_name, password):
        #creates save admin user with give email and password
        if not email:
            raise ValueError("User must have email or password")
            
        user = self.create_user(
            email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            site = None,
        )
        
        user.is_admin=True
        user.save(using=self._db)
        return user
    
    def activate_user(self, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = Profile.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, user.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.is_verified = True
            user.save()

            return user

        return None

class Profile(AbstractBaseUser):
    
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(
        verbose_name='email address',
        unique=True,
        max_length=255,
        blank=False,
        default="",
    )

    is_verified = models.BooleanField(default=False)
    is_activate = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False,blank=True,)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True,blank=True,)

    objects = PersonManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name",]

    # def __str__(self):
    #     return "%s %s" % (self.first_name, self.last_name)

    # this methods are require to login super user from admin panel
    def has_perm(self, perm, obj=None):
        return True

    # this methods are require to login super user from admin panel
    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    # @property
    # def is_anonymous(self):
    #     "Is the user a member of staff?"
    #     # Simplest possible answer: All admins are staff
    #     return self.is_admin


    def send_verification(self, user, site):
        
        context = {
            'user':user,
            'domain':site.domain,
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token':account_activation_token.make_token(user),
        }

        email = user.email
        subject = 'Activate Your Account'
        content = get_template('registration/activation.html').render(context)
        email = EmailMessage(subject, content,to=[email])
        email.content_subtype = 'html'
        email.send()
    
        return user

class List(TenantAwareModel):
    """
    a model for creating a list of a user
    """

    Priority_Choices = [
        ('lp',"Low Priority"),
        ('mp',"Medium Priority"),
        ('hp',"High Priority")
    ]

    title = models.CharField(max_length=150,default="")
    description = models.TextField()
    is_done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)
    priority = models.CharField(max_length=2, choices=Priority_Choices, default='lp')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
