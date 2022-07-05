from fastapi.responses import FileResponse
import secrets
from enum import Enum
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from returngraph import take_percent_change_sev_cur
from timeseries_rates import set_timeseries, translate_date


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


@app.get("/timeseries/{start_date}/{end_date}")
async def time(start_date_year: Year, start_date_month: Month, start_date_day: Day,
               end_date_year: Year, end_date_month: Month, end_date_day: Day,
               username=Depends(get_current_username)):
    start_date, end_date = translate_date(start_date_day, start_date_month, start_date_year,
                                          end_date_day, end_date_month, end_date_year)
    set_timeseries(start_date, end_date)
    return 'Timeseries are setting'


@app.get("/sev_currencies/{first_cur}")
async def main(first_cur: CurrencyName, second_cur: CurrencyName = None,
               third_cur: CurrencyName = None, four_cur: CurrencyName = None,
               username=Depends(get_current_username)):
    used_currencies = [currency for currency in [first_cur, second_cur, third_cur, four_cur] if currency is not None]

    take_percent_change_sev_cur(used_currencies)
    return FileResponse("percent_changes.png")
