import subprocess
import logging
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from datetime import datetime
from telegram import Bot
from dotenv import load_dotenv
from config import configuration as config

# Get the current date
current_date = datetime.now()
# Format the date as YYYY-MM-DD
formatted_date = current_date.strftime('%Y-%m-%d')
# Configure the logger
logging.basicConfig(filename=f'logs/log_{formatted_date}.txt', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# Load environment variables from .env file
env_path = os.getcwd()+os.path.join('/config','.env')
load_dotenv(env_path)

class PostmanNewman:
    @staticmethod
    def execute_postman_test():
        # Paths to collection and environment files
        collection_file = os.getcwd()+os.path.join('/assets','collection','pintu_collection.json') 
        environment_file = os.getcwd()+os.path.join('/assets','environment', 'pintu_env.json') 
        # Replace 'your_report_filename.html' with the desired filename for the HTML report
        report_filename = os.getcwd()+os.path.join('/reports',f'pintu_api_report_{formatted_date}.html')

        # Command to run Newman with htmlextra reporter
        command = f'newman run {collection_file} --environment {environment_file} --reporters htmlextra --reporter-htmlextra-export {report_filename}'
        try:
            # Execute the command
            subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8')
        except Exception as e:
            # Log any exceptions
            logging.exception("An error occurred: %s", str(e))

    @staticmethod
    def send_result_to_email():
        sender_email = f'{os.getenv("SENDER")}'
        app_password = f'{os.getenv("APP_PASSWORD")}'
        recipient_email = f'{config.email_credentials.get("recipient")}'
        smtp_server = f'{os.getenv("SMTP_SERVER")}'
        smtp_port = f'{os.getenv("SMTP_PORT")}'

        # Create a MIME multipart message
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = recipient_email
        message['Subject'] = 'HTML Report'

        # Attach HTML file
        html_file_path = os.getcwd()+os.path.join('/reports',f'pintu_api_report_{formatted_date}.html')
       
        # Attach body text to the email
        body = 'HELLO, THIS IS JUST EXAMPLE REPORT FOR APITEST ! DOWNLOAD THE FILE AND OPEN IN BROWSER TO SEE THE RESULT !'
        message.attach(MIMEText(body, 'plain'))

        # Attach the file
        attachment = open(html_file_path, 'rb')

        attachment_part = MIMEApplication(attachment.read(), Name=f'pintu_api_report_{formatted_date}.html')
        attachment.close()

        # Set the Content-Disposition header to "attachment"
        attachment_part.add_header('Content-Disposition', f'attachment; filename=pintu_api_report_{formatted_date}.html')

        # Add the attachment to the email
        message.attach(attachment_part)

        # Connect to the SMTP server and send the email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, app_password)
            server.sendmail(sender_email, recipient_email, message.as_string())

    @staticmethod
    async def send_result_to_telegram():
        # Create a bot instance
        bot = Bot(token=f'{os.getenv("BOT_TOKEN")}')
        group_chat_id = f'{os.getenv("CHAT_ID")}'
        await bot.initialize()
        # Path to the file 
        file_path = os.getcwd()+os.path.join('/reports', f'pintu_api_report_{formatted_date}.html')
        try:
            # Send the file to the group
            with open(file_path, 'rb') as file:
                # Send the file as a document
                await bot.send_document(chat_id=group_chat_id, document=file, caption=f'Here are API test result for {formatted_date} !')
        except Exception as e:
            print(f"Error: {e}")