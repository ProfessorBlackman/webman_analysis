import math
import random

from django.conf import settings
from django.core.mail import EmailMessage

from redis_config import redis_client
from webman_analysis.loggers import default_logger, redis_logger


def generate_otp() -> str:
    digits = "0123456789"
    OTP = ""
    for _ in range(6):
        OTP += digits[math.floor(random.random() * 10)]
    return OTP


def save_otp(email: str, otp: str) -> None:
    try:
        redis_client.set(email, otp, ex=300)
    except Exception as e:
        redis_logger.error(f"Error saving otp: {e}")


def get_otp(email: str) -> str:
    try:
        otp_bytes = redis_client.getdel(email)
        if otp_bytes is not None:
            return otp_bytes.decode('utf-8')
        return ""
    except Exception as e:
        redis_logger.error(f"Error getting otp: {e}")
        return ""


def send_otp(email: str, otp: str) -> None:
    print(f"Sending OTP to {email}: {otp}")
    subject = "Confirm your account"
    sender_email = settings.EMAIL_HOST_USER
    link = f"{settings.FRONTEND_DOMAIN}/confirm?email={email}&otp={otp}"
    body = (f"Use this otp to verify your account: \n {otp}. \n"
            f"Or click this link to verify your account: \n {link}")

    email = EmailMessage(
        subject=subject,
        body=body,
        from_email=sender_email,
        to=[email]
    )
    try:
        email.send()
    except Exception as e:
        default_logger.error(f"Error sending email: {e}")


def verify_otp(otp_from_user: str, stored_otp: str) -> bool:
    print(f"types [otp_from_user] : {type(otp_from_user)} | [stored_otp] : {type(stored_otp)} ")
    return otp_from_user == stored_otp
