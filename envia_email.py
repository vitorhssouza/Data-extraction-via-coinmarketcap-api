import smtplib
from oculto import dados
from email.message import EmailMessage

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# Função que envia email


def envia_email(texto):
    try:
        msg = EmailMessage()
        msg['Subject'] = 'PREÇO CRIPTMOEDA'
        msg['From'] = dados['email']
        msg['To'] = dados['to']
        #msg.add_header('Content-Type', 'text/html')
        #msg.set_content(texto, 'html')
        msg.set_content(texto)
        #msg.set_payload(texto)
        #msg.attach(MIMEText(texto, 'html'))

        # enviando um email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(dados['email'], dados['senha'])
            smtp.send_message(msg)
            print('Email enviado')

    except:
        print('Não conseguir enviar o email')







