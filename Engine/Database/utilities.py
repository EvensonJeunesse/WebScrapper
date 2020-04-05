import pymysql.cursors   #pip3 install PyMySQL

def OpenDatabase():
    connection = None
    try :
        """connection= pymysql.connect(host='',
                                     user='',
                                     password='',
                                     db='',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)"""

        print ("connect successful!!")
    except:
        print ("connection failure...")
    return connection
