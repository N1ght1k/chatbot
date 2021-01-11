import myconnutils
from datetime import timedelta, datetime
import traceback

today = datetime.today()
tomorrow = today + timedelta(days=1)


def like_update(value):
    new_value = '%' + str(value) + '%'
    return new_value


def dep_flight_number(flight_number):
    connection = myconnutils.get_connection()
    sql_query = 'SELECT * FROM departure WHERE ru_flight_number LIKE \'%s\' ' \
                'AND (plan LIKE \'%s\' OR plan LIKE \'%s\');' \
                % (like_update(flight_number), like_update(today.strftime("%d.%m")),
                   like_update(tomorrow.strftime("%d.%m")))
    cursor = connection.cursor()
    cursor.execute(sql_query)
    result = cursor.fetchall()
    connection.close()
    return result


def dep_city(city):
    connection = myconnutils.get_connection()
    sql_query = 'SELECT * FROM departure WHERE (ru_airport LIKE \'%s\' OR ru_airport_1 LIKE \'%s\') ' \
                'AND (plan LIKE \'%s\' OR plan LIKE \'%s\');' \
                % (like_update(city), like_update(city), like_update(today.strftime("%d.%m")),
                   like_update(tomorrow.strftime("%d.%m")))
    cursor = connection.cursor()
    cursor.execute(sql_query)
    result = cursor.fetchall()
    connection.close()
    return result


def arr_flight_number(flight_number):
    connection = myconnutils.get_connection()
    sql_query = 'SELECT * FROM arrival WHERE ru_flight_number LIKE \'%s\' ' \
                'AND (plan LIKE \'%s\' OR plan LIKE \'%s\');' \
                % (like_update(flight_number), like_update(today.strftime("%d.%m")),
                   like_update(tomorrow.strftime("%d.%m")))
    cursor = connection.cursor()
    cursor.execute(sql_query)
    result = cursor.fetchall()
    connection.close()
    return result


def arr_city(city):
    connection = myconnutils.get_connection()
    sql_query = 'SELECT * FROM arrival WHERE (ru_airport LIKE \'%s\' OR ru_airport_1 LIKE \'%s\') ' \
                'AND (plan LIKE \'%s\' OR plan LIKE \'%s\');' \
                % (like_update(city), like_update(city), like_update(today.strftime("%d.%m")),
                   like_update(tomorrow.strftime("%d.%m")))
    cursor = connection.cursor()
    cursor.execute(sql_query)
    result = cursor.fetchall()
    connection.close()
    return result


def arr_city_today(city):
    connection = myconnutils.get_connection()
    sql_query = 'SELECT * FROM arrival WHERE (ru_airport LIKE \'%s\' OR ru_airport_1 LIKE \'%s\') ' \
                'AND (plan LIKE \'%s\');' \
                % (like_update(city), like_update(city), like_update(today.strftime("%d.%m")))
    cursor = connection.cursor()
    cursor.execute(sql_query)
    result = cursor.fetchall()
    connection.close()
    return result


def arr_city_tomorrow(city):
    connection = myconnutils.get_connection()
    sql_query = 'SELECT * FROM arrival WHERE (ru_airport LIKE \'%s\' OR ru_airport_1 LIKE \'%s\') ' \
                'AND (plan LIKE \'%s\');' \
                % (like_update(city), like_update(city), like_update(tomorrow.strftime("%d.%m")))
    cursor = connection.cursor()
    cursor.execute(sql_query)
    result = cursor.fetchall()
    connection.close()
    return result


def dep_city_today(city):
    connection = myconnutils.get_connection()
    sql_query = 'SELECT * FROM departure WHERE (ru_airport LIKE \'%s\' OR ru_airport_1 LIKE \'%s\') ' \
                'AND (plan LIKE \'%s\');' \
                % (like_update(city), like_update(city), like_update(today.strftime("%d.%m")))
    cursor = connection.cursor()
    cursor.execute(sql_query)
    result = cursor.fetchall()
    connection.close()
    return result


def dep_city_tomorrow(city):
    connection = myconnutils.get_connection()
    sql_query = 'SELECT * FROM departure WHERE (ru_airport LIKE \'%s\' OR ru_airport_1 LIKE \'%s\') ' \
                'AND (plan LIKE \'%s\');' \
                % (like_update(city), like_update(city), like_update(tomorrow.strftime("%d.%m")))
    cursor = connection.cursor()
    cursor.execute(sql_query)
    result = cursor.fetchall()
    connection.close()
    return result


def check_subscribe(user, flight_id):
    connection = myconnutils.get_connection()
    sql_query = 'SELECT * FROM subscribes WHERE user = \'%s\' AND flight = \'%s\';' % (user, flight_id)
    cursor = connection.cursor()
    cursor.execute(sql_query)
    result = cursor.fetchall()
    connection.close()
    return result


def add_subscribe(user, flight_id):
    connection = myconnutils.get_connection()
    sql_query = 'INSERT INTO subscribes (user, flight) VALUES (\'%s\', \'%s\');' % (user, flight_id)
    try:
        cursor = connection.cursor()
        cursor.execute(sql_query)
        connection.commit()
    except Exception:
        print('Ошибка:\n', traceback.format_exc())
    connection.close()


def get_status():
    connection = myconnutils.get_connection()
    sql_query_dep = 'SELECT subscribes.flight, departure.status FROM subscribes, departure ' \
                    'WHERE subscribes.flight = departure.flight_id;'
    sql_query_arr = 'SELECT subscribes.flight, arrival.status FROM subscribes, arrival ' \
                    'WHERE subscribes.flight = arrival.flight_id;'
    cursor = connection.cursor()
    cursor.execute(sql_query_dep)
    result_dep = cursor.fetchall()
    cursor.execute(sql_query_arr)
    result_arr = cursor.fetchall()
    result = {'departure': list(result_dep), 'arrival': list(result_arr)}
    connection.close()
    return result


def get_by_flight_id(orient, flight_id):
    connection = myconnutils.get_connection()
    sql_query = ''
    if orient == 'departure':
        sql_query = 'SELECT * FROM departure WHERE flight_id = \'%s\';' % flight_id
    if orient == 'arrival':
        sql_query = 'SELECT * FROM arrival WHERE flight_id = \'%s\';' % flight_id
    print(sql_query)
    cursor = connection.cursor()
    cursor.execute(sql_query)
    result = cursor.fetchone()
    connection.close()
    return result


def get_users(flight_id):
    connection = myconnutils.get_connection()
    sql_query = 'SELECT user FROM subscribes WHERE flight = \'%s\';' % flight_id
    cursor = connection.cursor()
    cursor.execute(sql_query)
    result = cursor.fetchall()
    connection.close()
    return result


def del_sub(user):
    connection = myconnutils.get_connection()
    sql_query = 'DELETE FROM subscribes WHERE user = \'%s\';' % user
    try:
        cursor = connection.cursor()
        cursor.execute(sql_query)
        connection.commit()
    except Exception:
        print('Ошибка:\n', traceback.format_exc())
    connection.close()


def del_all_subs():
    connection = myconnutils.get_connection()
    sql_query = 'SELECT DISTINCT flight FROM subscribes;'
    cursor = connection.cursor()
    cursor.execute(sql_query)
    result = cursor.fetchall()
    for item in result:
        sql_query_dep = 'SELECT status FROM departure WHERE flight_id = \'%s\';' % item['flight']
        cursor.execute(sql_query_dep)
        status = cursor.fetchone()
        if status:
            if status['status'] == 'ВЫЛЕТЕЛ' or status['status'] == 'ОТМЕНЕН':
                sql_query_del = 'DELETE FROM subscribes WHERE flight = \'%s\';' % item['flight']
                cursor.execute(sql_query_del)
        else:
            sql_query_arr = 'SELECT status FROM arrival WHERE flight_id = \'%s\';' % item['flight']
            cursor.execute(sql_query_arr)
            status = cursor.fetchone()
            if status:
                if status['status'] == 'ПРИБЫЛ' or status['status'] == 'ОТМЕНЕН':
                    sql_query_del = 'DELETE FROM subscribes WHERE flight = \'%s\';' % item['flight']
                    cursor.execute(sql_query_del)
    connection.close()
