from fastapi.responses import FileResponse
import secrets
from enum import Enum
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from returngraph import sel_one_cur






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
    correct_username = secrets.compare_digest(credentials.username, "losandtok")
    correct_password = secrets.compare_digest(credentials.password, "yan432678")
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
async def main(currency_name: CurrencyName):
    sel_one_cur(currency_name)
    return FileResponse("figure.png")

