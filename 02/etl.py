import psycopg2


drop_table_queries = [
    "DROP TABLE IF EXISTS events",
]
create_table_queries = [
    """
    CREATE TABLE IF NOT EXISTS staging_events (
        id text,
        type text,
        actor text,
        repo text,
        created_at text
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS events (
        id int
    )
    """,
]
copy_table_queries = [
    """
    COPY staging_events FROM 's3://zkan-swu-labs/github_events_01.json'
    CREDENTIALS 'aws_iam_role=arn:aws:iam::264405253253:role/AWSServiceRoleForRedshift'
    JSON 's3://zkan-swu-labs/events_json_path.json'
    REGION 'ap-southeast-2'
    """,
]
insert_table_queries = [
    """
    INSERT INTO
      events (
        id
      )
    SELECT
      DISTINCT id,
    FROM
      staging_events
    WHERE
      id NOT IN (SELECT DISTINCT id FROM events)
    """,
]


def drop_tables(cur, conn):
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def load_staging_tables(cur, conn):
    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()

def insert_tables(cur, conn):
    for query in insert_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    host = "redshift-cluster-1.ceh8m2ujwodm.ap-southeast-2.redshift.amazonaws.com:5439/dev"
    dbname = "dev"
    user = "awsuser"
    password = "Jowiwi99%"
    port = "5439"
    conn_str = f"host={host} dbname={dbname} user={user} password={password} port={port}"
    conn = psycopg2.connect(conn_str)
    cur = conn.cursor()

    query = "select * from category"
    cur.execute(query)
    records = cur.fetchall()
    for row in records:
        print(row)

    conn.close()


if __name__ == "__main__":
    main()
