from fastapi.responses import FileResponse
import secrets
from enum import Enum
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from returngraph import  take_percent_change_sev_cur






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




@app.get("/sev_currencies/{first_cur}")
async def main(first_cur: CurrencyName, username=Depends(get_current_username), second_cur: CurrencyName =None, third_cur:CurrencyName =None, four_cur:CurrencyName=None):
    l = [j for j in [first_cur, second_cur, third_cur, four_cur] if j != None]

    take_percent_change_sev_cur(l)
    return FileResponse("C:/Users/Ольга/PycharmProjects/fastapi_clone/percent_changes.png")

