import psycopg2

subject = 'subject'
researcher = 'researcher'
data = 'processed_data'

# Update connection string information
host = "wearable-bmi-db.postgres.database.azure.com"
dbname = "bmi"
user = "jose@wearable-bmi-db"
password = "seniorproject1."
sslmode = "require"

# Construct connection string
conn_string = "host={0} user={1} dbname={2} password={3} sslmode={4}".format(host, user, dbname, password, sslmode)
conn = psycopg2.connect(conn_string)
print("Connection established")

cursor = conn.cursor()


def insert(table, *args):
    """ Handles insertions into any of the 3 tables in our azure database"""
    if table is 'subject':
        ins_query = "INSERT INTO subject (researcher_id, age, weight, height, bmi, ethnicity, fitzpatrick, gender) " \
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"
        vals = (args[0], args[1], args[2], args[3], args[4], args[5], args[6], args[7])
        cursor.execute(ins_query, vals)
        print('inserted into subject')


def commit():
    """ Saves modifications to database like insertions remotely """
    conn.commit()


def close():
    """ Close connection to Azure database. Must be called at the end """
    cursor.close()
    conn.close()

