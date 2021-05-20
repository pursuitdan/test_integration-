import sqlite3

# db_name = the name of the database
def create_table_db(db_name):
    # SQL statements
    sql_drop_entries = '''
        DELETE FROM uniqueMAC1;
    '''
    sql_create_table = '''
        CREATE TABLE IF NOT EXISTS uniqueMAC1(
            TX TEXT,
            RX TEXT,
            SNR REAL,
            ID REAL);
        '''
    # connect to database
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    # execute sql
    cur.execute(sql_create_table)
    cur.execute(sql_drop_entries)

    # end up execution
    con.commit()
    cur.close()
    con.close()

def read_all_records_db(db_name):
    # SQL statements
    sql_read_record = '''
        SELECT * FROM uniqueMAC1;
        '''
    # connect to database
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    # execute sql
    cur.execute(sql_read_record)
    result = cur.fetchall()
    # end up execution
    con.commit()
    cur.close()
    con.close()
    return result

def log_results(results):
    with open('query_output','w') as f:
        for r in results:
            tx = r[0]
            rx = r[1]
            snr = r[2]
            id=r[3]
            f.write('{},{},{},{}'.format(tx,rx,snr,id))

def printlog(db_name):
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    cur.execute('SELECT * FROM uniqueMAC1')
    for row in cur:
        print(row)

# log = a file pointer to log the output
def analysis(log):
   
    conn = sqlite3.connect('test.db')
    cur = conn.cursor()

    cur.execute('SELECT TX FROM (SELECT * FROM uniqueMAC1 ORDER BY ID DESC LIMIT 10 ) GROUP BY TX')
    #print('Printing analysis data')
    output=[]
    for row in cur:
        output.append(row)

    cur.execute('SELECT RX FROM (SELECT * FROM uniqueMAC1 ORDER BY ID DESC LIMIT 10 ) GROUP BY RX ')
    for row in cur:
        output.append(row)

    conn.commit()
    conn.close()
    unique_output=set(output)
    log.write('{}\n'.format(len(unique_output)))




