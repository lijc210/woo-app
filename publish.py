# coding: utf-8
"""
@File    :   main.py
@Time    :   2023/05/05 18:46:35
@Author  :   lijc210@163.com
@Desc    :   
"""
import uvicorn
from fastapi import FastAPI
from utils import upload_cf
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/upload_cf")
async def upload_cf():
    upload_cf()
    return {"message": "Hello World"}

@app.get("/updater")
async def updater():

    
    return {"message": "Hello World"}




if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=15604)
