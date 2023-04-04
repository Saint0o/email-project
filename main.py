import mail_client

while True:
    command = input('1. Отправить письмо\n2. Прочитать письмо\n3. Выйти\n')

    match command:
        case '1':
            # username = input('Введите userName: ')
            # password = input('Введите password: ')
            # from_addr = input('Адресант: ')
            # to_addrs = input('Адресат: ')
            # subject = input('Subject: ')
            # text = input('Text: ')
            # private_key = input('Приватный ключ: ')
            username = 'testirovaniye321@gmail.com'
            password = 'igdptgutxfgzjjlz'
            from_addr = 'testirovaniye321@gmail.com'
            to_addrs = 'testirovaniye321@gmail.com'
            subject = '123'
            text = '123'
            private_key = './id_rsa'

            mail_client.send_email(from_addr,
                                   to_addrs,
                                   username,
                                   password,
                                   subject,
                                   text,
                                   private_key)
        case '2':
            username = 'testirovaniye321@gmail.com'
            password = 'igdptgutxfgzjjlz'

            mail_client.receive_mail(username, password)
        case 3:
            break
        case _:
            print("Неизвестная команда")



