import re
import requests
import logging

logging.basicConfig(level=logging.NOTSET)


def extract_table_columns(sql_content):
    create_table_pattern = re.compile(
        r'CREATE TABLE\s+"?(\w+)"?\s*\((.*?)\);', re.DOTALL | re.IGNORECASE)

    CONSTRAINTS_CODES = {'check', 'not null',
                         'unique', 'primary', 'foreign'}

    table_columns = {}

    match = create_table_pattern.search(sql_content)
    if match:
        table_name = match.group(1)
        columns_content = match.group(2)
        columns = {}
        rows = [row.strip() for row in columns_content.split(',')]

        for row in rows:
            column_pattern = re.compile(
                r'"?(\w+)"?\s+(\w+(?:\(\d+\))?)\s*(?:\s+(.*))?$')
            match_col = column_pattern.match(row)
            if match_col:
                column_name = match_col.group(1)
                column_type = match_col.group(2)
                constraints = match_col.group(3)

                if column_name in CONSTRAINTS_CODES:
                    continue

                column_info = {'typeOfColumn': column_type,
                               'constraints': [constraints.strip()] if constraints else None}
                columns[column_name] = column_info

        table_columns[table_name] = columns

    return table_columns


def generate_insert_statements(table_columns):
    for table_name, columns in table_columns.items():
        print(f"\n-- INSERT statements for table: {table_name}")
        values_placeholder = ', '.join(['%s'] * len(columns))
        print(
            f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({values_placeholder});")


def generate_insert_statement_from_ai(sql_content):
    logging.info(f"Generating INSERT Statements for table {sql_content}")
    prompt = (
        f"Generate me random fake data for the following table:"
        f"{sql_content}"
        f"Make it into insert statements and give me only the insert statements in your response."
        f"Format it as:"
        f"INSERT into..."
        f"Values (...)"
        f"Values (...)"
        f"Make 10 statements"
    )
    res = requests.get(f"https://api.freegpt4.ddns.net/?text={prompt}")
    print(res)
    print(res.text)
    return ''


if __name__ == "__main__":
    sql_content = """
        create table "address" (
            "customer_id" bigint,
            "id" bigint not null,
            "address_line" varchar(255),
            "city" varchar(255), 
            "coordinates" varchar(255),
            "country" varchar(255),
            "postal_code" varchar(255),
            "street_number" varchar(255),
            "unit_number" varchar(255), 
            primary key ("id"),
            foreign key ("customer_id") references "customer"
        );
        """

    insert_statement = generate_insert_statement_from_ai(sql_content)
