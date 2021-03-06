from datetime import datetime
import re
import sys

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.mail import EmailMultiAlternatives, get_connection
from django.core.management.base import NoArgsCommand
from django.template import Template, Context
from django.template.loader import render_to_string
from django.template.loaders.app_directories import Loader
from django.utils import translation

from informant.models import Recipient, Newsletter
from informant.settings import *

NEWSLETTER_EMAIL = settings.NEWSLETTER_EMAIL


class Command(NoArgsCommand):
    help = "Send undelivered recipes newsletters"

    def handle_noargs(self, **options):
        translation.activate(settings.LANGUAGE_CODE)

        site = Site.objects.get_current()
        connection = get_connection()

        # Fake md5
        md5_mark = '00112233445566778899aabbccddeeff'
        pat = re.compile(md5_mark)

        # Newsletters, which have approved and have not delivered
        newsletters = Newsletter.objects.filter(approved=True, sent=False,
                                                date__lte=datetime.now())

        for newsletter in newsletters:
            # Prepare context
            c = Context({
                'newsletter': newsletter,
                'site': site,
                'recipient': {'md5': md5_mark},
                'MEDIA_URL': settings.MEDIA_URL,
                'STATIC_URL': settings.STATIC_URL
            })

            # Render parts
            l = Loader()

            #template = l.load_template_source('informant/mail/newsletter.html')
            content_html_orig = render_to_string('informant/mail/newsletter.html', c)
            content_txt_orig = render_to_string('informant/mail/base.txt', c)

            # Replace relative media
            content_html_orig = content_html_orig.replace(
                settings.MEDIA_URL,
                'http://%s%s' % (site.domain, settings.MEDIA_URL)
            )

            # Recipients, who have not got newsletter
            recipients = newsletter.recipient.filter(sent=False, deleted=False)

            for recipient in recipients:
                # Replace fake md5
                content_html = re.sub(pat, recipient.md5, content_html_orig)
                content_txt = re.sub(pat, recipient.md5, content_txt_orig)

                # Send mail
                msg = EmailMultiAlternatives(
                    SUBJECT,
                    content_txt,
                    NEWSLETTER_EMAIL,
                    (recipient.email,)
                )
                msg.attach_alternative(content_html, 'text/html')

                try:
                    connection.send_messages((msg,))
                except Exception, e:
                    sys.stderr.write("%s - %s\n" % (recipient.email, str(e)))

                # Set recipient delivered flag
                recipient.sent = True
                recipient.save()

            # If newsletter was sent, set newsletter delivered flag
            newsletter.sent = True
            newsletter.save()

            # And clear recipients delivered flag
            Recipient.objects.all().update(sent=False)
