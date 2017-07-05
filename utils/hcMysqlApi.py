import pymysql.cursors
import pymysql

def init(config):
    global connection
    connection = pymysql.connect(host=config['db']['host'],
                             user='root',
                             password=config['passwords']['rdsPassword'],
                             db=config['db']['db'],
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

def printRecords(config):
    try:
        init (config)
        with connection.cursor() as cursor:
        # Read a single record
            sql = "SELECT * FROM " + config['db']['table']
            cursor.execute(sql)
            result = cursor.fetchone()
            print(result)
    finally:
        connection.close()

def addRecord(config, stats):
    try:
        init (config)
        with connection.cursor() as cursor:
        # Read a single record
            sql = "INSERT INTO " + config['db']['table'] + "(`foodName`, `updateTime`, `notificationSent`, `lastModified`, `notificationSentTimeStamp`) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (stats['foodName'], stats['updateTime'], stats['notificationSent'], stats['lastModified'], stats['notificationSentTimeStamp']))
            connection.commit()
            result = cursor.fetchone()
            print(result)
    finally:
        connection.close()

def addRecordStub(config):
    stats = {}
    stats['foodName'] = "three-strawberries.jpg"
    stats['updateTime'] = "2017-06-28T19:25:18.001Z"
    stats['notificationSent'] = "false"
    stats['lastModified'] = "2017-06-28T19:25:18.001Z"
    stats['notificationSentTimeStamp'] = "1970-01-01T00:00:00.000Z"
    addRecord(config, stats)