from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.core.signing import TimestampSigner
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View

User = get_user_model()
signer = TimestampSigner()


class SendVerificationEmailView(View):
    def post(self, request, *args, **kwargs):
        user = get_object_or_404(User, id=kwargs.get("user_id"))
        token = signer.sign(user.email)
        verification_link = f"http://127.0.0.1:8000/verify-email/{token}/"

        subject = "Verify Your Email Address"
        message = f"Click the link below to verify your email:\n\n{verification_link}"
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [user.email]

        send_mail(subject, message, from_email, recipient_list)

        return JsonResponse(
            {"message": "Verification email sent successfully."}
        )
