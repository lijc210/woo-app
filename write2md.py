# coding: utf-8
"""
@File    :   main.py
@Time    :   2023/05/05 18:46:35
@Author  :   lijc210@163.com
@Desc    :   
"""
import uvicorn
from fastapi import FastAPI
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/upload_cf")
async def get_jobs():
    """
    打包完，调用此接口，上传到cloudflares
    """
    
    
    return {"message": "Hello World"}

@app.get("/updater")
async def get_jobs():
    """
    返回最新的包
    """
    
    return {"message": "Hello World"}




if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=15604)
