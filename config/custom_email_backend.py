import smtplib
import ssl
from django.core.mail.backends.smtp import EmailBackend

class CustomEmailBackend(EmailBackend):
    def _get_ssl_context(self):
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        return context

    def open(self):
        if self.connection:
            return False
        try:
            self.connection = smtplib.SMTP(self.host, self.port)
            self.connection.ehlo()
            if self.use_tls:
                self.connection.starttls(context=self._get_ssl_context())
                self.connection.ehlo()
            if self.username and self.password:
                self.connection.login(self.username, self.password)
            return True
        except:
            if self.fail_silently:
                return False
            raise