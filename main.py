from fastapi import FastAPI

app = FastAPI()





@app.get("/")
async def root():
    return {"message": "Hello World"}
@app.get("/plus/{x}/{y}")
async def sum(x, y):
    return {int(x) +int(y)}
@app.get("/multiply/{x}/{y}")
async def sum(x, y):
    return {int(x) * int(y)}
@app.get("/difference/{x}/{y}")
async def difference(x,y):
    return {int(x) - int(y)}
