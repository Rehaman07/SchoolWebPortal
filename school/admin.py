from django.contrib import admin
from django.core.mail import send_mass_mail
from django.conf import settings
from .models import (
    Notice, GalleryCategory, GalleryImage,
    AdmissionApplication, Event, Enquiry,
    ActivityUpdate, VideoEmbed, Student, Teacher
)

# ─────────────────────────────────────────────────────────────
#  Admin Site Branding
# ─────────────────────────────────────────────────────────────
admin.site.site_header = "Little Steps International Pre School"
admin.site.site_title = "Little Steps Admin"
admin.site.index_title = "School Management Panel"


# ─────────────────────────────────────────────────────────────
#  Custom Admin Actions
# ─────────────────────────────────────────────────────────────

@admin.action(description="📧 Send email notification to all parents")
def send_notification_email(modeladmin, request, queryset):
    """Send a mass email to all parents for selected notices/events."""
    parent_emails = list(
        Student.objects.exclude(parent_email='')
        .values_list('parent_email', flat=True)
    )

    if not parent_emails:
        modeladmin.message_user(request, "No parent emails found in the system.", level='warning')
        return

    email_messages = []

    for item in queryset:
        subject = f"School Update: {item.title}"
        if isinstance(item, Notice):
            body = f"Notice: {item.title}\n\n{item.content}"
        elif isinstance(item, Event):
            body = f"Event: {item.title}\nDate: {item.date}\n\n{item.description}"
        else:
            body = str(item)

        # One email per parent (avoids exposing other parents' addresses)
        for email in parent_emails:
            email_messages.append((subject, body, settings.DEFAULT_FROM_EMAIL, [email]))

    try:
        count = send_mass_mail(tuple(email_messages), fail_silently=False)
        modeladmin.message_user(
            request,
            f"✅ Successfully sent {count} emails for {queryset.count()} item(s).",
            level='success'
        )
    except Exception as e:
        modeladmin.message_user(request, f"❌ Error sending emails: {e}", level='error')


# ─────────────────────────────────────────────────────────────
#  Model Admin Registrations
# ─────────────────────────────────────────────────────────────

@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_posted', 'is_active')
    list_filter = ('is_active', 'date_posted')
    search_fields = ('title', 'content')
    list_editable = ('is_active',)
    actions = [send_notification_email]


class GalleryImageInline(admin.TabularInline):
    model = GalleryImage
    extra = 2


@admin.register(GalleryCategory)
class GalleryCategoryAdmin(admin.ModelAdmin):
    inlines = [GalleryImageInline]
    search_fields = ('name',)


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('caption', 'category', 'created_at')
    list_filter = ('category',)


@admin.register(AdmissionApplication)
class AdmissionApplicationAdmin(admin.ModelAdmin):
    list_display = ('child_name', 'get_program_display_label', 'parent_name', 'phone', 'email', 'submitted_at')
    list_filter = ('program', 'submitted_at')
    search_fields = ('child_name', 'parent_name', 'email', 'phone')
    readonly_fields = ('submitted_at',)

    @admin.display(description='Program')
    def get_program_display_label(self, obj):
        return obj.get_program_display()


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'time')
    list_filter = ('date',)
    search_fields = ('title', 'description')
    actions = [send_notification_email]


@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'submitted_at')
    list_filter = ('submitted_at',)
    search_fields = ('name', 'email', 'message')
    readonly_fields = ('submitted_at',)


@admin.register(ActivityUpdate)
class ActivityUpdateAdmin(admin.ModelAdmin):
    list_display = ('title', 'date')
    list_filter = ('date',)
    search_fields = ('title', 'content')


@admin.register(VideoEmbed)
class VideoEmbedAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active')
    list_filter = ('is_active',)
    list_editable = ('is_active',)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'program_enrolled', 'parent_name', 'parent_phone', 'enrolled_date')
    list_filter = ('program_enrolled', 'enrolled_date')
    search_fields = ('name', 'parent_name', 'parent_email')


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('name', 'designation')
    search_fields = ('name', 'designation')
