import random
from django.core.mail import EmailMultiAlternatives

def random_int():
    random_num = random.randint(1111, 9999)
    return int(random_num)

def send_verify_otp_mail(subject, text_message, from_mail, to_email, html_message):
    email = EmailMultiAlternatives(
        subject,
        text_message,
        from_mail,
        [to_email],
    )
    email.content_subtype = 'html'
    email.attach_alternative(html_message, "text/html")
    email.send()
    print('Verify mail send successfully')