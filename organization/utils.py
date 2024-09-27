from django.core.mail import send_mail
from django.template.loader import render_to_string

def send_mail_to_receipients(data, mail_list, sender):
    email_body = render_to_string('organization/mail_template.html', data)
    try:
        send_mail(
            f'{data["org_name"]} - {data["branch"]} End Day Report',
            '',
            sender,
            mail_list,
            fail_silently=False,
            html_message=email_body
        )
    except Exception:
        pass


def send_combined_mail_to_receipients(combine_data, terminals_data,mail_list, sender):
    email_body = render_to_string('organization/combined_end_day_report_list.html', {'combine_data':combine_data, 'terminals_data':terminals_data})
    try:
        send_mail(
            'End Day Report',
            '',
            sender,
            mail_list,
            fail_silently=False,
            html_message=email_body
        )
    except Exception as e:
        print("Exception Occured", e)

from django.db.models import Sum
def get_mobilepayments(branch, terminal):
    from bill.models import MobilePaymentSummary
    mobilepayment_summary = MobilePaymentSummary.objects.filter(branch=branch, terminal=terminal, sent_in_mail=False) 

    if mobilepayment_summary:
        total_per_type = mobilepayment_summary.values('type__name').annotate(total_value=Sum('value'))
        return mobilepayment_summary,total_per_type
    else:
        return None, None

# convert_to_dict = get_mobilepayments(3, 2)

def convert_to_dict(value):
    # Convert the queryset to a dictionary
    if value:
        total_per_type_dict = {item['type__name']: item['total_value'] for item in value}   

        return total_per_type_dict
    else:
        return None