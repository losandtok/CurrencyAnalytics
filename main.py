import hashlib
from loguru import logger
import secrets
from fastapi.responses import FileResponse
from enum import Enum
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session


from returngraph import take_percent_change_sev_cur
from timeseries_rates import translate_date
from user_database import crud, schemas, models
from user_database.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

class CurrencyName(str, Enum):
    USD = "USD"
    EUR = "EUR"
    BTC = "BTC"
    UAH = "UAH"
    PLN = "PLN"
    BYN = "BYN"
    RUB = "RUB"


class Day(str, Enum):
    one = '01'
    two = '02'
    three = '03'
    four = '04'
    five = '05'
    six = '06'
    seven = '07'
    eight = '08'
    nine = '09'
    ten = '10'
    eleven = '11'
    twelve = '12'
    thirteen = '13'
    fourteen = '14'
    fifteen = '15'
    sixteen = '16'
    seventeen = '17'
    eighteen = '18'
    nineteen = '19'
    twenty = '20'
    twenty_one = '21'
    twenty_two = '22'
    twenty_three = '23'
    twenty_four = '24'
    twenty_five = '25'
    twenty_six = '26'
    twenty_seven = '27'
    twenty_eight = '28'
    twenty_nine = '29'
    thirty = '30'


class Month(str, Enum):
    January = '01'
    February = '02'
    March = '03'
    April = '04'
    May = '05'
    June = '06'
    July = '07'
    August = '07'
    September = '09'
    Ocrober = '10'
    November = '11'
    December = '12'


class Year(str, Enum):
    eighteen_year = '2018'
    nineteen_year = '2019'
    twenty_year = '2020'
    twenty_one_year = '2021'
    twenty_two_year = '2022'


app = FastAPI()

security = HTTPBasic()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.post("/users/{email}/{password}", response_model=schemas.User)
def create_user(email, password, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, email=email, password=password)




def get_current_username(credentials: HTTPBasicCredentials = Depends(security), db: Session = Depends(get_db)):
    """test /users/me
user.hashed_password != hashed_password:

Output:
(for {
  "email": "r4",
  "p": "444"
  "id": 3,
  "is_active": true,
  "items": []
})

correct_username:True
correct_user_name:r4
password:b'444'
hashed_password:b"\xa1G\xabjM\x16J\x01-\xab\xae\xd4\xf3\x95\xffM\xab\xa6e\xabi'\xe7\xfa=\x94o|\xd5\xa7\x02\xc8"
user.hashed_password:\xc3a64853673e4d6834e1c96b7398598ae91d2f5d815dfb54c3f767245d1bb1d7
correct_password:False


correct_username:True
correct_password:False
correct_user_name:r4
password:b'444'
hashed_password:b"\xa1G\xabjM\x16J\x01-\xab\xae\xd4\xf3\x95\xffM\xab\xa6e\xabi'\xe7\xfa=\x94o|\xd5\xa7\x02\xc8"
user.hashed_password:\xc3a64853673e4d6834e1c96b7398598ae91d2f5d815dfb54c3f767245d1bb1d7


After change in crud (add repr())
{
  "email": "r5",
  "p": "555"
  "id": 4,
  "is_active": true,
  "items": []
}    """

    user_name = credentials.username
    password = credentials.password
    user = crud.get_user_by_email(db, user_name)

    hashed_password = 'not initialized'
    user_hashed_password_bytes = 'not initialized'

    if user:
        correct_user_name = user_name
        logger.info(f"user.salt:{user.salt}\ntype(user.salt):{type(user.salt)}")
        salt = bytes.fromhex(user.salt)
        password = password.encode('utf-8')
        # logger.info(f"password, type(password): {password}, {type(password)}")
        # user_hashed_password_bytes = user.hashed_password.encode('utf-8')
        user_hashed_password_bytes = bytes.fromhex(user.hashed_password)
        hashed_password = hashlib.pbkdf2_hmac('sha256', password, salt, 10000)

        if user_hashed_password_bytes == hashed_password:
            correct_password = password
        else:
            correct_password = b"None"
    else:
        correct_user_name = "None"
        correct_password = b"None"
    is_correct_username = secrets.compare_digest(user_name, correct_user_name)
    logger.info(f"is_correct_username:{is_correct_username}\n"
                f"correct_password:{correct_password}\n"
                f"correct_user_name:{correct_user_name}\n"
                f"password:{password}\nhashed_password:{hashed_password}\n"
                f"user.hashed_password:{user.hashed_password}\n"
                f"user_hashed_password_bytes:{user_hashed_password_bytes}")
    is_correct_password = secrets.compare_digest(password, correct_password)

    logger.info(f"is_correct_password:{is_correct_password}")
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return user_name


@app.get("/users/me")
def read_current_user(username: str = Depends(get_current_username)):
    return {"username": username}


@app.get("/timeseries/{start_date}/{end_date}")
async def time(start_date_year: Year, start_date_month: Month, start_date_day: Day,
               end_date_year: Year, end_date_month: Month, end_date_day: Day,
               username=Depends(get_current_username), db: Session = Depends(get_db)):
    start_date, end_date = translate_date(start_date_day, start_date_month, start_date_year,
                                          end_date_day, end_date_month, end_date_year)
    user_id = crud.get_current_user_id(db, username)
    crud.create_user_timeseries(db=db, user_id=user_id, timeseries=start_date + 'to' + end_date)
    return 'Timeseries are setting'



@app.get("/sev_currencies/{first_cur}")
async def main(first_cur: CurrencyName, second_cur: CurrencyName = None,
               third_cur: CurrencyName = None, four_cur: CurrencyName = None,
               username=Depends(get_current_username), db: Session = Depends(get_db)):
    used_currencies = [currency for currency in [first_cur, second_cur, third_cur, four_cur] if currency is not None]
    user_id = crud.get_current_user_id(db, username)
    crud.get_last_timeseries(db, user_id)

    date = crud.get_last_timeseries(db, user_id)
    start_date, end_date = date[0].split('to')
    take_percent_change_sev_cur(used_currencies, start_date, end_date)
    return FileResponse("percent_changes.png")

