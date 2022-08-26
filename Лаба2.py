import getpass
import psycopg2

def access_editor():
    print('Введите пароль:')
    pas = getpass.getpass()

    try:
        connection = psycopg2.connect(host='localhost',
                                      database='postgres',
                                      user='Admin',
                                      password=pas,
                                      port=5432)
        print('Connection success.')
    except Exception:
        print('ERROR: Connection refused.')
        exit()

    
    with connection:
        cursor = connection.cursor()

        print('Выберите вариант ответа:')
        print('1.Добавить права')
        print('2.Удалить права')
        
        answer = input()

        if answer in ['1','1.','Добавить','добавить','Добавить права',
                      'добавить права','1.Добавить права','1.добавить права']:
            
            print('Введите пользователя:')
            user = input()
            print('Введетие этаж:')
            level = input()

            try:
                command = 'INSERT INTO access_table VALUES (\''+user+'\',\''+level+'\');'
                cursor.execute(command)

                command = 'GRANT SELECT ON export,access_table TO \"'+user+'\";'
                cursor.execute(command)

                print('Access granted.')
            except Exception:
                print('ERROR: Access not granted')
                exit()

        else:
            
            print('Введите пользователя:')
            user = input()

            try:
                command = 'REVOKE SELECT ON export,access_table FROM \"'+user+'\";'
                cursor.execute(command)

                command = 'DELETE FROM access_table WHERE login = \''+user+'\';'
                cursor.execute(command)

                print('Access deleted')
            except Exception:
                print('ERROR: Access not deleted')
                exit()
                
access_editor()
