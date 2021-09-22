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


def calculate_hardware_burden(model):
    hw = 0
    if model.cpu and model.cpu.gflops and model.number_of_cpus:
        hw = hw + model.cpu.gflops * model.number_of_cpus
    if model.gpu and model.gpu.gflops and model.number_of_gpus:
        hw = hw + model.gpu.gflops * model.number_of_gpus
    if model.tpu and model.tpu.gflops and model.number_of_tpus:
        hw = hw + model.tpu.gflops * model.number_of_tpus

    if model.training_time:
        hw = hw * model.training_time
    else:
        hw = None

    return hw if hw else None
