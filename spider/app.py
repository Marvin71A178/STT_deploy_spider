import os , sys
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncio
from starlette.concurrency import run_in_threadpool
import uvicorn
from spider import Novel , Novel_content 


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class process_Novel_class(BaseModel):
    url: str


@app.get("/")
async def root():
    return {"message": "Welcome to the storyteller spider API. Use /docs/ to perform function."}

@app.post("/Novel_catalog/")
async def cat_Novel_catalog(request: process_Novel_class):
    try:
        novel = Novel(request.url)  # 初始化 Novel 對象
        result = await run_in_threadpool(novel.check_website)  # 異步執行網站檢查
        return novel.dic  # 返回字典結果
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/Novel_page_content/")
async def cat_Novel_page_content(request: process_Novel_class):
    try:
        novel_content = Novel_content(request.url)  # 初始化 Novel_content 對象
        content = await run_in_threadpool(novel_content.check_website)  # 異步執行網站檢查
        return novel_content.content  # 返回頁面內容
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == '__main__':
    uvicorn.run(app , host = '0.0.0.0' , port = 8060)
    