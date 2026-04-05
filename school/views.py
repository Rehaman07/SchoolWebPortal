from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import (
    Notice, GalleryCategory, GalleryImage,
    AdmissionApplication, Event, Enquiry,
    ActivityUpdate, VideoEmbed, Student, Teacher
)
from .forms import AdmissionForm, EnquiryForm
from datetime import date


def home(request):
    notices = Notice.objects.filter(is_active=True)[:5]
    updates = ActivityUpdate.objects.all()[:3]
    events = Event.objects.filter(date__gte=date.today())[:3]
    videos = VideoEmbed.objects.filter(is_active=True)[:2]
    context = {
        'notices': notices,
        'updates': updates,
        'events': events,
        'videos': videos,
    }
    return render(request, 'home.html', context)


def about(request):
    teachers = Teacher.objects.all()
    return render(request, 'about.html', {'teachers': teachers})


def gallery(request):
    categories = GalleryCategory.objects.all()
    images = GalleryImage.objects.all()
    return render(request, 'gallery.html', {'categories': categories, 'images': images})


def events(request):
    upcoming_events = Event.objects.filter(date__gte=date.today())
    past_events = Event.objects.filter(date__lt=date.today()).order_by('-date')[:5]
    return render(request, 'events.html', {
        'upcoming_events': upcoming_events,
        'past_events': past_events,
    })


def updates(request):
    all_updates = ActivityUpdate.objects.all()
    return render(request, 'updates.html', {'updates': all_updates})


def admissions(request):
    if request.method == 'POST':
        form = AdmissionForm(request.POST)
        if form.is_valid():
            app = form.save()

            # Email notification to school
            try:
                subject = f"New Admission Application: {app.child_name}"
                body = (
                    f"A new admission application has been received.\n\n"
                    f"Child Name   : {app.child_name}\n"
                    f"Date of Birth: {app.date_of_birth}\n"
                    f"Parent Name  : {app.parent_name}\n"
                    f"Phone        : {app.phone}\n"
                    f"Email        : {app.email}\n"
                    f"Program      : {app.get_program_display()}\n\n"
                    f"Message      : {app.message or 'N/A'}"
                )
                recipient = getattr(settings, 'SCHOOL_NOTIFICATION_EMAIL', settings.DEFAULT_FROM_EMAIL)
                send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [recipient], fail_silently=True)
            except Exception:
                pass  # Never crash the user flow because of email

            messages.success(request, 'Admission application submitted successfully. We will contact you soon.')
            return redirect('admissions')
        # Form is invalid — fall through and re-render with errors
    else:
        form = AdmissionForm()

    return render(request, 'admissions.html', {
        'form': form,
        'programs': AdmissionApplication.PROGRAM_CHOICES,  # keep backward-compat with template
    })


def contact(request):
    if request.method == 'POST':
        form = EnquiryForm(request.POST)
        if form.is_valid():
            enquiry = form.save()

            # Email notification to school
            try:
                subject = f"New Enquiry from {enquiry.name}"
                body = (
                    f"A new contact enquiry has been received.\n\n"
                    f"Name   : {enquiry.name}\n"
                    f"Phone  : {enquiry.phone}\n"
                    f"Email  : {enquiry.email}\n"
                    f"Message: {enquiry.message}"
                )
                recipient = getattr(settings, 'SCHOOL_NOTIFICATION_EMAIL', settings.DEFAULT_FROM_EMAIL)
                send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [recipient], fail_silently=True)
            except Exception:
                pass

            messages.success(request, 'Your enquiry has been submitted successfully. We will get back to you shortly.')
            return redirect('contact')
        # Invalid form — re-render with errors
    else:
        form = EnquiryForm()

    return render(request, 'contact.html', {'form': form})
