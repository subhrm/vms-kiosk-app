import os
import mysql.connector

from vms_kiosk_app import config, logger


def get_connection():
    logger.info("Trying to connect to MySQL database")

    cnx = None

    try:
        uid = os.environ.get("SQL_SERVER_USER_ID")
        pwd = os.environ.get("SQL_SERVER_USER_PWD")
        # print("user id :", uid, "Password" , pwd)
        cnx = mysql.connector.connect(host=config.SQL_SERVER_IP,
                                      port=config.SQL_SERVER_PORT,
                                      user=uid,
                                      password=pwd,
                                      database=config.DB_NAME)
    except Exception:
        logger.exception("SQL Connection failed")

    return cnx


def get_all_visitor_photos():
    '''
        Get photos of all visitors
    '''

    logger.info("Trying to fetch all visitor images")



    try:
        cnx = get_connection()
        cursor = cnx.cursor()
        query = '''
            select v.name, i.image_data
            from visitor v,
                images i
            where v.status = 1 
            and v.actual_photo is not null
            and  v.actual_photo = i.image_id;
        '''
        cursor.execute(query)
        res = cursor.fetchall()
        resp = []
        for row in res:
            resp.append(row)
        cursor.close()
        cnx.close()
    except Exception as ex:
        logger.exception(str(ex))
        #raise Exception("Some thing went wrong")

    return resp

def get_all_poi_photos():
    '''
        Get photos of all persons of interest
    '''

    logger.info("Trying to fetch all poi images")



    try:
        cnx = get_connection()
        cursor = cnx.cursor()
        query = '''
            select p.type, p.name, i.image_data
            from person_of_interest p,
                images i
            where p.image_id is not null
            and  p.image_id = i.image_id;
        '''
        cursor.execute(query)
        res = cursor.fetchall()
        resp = []
        for row in res:
            resp.append(row)
        cursor.close()
        cnx.close()
    except Exception as ex:
        logger.exception(str(ex))
        #raise Exception("Some thing went wrong")

    return resp
