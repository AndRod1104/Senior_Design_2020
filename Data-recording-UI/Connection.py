import psycopg2

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


def insert(table, a, b, c, d, e, f, g, h):
    if table is 'subject':
        ins_query = "INSERT INTO subject (researcher_id, age, weight, height, bmi, ethnicity, fitzpatrick, gender) " \
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"
        vals = (a, b, c, d, e, f, g, h)
        cursor.execute(ins_query, vals)
        print('inserted into subject')


def close_conn():
    # Clean up
    conn.commit()
    cursor.close()
    conn.close()