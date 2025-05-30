import sqlite3 as sq
import datetime
import os

BASE_FOLDER = r"C:\dev\project080525\data"
db_path = BASE_FOLDER + "\dbimg.db"

def add_user(username):
    try:
        con = sq.connect(db_path) 
        cur = con.cursor()
        
        # проверка существования БД
        cur.execute('''
            CREATE TABLE IF NOT EXISTS "users" (
                "id_users"	TEXT NOT NULL UNIQUE,
                "original"	BLOB,
                "check"	BLOB,
                PRIMARY KEY("id_users")
            );
        ''')

        
        # вставка данных
        cur.execute(f"""INSERT INTO "users" ("id_users") 
                        VALUES ("{str(username)}");""") 
        con.commit()

    except sq.Error as e:
        print(f'Ошибка открытия БД {e}')
    except Exception as ex:
        print(f'Другая ошибка {ex}')
    con.close()

def insert_image(username, img_path, original_or_check):
    # открыть изображение для чтения
    try:
        with open(img_path, 'rb') as img:
            img_data = img.read()
    except:
        print('Ошибка чтения изображения')
        raise

    try:
        con = sq.connect(db_path) 
        cur = con.cursor()
        
        # проверка существования БД
        cur.execute('''
            CREATE TABLE IF NOT EXISTS "users" (
                "id_users"	TEXT NOT NULL UNIQUE,
                "original"	BLOB,
                "check"	BLOB,
                PRIMARY KEY("id_users")
            );
        ''')

        
        # вставка данных
        print(original_or_check, img_data, username)
        query = f"UPDATE users SET {original_or_check} = ? WHERE id_users = ?;"
        cur.execute(query, (img_data, username))

        if  cur.rowcount == 0:
            print(f'{username} не найден')
        else:
            print(f'Изображение добавлено')

        con.commit()        


    except sq.Error as e:
        print(f'Ошибка открытия БД {e}')
    except Exception as ex:
        print(f'Другая ошибка {ex}')
    
    con.close()





#извлечь файл
def retrieve_image(name_file):
    

    try:
        con = sq.connect(db_path) 
        cur = con.cursor()
        
       
        # вставка данных
        cur.execute("SELECT image FROM images WHERE name=?", (name_file,))
        res = cur.fetchone()

        con.close()

        if res:
            file = open('image_text'+'.'+name_file.split('.')[-1], 'wb') # надо найти место для сохранения изображения
            file.write(res[0])
        else:
            print('файла нет')

    except sq.Error as e:
        print(f'Ошибка открытия БД {e}')
    except Exception as ex:
        print(f'Другая ошибка {ex}')



if __name__ == "__main__":


    main_dir = os.getcwd()
    folder_path =f'{main_dir}\\data\\{username}' 
    
    
    os.makedirs(folder_path, exist_ok=True)