import tkinter as tk
from tkinter import messagebox
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Função para enviar o e-mail
def enviar_email():
    # Configurações do servidor SMTP do Gmail
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587  # Porta padrão do Gmail para TLS
    
    # Seu endereço de e-mail e senha (é recomendado usar variáveis de ambiente para não expor diretamente no código)
    email_sender = 'seu_email@gmail.com'
    senha = 'sua_senha'
    
    # Destinatário
    email_destinatario = 'josegrand65@gmail.com'
    
    # Assunto e corpo do e-mail
    assunto = 'Teste de e-mail via Python'
    corpo = 'Olá José, este é um e-mail de teste enviado via Python.'
    
    # Configuração do e-mail
    msg = MIMEMultipart()
    msg['From'] = email_sender
    msg['To'] = email_destinatario
    msg['Subject'] = assunto
    
    msg.attach(MIMEText(corpo, 'plain'))
    
    # Conectando ao servidor SMTP
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(email_sender, senha)
        
        # Enviando e-mail
        server.sendmail(email_sender, email_destinatario, msg.as_string())
        
        # Fechando a conexão
        server.quit()
        
        messagebox.showinfo('E-mail enviado', 'O e-mail foi enviado com sucesso!')
    except Exception as e:
        messagebox.showerror('Erro', f'Ocorreu um erro ao enviar o e-mail:\n\n{str(e)}')

# Criando a janela principal
janela = tk.Tk()
janela.title('Envio de E-mail')

# Botão para enviar o e-mail
btn_enviar = tk.Button(janela, text='Enviar E-mail', command=enviar_email)
btn_enviar.pack(pady=20)

# Rodando a aplicação
janela.mainloop()
