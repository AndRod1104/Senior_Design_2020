import psycopg2

# Table names
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
    if table is subject:
        ins_query = "INSERT INTO subject (researcher_id, age, weight, height, bmi, ethnicity, fitzpatrick, gender) " \
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"
        val = (args[0], args[1], args[2], args[3], args[4], args[5], args[6], args[7])
        cursor.execute(ins_query, val)
    elif table is researcher:
        ins_query = "INSERT INTO researcher (email, passwrd, f_name, m_initial, l_name, institution) " \
                    "VALUES (%s, %s, %s, %s, %s, %s);"
        val = (args[0], args[1], args[2], args[3], args[4], args[5])
        cursor.execute(ins_query, val)
    elif table is data:
        ins_query = "INSERT INTO processed_data (body_location, subject_id, wave_length, absorbance, time_date) " \
                    "VALUES (%s, %s, %s, %s, %s);"
        val = (args[0], args[1], args[2], args[3], args[4], args[5])
        cursor.execute(ins_query, val)


def select(attribute, table, pk, pk_val):
    """ Select a specific value from a table by inputting primary key """
    select_query = "SELECT %s FROM %s WHERE %s = %s;"
    val = (attribute, table, pk, pk_val)
    cursor.execute(select_query, val)
    output = cursor.fetchone()
    return output[0]


def commit():
    """ Saves modifications to database like insertions remotely """
    conn.commit()


def close():
    """ Close connection to Azure database. Must be called at the end """
    cursor.close()
    conn.close()

