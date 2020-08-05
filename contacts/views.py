from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from .models import Contact


def contact(request):
    if request.method == 'POST':
        listing_id = request.POST['listing_id']
        listing = request.POST['listing']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        user_id = request.POST['user_id']
        realtor_email = request.POST['realtor_email']

        # check if there's already an inquiry for the same property by a registered user

        if request.user.is_authenticated:
            has_contacted = Contact.objects.all().filter(listing_id=listing_id, user_id=user_id)
            if has_contacted:
                messages.error(request, 'You have already submitted an inquiry for this Property')
                return redirect('/listings/'+listing_id)

        contact = Contact(listing=listing, listing_id=listing_id, name=name, email=email, phone=phone,
                          message=message, user_id=user_id)

        contact.save()
        send_mail(
            'PROPERTY LISTING INQUIRY',
            'There has been an inquiry for ' + listing + ' by ' + name + '. Sign into the Admin Portal for more info',
            'sudhanshujha.1998@gmail.com',
            [realtor_email, 'sudhanshujha.005@gmail.com'],
            fail_silently=False
        )
        messages.success(request, 'Your enquiry has been submitted!')

        return redirect('/listings/'+listing_id)
