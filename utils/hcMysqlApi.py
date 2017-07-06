import pymysql.cursors
import pymysql

def init(config):
    connection = pymysql.connect(host=config['db']['host'],
                             user='root',
                             password=config['passwords']['rdsPassword'],
                             db=config['db']['db'],
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
    return connection

# please note that you're supposed to get a connection here - so you're suppose to close it after using the function!
def isLatestDate(config, feedingDate, cursor):
    sql = "SELECT COUNT(*) as count FROM " + config['db']['table'] + " WHERE 'lastModified' >= '" + feedingDate + "'"
    print sql
    cursor.execute(sql)
    result = cursor.fetchone()
    if (result["count"] > 0):
        print ("Cat was fed at a later time than " + feedingDate + ", skipping...")
        return False
    return True

def printRecords(config):
    connection = init(config)
    try:
        with connection.cursor() as cursor:
        # Read a single record
            sql = "SELECT * FROM " + config['db']['table']
            cursor.execute(sql)
            result = cursor.fetchone()
            print(result)
    finally:
        connection.close()

def addRecord(config, stats):
    connection = init(config)
    try:
        with connection.cursor() as cursor:
        # Read a single record
            if not isLatestDate(config, stats['lastModified'], cursor):
                return
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