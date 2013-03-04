from django.contrib import admin
from django.template.loaders.app_directories import Loader
from django.utils.translation import ugettext_lazy as _

from informant.models import Newsletter, Recipient

from .settings import RICHTEXT_WIDGET

ModelAdmin = admin.ModelAdmin
if RICHTEXT_WIDGET and RICHTEXT_WIDGET.__name__ == "ImperaviWidget":
    # Imperavi works a little differently
    # It's not just a field, it's also a media class and a method.
    # To avoid complications, we reuse ImperaviStackedInlineAdmin
    try:
        from imperavi.admin import ImperaviAdmin
        ModelAdmin = ImperaviAdmin
    except ImportError:
        # Log a warning when import fails as to aid debugging.
        logger.warning(
            'Error importing ImperaviStackedInlineAdmin. '
            'Imperavi WYSIWYG text editor might not work.'
        )

class NewsletterAdmin(ModelAdmin):
    list_display = ('subject', 'date', 'sent', 'approved', 'preview_url',)
    ordering = ('-date',)
    actions = ['reset_sent_flag', ]

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'content':
            l = Loader()
            kwargs['initial'] = l.load_template_source('informant/mail/newsletter.html')[0]
        return super(NewsletterAdmin, self).formfield_for_dbfield(db_field, **kwargs)

    def reset_sent_flag(self, request, queryset):
        queryset.update(sent=False)
    reset_sent_flag.short_description = _('Send again')


class RecipientAdmin(admin.ModelAdmin):
    fields = ('email', 'sent', 'deleted',)
    list_display = ('email', 'sent', 'deleted', 'date', 'md5',)
    search_fields = ('email',)

admin.site.register(Newsletter, NewsletterAdmin)
admin.site.register(Recipient, RecipientAdmin)
