from fastapi.responses import FileResponse
import secrets
from enum import Enum
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from returngraph import sel_one_cur, take_percent_change_sev_cur
import uvicorn





class CurrencyName(str, Enum):
    USD = "USD"
    EUR = "EUR"
    BTC = "BTC"
    UAH = "UAH"
    PLN = "PLN"
    BYN = "BYN"


app = FastAPI()

security = HTTPBasic()


def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "yan")
    correct_password = secrets.compare_digest(credentials.password, "2508")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username




@app.get("/users/me")
def read_current_user(username: str = Depends(get_current_username)):
    return {"username": username}


@app.get("/currencies/{currency_name}")
async def main(currency_name: CurrencyName, username = Depends(get_current_username)):
    sel_one_cur(currency_name)
    return FileResponse("figure.png")

@app.get("/sev_currencies/{first_cur}")
async def main(first_cur, username = Depends(get_current_username), second_cur=None, third_cur =None, four_cur=None):
    l = [j for j in [first_cur, second_cur, third_cur, four_cur] if j != None]

    take_percent_change_sev_cur(l)
    return FileResponse("percent_changes.png")

if __name__ == "__main__":
    uvicorn.run("main:app",host='127.0.0.1', port=8000, reload=True, debug=True, workers=1)