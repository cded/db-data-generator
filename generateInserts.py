import re
import logging
from dotenv import load_dotenv
import os
import google.generativeai as genai
import asyncio

load_dotenv()


logging.basicConfig(level=logging.NOTSET)

genai.configure(api_key=os.environ['GEMINI_API_KEY'])
model = genai.GenerativeModel('gemini-pro')


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


def extract_inserts(response):
    sql_pattern = re.compile(r'```sql(.*?)```', re.DOTALL)
    sql_matches = sql_pattern.findall(response)
    return sql_matches


async def generate_insert_statement_from_ai(sql_content: str):
    if not sql_content.lower().startswith('create table'):
        logging.error("Not a valid SQL statement")
        return
    logging.info(f"Generating INSERT Statements for table {sql_content}")
    prompt = (
        f"{sql_content}"
        f"Generate me random fake data for the following tables:"
        f"Make it into insert statements and give me only the insert statements in your response."
        f"Format it as:"
        f"INSERT into..."
        f"Values (...)"
        f"(...)"
        f"Make 10 statements"
        f"Note that bigserial is a number. Each row table has an id."
    )

    response = await model.generate_content_async(prompt)

    sql_inserts = []
    try:
        sql_inserts = extract_inserts(response.text)
    except:
        logging.info(f"Multiple candidates found")
        sql_inserts = extract_inserts(
            response.candidates[0].content.parts)

    return sql_inserts


def write_queries_to_file(file_path, queries):
    with open(file_path, 'a') as output_file:
        for query in queries:
            output_file.write(query.strip())


async def main():
    input_file_path = './my-schema.sql'
    output_file_path = 'extracted_sql_statements.sql'

    result_queries = []

    with open(input_file_path, 'r') as sql_file:
        corouts = [generate_insert_statement_from_ai(
            line) for line in sql_file]
        for coro in asyncio.as_completed(corouts):
            result = await coro
            if result:
                result_queries.extend(result)

    write_queries_to_file(output_file_path, result_queries)


if __name__ == "__main__":
    asyncio.run(main())
