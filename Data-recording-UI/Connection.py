import psycopg2

# Table names
subject = 'subject'
researcher = 'researcher'
data = 'processed_data'

# Update connection string information
host = "Azure host name Place Holder"
dbname = "Database name Place Holder"
user = "User name from Azure Place Holder"
password = "Password Place Holder"
sslmode = "require"

# Construct connection string
conn_string = "host={0} user={1} dbname={2} password={3} sslmode={4}".format(host, user, dbname, password, sslmode)
conn = psycopg2.connect(conn_string)
print("Connection established")

cursor = conn.cursor()


# Methods to query database
def insert(table, *args):
    """ Handles insertions into any of the 3 tables in our azure database"""
    ins_query = ""
    val = ""
    if table is subject:
        ins_query = "INSERT INTO subject (researcher_id, age, weight, height, bmi, ethnicity, fitzpatrick, gender) " \
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"
        val = (args[0], args[1], args[2], args[3], args[4], args[5], args[6], args[7])
    elif table is researcher:
        ins_query = "INSERT INTO researcher (email, passwrd, f_name, m_initial, l_name, institution) " \
                    "VALUES (%s, %s, %s, %s, %s, %s);"
        val = (args[0], args[1], args[2], args[3], args[4], args[5])
    elif table is data:
        ins_query = "INSERT INTO processed_data (body_location, subject_id, wave_length, absorbance, time_date) " \
                    "VALUES (%s, %s, %s, %s, %s);"
        val = (args[0], args[1], args[2], args[3], args[4], args[5])

    cursor.execute(ins_query, val)
    conn.commit()


def multi_select(column, table):
    """ Select a whole column from a table """
    cursor.execute(f"SELECT {column} FROM {table};")
    output = cursor.fetchall()
    return output


def select(column, table, pk, pk_val):
    """ Select a specific value from a table by inputting primary key """
    select_query = f"SELECT {column} FROM {table} WHERE {pk} = %s;"
    val = (pk_val,)
    cursor.execute(select_query, val)
    output = cursor.fetchone()
    return output[0]


def email_exist(an_email):
    """ Checks for input email to see if it already exists in db """
    email_list = multi_select('email', researcher)
    for email in email_list:
        if an_email == email[0]:
            return True

    return False


def close():
    """ Close connection to Azure database. Must be called at the end """
    cursor.close()
    conn.close()

