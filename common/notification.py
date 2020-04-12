from django.conf import settings
from django.core.mail import EmailMultiAlternatives
# get_template is what we need for loading up the template for parsing.
# from django.template.loader import get_template
# Templates in Django need a "Context" to parse with, so we'll borrow this.
# "Context"'s are really nothing more than a generic dict wrapped up in a
# neat little function call.
from django.template import loader
from django.core import mail


class Common():
    mail = mail

    def getDefaultSender(self):
        """
        User = get_user_model()
        a = User.objects.filter(is_superuser=1).all()
        b = a[0]
        if b.first_name is not None and b.first_name !='':
            return "%s %s<%s>"%(b.first_name, b.last_name, b.email)
        else:
            return b.email
        """
        return "Blog Site <contact@blogsite.com>"

    def send_mass_mail(self, mail_list):
        msg_list = []                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
        for email in mail_list:
            email['mail_template_args']['STATIC_URL'] = settings.STATIC_URL
            mail_context = email['mail_template_args']
            try:
                template = loader.get_template('generic/' + email['mail_template'])
            except:
                template = loader.get_template(email['mail_template'])
            text_part = template.render(mail_context)
            html_part = template.render(mail_context)
            msg = EmailMultiAlternatives(
                email['mail_subject'],
                text_part,
                self.getDefaultSender(),
                email['mail_to'] if type(email['mail_to'])== list else [email['mail_to']],
            )
            msg.attach_alternative(html_part, "text/html")
            msg_list.append(msg)
        try:
            connection = mail.get_connection(
                                host=settings.EMAIL_HOST,
                                port=int(settings.EMAIL_PORT),
                                username=settings.EMAIL_HOST_USER,
                                password=settings.EMAIL_HOST_PASSWORD,
                                use_tls=True)
            connection.open()
            connection.send_messages(msg_list)
            connection.close()
        except Exception as e:
            pass

    def send_mail(self, **kwargs):
        def inner():
            list = []
            kwargs['mail_template_args']['STATIC_URL'] = settings.STATIC_URL
            mail_context = kwargs['mail_template_args']
            try:
                template = loader.get_template('generic/' + kwargs['mail_template'])
            except:
                template = loader.get_template(kwargs['mail_template'])
            text_part = template.render(mail_context)
            html_part = template.render(mail_context)
            cc = None
            if kwargs.has_key("cc"):
                cc = kwargs['cc']
            msg = EmailMultiAlternatives(
                kwargs['mail_subject'],
                text_part,
                self.getDefaultSender(),
                [kwargs['mail_to']],
                cc=[cc]
            )
            msg.attach_alternative(html_part, "text/html")
            list.append(msg)
            try:
                connection = mail.get_connection(
                                    host=settings.EMAIL_HOST,
                                    port=int(settings.EMAIL_PORT),
                                    username=settings.EMAIL_HOST_USER,
                                    password= settings.EMAIL_HOST_PASSWORD,
                                    use_tls=True)
                connection.open()
                connection.send_messages(list)
                connection.close()
            except Exception as e:
                print ('Exception: %s' % e)
            # raise Exception(mail_context)
            # raise Exception(kwargs)"""
        return inner

