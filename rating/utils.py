from django.core.mail import send_mail
from django.template.loader import render_to_string

def send_mail_to_receipients(data, mail_list, sender):
    email_body = render_to_string('mailrecipient/mail_template.html', data)
    try:
        send_mail(
            'Review Report',
            '',
            sender,
            mail_list,
            fail_silently=False,
            html_message=email_body
        )
    except Exception:
        pass
    
from user.models import Customer
from menu.models import Organization

def give_review_points(customer_name, customer_phone):
    try:
        organization = Organization.objects.first()
        review_points = organization.review_points
    except Exception as e:
        print("Organization is not created")
    try:
        customer = Customer.objects.get(name=customer_name, phone=customer_phone)
        customer.loyalty_points += review_points
        customer.save()
    except Customer.DoesNotExist:
        print("Customer does not exst of that name and phone")