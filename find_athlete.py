# импортируем модули стандартной библиотеки uuid и datetime
import uuid
import datetime

# импортируем библиотеку sqlalchemy и некоторые функции из нее 
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import func

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

class Athletes(Base):
    """
    Описывает структуру таблицы user для хранения регистрационных данных пользователей
    """
    # задаем название таблицы
    __tablename__ = 'athelete'
    # идентификатор пользователя, первичный ключ
    id = sa.Column(sa.Integer, primary_key=True)
    # возраст
    age = sa.Column(sa.Integer)
    # день рождения
    birthdate = sa.Column(sa.Text)
    # пол
    gender = sa.Column(sa.Text)
    # рост
    height = sa.Column(sa.REAL)
    # имя 
    name = sa.Column(sa.Text)
    # вес
    weight = sa.Column(sa.Integer)
    # количество золотых медалей
    gold_medals = sa.Column(sa.Integer)
    # количество серебрнных медалей
    silver_medals = sa.Column(sa.Integer)
    # количество бронзовых медалей
    bronze_medals = sa.Column(sa.Integer)
    # всего медалей
    total_medals = sa.Column(sa.Integer)
    # вид спорта
    sport = sa.Column(sa.Integer)
    # страна
    country = sa.Column(sa.Integer)    

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

def find(session, birthdate, height):

    # Создадим запрос к таблице с атлетами по поиску атлета ближайшего по возрасту к пользователю
    query_athlete_1 = session.query(Athletes).order_by(func.abs(func.julianday(Athletes.birthdate) - func.julianday(birthdate))).first()
    # Создадим запрос к таблице с атлетами по поиску атлета ближайшего по росту
    query_athlete_2 = session.query(Athletes).order_by(func.abs(Athletes.height - height)).first()

    # Выведем результаты
    print("Ближайший атлет по возрасту к пользователю: {} из {}".format(query_athlete_1.name, query_athlete_1.country))
    print("Ближайший атлет по росту к пользователю: {} из {}".format(query_athlete_2.name, query_athlete_2.country))

def main():
    """
    Осуществляет взаимодействие с пользователем, обрабатывает пользовательский ввод
    """
    session = connect_db()

    # Устанавливаем значение для цикла при опросе пользователя
    flag = True
    # для того чтоб модуль работал не единоразово, а можно было проверть нескольких пользователей возьмем все в цикл
    while flag:
        # Запрашиваем идентификатор пользователя
        user_id = input("Введите идентификатор пользователя: ")
        # Выполняем запрос к БД
        query = session.query(User).filter(User.id == user_id).first()
        # Проверяем есть ли такой пользоваель или запрос пуст
        if query is not None:
            find(session, query.birthdate, query.height)
            # После вывода ответа, уточним у пользователя хочет ли он повторить попытку
            answer = input("Хотите попробовать еще раз? (Y/N): ")
            # Проверим ответ пользователя
            if answer.upper() == "Y":
                # установим необходимое значение для продолжения работы модуля
                flag = True
            else:
                # установим необходимое значение для прекращения работы модуля
                flag = False
        else:
            # Выведем сообщение об ошибке и уточним у пользователя хочет ли он повторить попытку
            answer = input("Вы ввели ошибочный идентификатор пользователя. Попробовать еще раз? (Y/N): ")
            # Проверим ответ пользователя
            if answer.upper() == "Y":
                # установим необходимое значение для продолжения работы модуля
                flag = True
            else:
                # установим необходимое значение для прекращения работы модуля
                flag = False

if __name__ == "__main__":
    main()
