from sqlalchemy.sql.expression import text
import logging


def parseInt(value):
    try:
        return int(float(value))
    except Exception:
        return None


def parseFloat(value):
    try:
        return float(value)
    except Exception:
        return None


def executeSQLfromFile(db, filename):
    sql_file = open(filename, 'r')

    sql_command = ''

    for line in sql_file:
        if not line.startswith('--') and line.strip('\n'):
            sql_command += line.strip('\n')
            if sql_command.endswith(';'):
                try:
                    db.execute(text(sql_command))
                except Exception as e:
                    logging.error(e)
                finally:
                    sql_command = ''
