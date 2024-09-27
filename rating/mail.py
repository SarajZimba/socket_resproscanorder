import environ
env = environ.Env(DEBUG=(bool, False))
from .utils import send_mail_to_receipients
from threading import Thread
from datetime import datetime
from organization.models import MailRecipient

# @receiver(post_save, sender=tblRatings)
def create_profile_for_email(instance):
    sender = env('EMAIL_HOST_USER')
    mail_list = []
    recipients = MailRecipient.objects.filter(status=True)
    for r in recipients:
        mail_list.append(r.email)
    if mail_list:
        dt_now = datetime.now()
        date_now = dt_now.date()
        time_now = dt_now.time().strftime('%I:%M %p')
        report_data = {
                'date_now': date_now,
                'time_now': time_now,
                'atmosphere': instance.atmosphere_rating,
                'service':instance.service_rating,
                'presentation': instance.presentation_rating,
                'cleanliness': instance.cleanliness_rating,
                'overall': instance.overall_rating,  
                'review': instance.review,
            }
        
        itemwiserating_list = get_itemrating(instance) 
        report_data['itemwiserating_list'] = itemwiserating_list    
        
        Thread(target=send_mail_to_receipients, args=(report_data, mail_list, sender)).start()

from .models import tblitemRatings, tblRatings
def get_itemrating(rating):

    itemwiserating_list = []
    itemratings = tblitemRatings.objects.filter(tblrating = rating)
    for itemrating in itemratings:
        itemrating_dict = {
            "itemname": itemrating.itemId.item_name,
            "rating": itemrating.rating,
            "comment":itemrating.comment
        }
        itemwiserating_list.append(itemrating_dict)

    return itemwiserating_list

def get_item(itemrating):
    items_list = []
    tblitems = tblitemRatings.objects.filter(status=True, is_deleted=False)
    for items in tblitems:
        items_dict = {
            'itemname' : items.itemId.item_name,
            'rating' : items.rating, 
            'atmosphere_rating' : items.tblrating.atmosphere_rating, 
            'service_rating': items.tblrating.service_rating, 
            'presentation_rating': items.tblrating.presentation_rating,
            'cleanliness_rating': items.tblrating.cleanliness_rating,
            'overall_rating': items.tblrating.overall_rating,
            'review': items.tblrating.review

        }

        items_list.append(items_dict)

    print("This is the final list", items)

    return items