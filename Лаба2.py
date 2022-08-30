import getpass
import psycopg2

def access_editor():
    #Вводим пароль администратора (при вводе через терминал (cmd,bash)
    #пароля не видно)
    print('Введите пароль:')
    pas = getpass.getpass()
    #Пытаемя присоедениться к нашей Базе Данных
    try:
        connection = psycopg2.connect(host='localhost',
                                      database='postgres',
                                      user='Admin',
                                      password=pas,
                                      port=5432)
        print('Connection success.')
    #Если по какой-либо причине не получается, закрываем скрипт
    except Exception:
        print('ERROR: Connection refused.')
        exit()

    #При усмпешной попытке подсоединения
    with connection:
        #Создаем курсор
        cursor = connection.cursor()
        #выбираем: Удалить или добавить права
        print('Выберите вариант ответа:')
        print('1.Добавить права')
        print('2.Удалить права')
        
        answer = input()
        
        #Если добавить права
        if answer in ['1','1.','Добавить','добавить','Добавить права',
                      'добавить права','1.Добавить права','1.добавить права']:
            #Вводим пользователя и по каким этажам разрешаем ему видеть строки
            print('Введите пользователя:')
            user = input()
            print('Введетие этаж:')
            level = input()
            #Пытаемся добавить права пользоватею.
            #Добавляем в табличку доступа и включаем права на селект.
            try:
                command = 'INSERT INTO access_table VALUES (\''+user+'\',\''+level+'\');'
                cursor.execute(command)

                command = 'GRANT SELECT ON export,access_table TO \"'+user+'\";'
                cursor.execute(command)

                print('Access granted.')
            #При неуспешной попытке выходим
            except Exception:
                print('ERROR: Access not granted')
                exit()
        #Если удаляем права
        else:
            #Вводим пользователя, у котррого хотим удалить права
            print('Введите пользователя:')
            user = input()
            #Пытаемся удалить права. Удаляем из палитики безопасности, а также из таблички доступа
            try:
                command = 'REVOKE SELECT ON export,access_table FROM \"'+user+'\";'
                cursor.execute(command)

                command = 'DELETE FROM access_table WHERE login = \''+user+'\';'
                cursor.execute(command)

                print('Access deleted')
            #При неуспешной попытке выходим из программы
            except Exception:
                print('ERROR: Access not deleted')
                exit()
#Запуск скрипта           
access_editor()
