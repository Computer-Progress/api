from slugify import slugify
import datetime
import gspread
from urllib import response
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi_cache.decorator import cache
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend


app = FastAPI(
    title='ComputerProgress', openapi_url=f"/api/v1/openapi.json"
)

app.add_middleware(GZipMiddleware, minimum_size=1000)

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    FastAPICache.init(InMemoryBackend(), prefix="fastapi-cache")


def getData(ws_name):
    gc = gspread.service_account(filename='./computerprogress.json')
    sh = gc.open_by_key('1xthNnZ_I43SUXzLvuP7TFXsd-XeHDUx_4dedH5sE2GM')
    worksheet = sh.worksheet(ws_name)
    if not worksheet:
        raise Exception(f"Worksheet {ws_name} not found")
    values = worksheet.get_all_values()
    [header, _, _, _, *data] = values
    dataset = []
    for row in data:
        item = {}
        for i in range(len(header)):
            item[header[i]] = row[i]
        dataset.append(item)
    return dataset


@app.get("/api/v1/metrics/{task_dataset_identifier}")
@cache(expire=60)
async def hardware_burden(task_dataset_identifier):
    print('calling')
    dataset = getData(task_dataset_identifier)
    response = []
    for item in dataset:
        new_item = {
            "model_name": item['name'] or None,
            "model_identifier":  slugify(
                item['name'],
                max_length=45,
                word_boundary=True
            ) or None,
            "model_hardware_burden": item['computing_power'] or None,
            "model_network_operations": item['network_operations'] or None,
            "paper_title": item['title'] or None,
            "paper_pwc_link": item['paper_with_code'] or None,
            "paper_link": item['paper_link'] or None,
            "model_operation_per_network_pass": item['flops'] if item['flops'] else (item['multiadds'] * 2 if item['multiadds'] else None),
        }
        response.append(new_item)
    return response


@app.get("/")
@cache(expire=60)
async def main():
    gc = gspread.service_account(filename='./computerprogress.json')
    sh = gc.open_by_key('1xthNnZ_I43SUXzLvuP7TFXsd-XeHDUx_4dedH5sE2GM')
    worksheet_list = sh.worksheets()
    bechmarks = []
    for worksheet in worksheet_list:
        if worksheet.title != 'benchmarks':
            bechmarks.append(
                {'name': worksheet.title, 'url': '/api/v1/metrics/' + worksheet.title}
            )
    response = {
        'benchmarks': bechmarks,
    }

    return response
