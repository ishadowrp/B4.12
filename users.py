# импортируем модули стандартной библиотеки uuid и datetime
import uuid
import datetime

# импортируем библиотеку sqlalchemy и некоторые функции из нее 
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# константа, указывающая способ соединения с базой данных
DB_PATH = "sqlite:///sochi_athletes.sqlite3"
# базовый класс моделей таблиц
Base = declarative_base()

class User(Base):
    """
    Описывает структуру таблицы user для хранения регистрационных данных пользователей
    """
    # задаем название таблицы
    __tablename__ = 'user'
    # идентификатор пользователя, первичный ключ
    id = sa.Column(sa.Integer, primary_key=True)
    # имя пользователя
    first_name = sa.Column(sa.Text)
    # фамилия пользователя
    last_name = sa.Column(sa.Text)
    # пол пользователя
    gender = sa.Column(sa.Text)
    # адрес электронной почты пользователя
    email = sa.Column(sa.Text)
    # дата рождения
    birthdate = sa.Column(sa.Text)
    # рост
    height = sa.Column(sa.REAL)

# Функция для установления соединения с базой данных.
def connect_db():
    """
    Устанавливает соединение к базе данных, создает таблицы, если их еще нет и возвращает объект сессии 
    """
    # создаем соединение к базе данных
    engine = sa.create_engine(DB_PATH)
    # создаем описанные таблицы
    Base.metadata.create_all(engine)
    # создаем фабрику сессию
    session = sessionmaker(engine)
    # возвращаем сессию
    return session()

def request_data(count_of_usr):
    """
    Запрашивает у пользователя данные и добавляет их в список users
    """
    # выводим приветствие
    print("Добрый день. Введите пожалуйста свои данные.")
    # запрашиваем у пользователя данные
    first_name = input("Введи своё имя: ")
    last_name = input("Фамилию: ")
    gender = input("Введите свой пол ('Male' - мужской/'Female' - женский): ")
    email = input("адрес электронной почты: ")
    birthdate = input("Дату рождения (ГГГГ-ММ-ДД): ")
    height = input("Введите свой рост: ")
    # генерируем идентификатор пользователя и сохраняем его строковое представление
    user_id = count_of_usr
    # создаем нового пользователя
    user = User(
        id=user_id,
        first_name=first_name,
        last_name=last_name,
        gender=gender,
        email=email,
        birthdate=birthdate,
        height=height
    )
    # возвращаем созданного пользователя
    return user

def main():
    """
    Осуществляет взаимодействие с пользователем, обрабатывает пользовательский ввод
    """
    session = connect_db()
    # устанавливаем признак неоходимости добавления пользователя
    need_input_user = True
    # Запрашиваем количество пользователей в таблице user для определения следующего номера ID
    count_of_usr =  session.query(User).count()
    # создаем цикл для ввода списка пользователей
    while need_input_user:
        # устанавливаем новый номер id
        count_of_usr += 1
        # запрашиваем данные пользоватлея
        user = request_data(count_of_usr)
        # добавляем нового пользователя в сессию
        session.add(user)
        # задаем вопрос необходимо ли ввести еще одного пользователя
        new_user = input("Хотите добавить еще одного пользовател? (Y/N): ")
        # при согласии продолжаем цикл
        if new_user.upper() == "Y":
            need_input_user = True
        else:
            # если ответ пользователя отдичается от "Y/y" тогда выходим из цикла.
            need_input_user = False  

    # сохраняем все изменения, накопленные в сессии
    session.commit()

if __name__ == "__main__":
    main()
