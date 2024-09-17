from __future__ import print_function
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from pprint import pprint

import utils.email_constants as email_constants

class EmailHandler:

    def __init__(self,
            api_key: str,
            email_subject: str,
            html_content: str
        ) -> None:
        self.__api_key = api_key
        self.__email_subject = email_subject
        self.__html_content = html_content
        self.__api_instance = None


    def __create_api_instance(self) -> None:
        """ Create an instance of the Brevo API.
        """
        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key['api-key'] = self.__api_key
        self.__api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
        # self.__api_instance = sib_api_v3_sdk.AccountApi(sib_api_v3_sdk.ApiClient(configuration))

    def __configure_email_data(self) -> None:
        """ Configure the email data.
        """
        self.__email_data = sib_api_v3_sdk.SendSmtpEmail(
            # bcc=bcc,
            # cc=cc,
            headers={
                'accept': 'application/json',
                'content-type': 'application/json',
                'api-key': self.__api_key
            },

            sender={"name": email_constants.SENDER_NAME, "email": email_constants.SENDER_EMAIL},
            to=[{"name": email_constants.TO_NAME, "email": email_constants.TO_EMAIL}],
            reply_to={"name": email_constants.REPLY_NAME, "email": email_constants.REPLY_EMAIL},

            subject=self.__email_subject,
            html_content=self.__html_content,
        )


    def __send_email(self) -> None:
        """ Send the email.
        """
        try:
            api_response = self.__api_instance.send_transac_email(self.__email_data)
            # api_response = self.__api_instance.get_account()
            pprint(api_response)
        except ApiException as e:
            print("Exception when calling SMTPApi->send_transac_email: %s\n" % e)


    def send(self) -> None:
        """ Entry point to send all emails.
        """
        self.__create_api_instance()
        self.__configure_email_data()
        self.__send_email()


if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    load_dotenv()

    api_key = os.getenv("BREVO_API_KEY")

    html_content = open("data/newsdataio/newsletter/2024-09-17.html", "r").read()

    email_handler = EmailHandler(
        api_key=api_key,
        email_subject="The Daily Indian Story",
        html_content=html_content
    )
    email_handler.send()