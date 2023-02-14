from fastapi import FastAPI, APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse

from database.database import SessionLocal
from schemas.schemas import UserDetail

app = FastAPI(title="User Details", openapi_url="/openapi.json")
api_router = APIRouter()


def get_database_session():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.on_event("startup")
def print_health():
    try:
        print("Checking connection")
        get_database_session()
        print("OK")
    except Exception as exc:
        print(str(exc))


@app.get("/")
def docs():
    return RedirectResponse(url="/docs")


@api_router.post("/user", status_code=200)
def create_user(data: UserDetail, db: Session = Depends(get_database_session)) -> dict:
    try:
        ans = db.execute(f"INSERT INTO user_details (firstname, lastname, phone_no, email, dob, address) VALUES ('{data.firstname}', '{data.lastname}', '{data.phone_no}', '{data.email}', '{data.dob}', '{data.address}');")
        db.commit()
        return {
            "status": 200,
            "message": "User created successfully",
            "payload": ans
        }
    except Exception as e:
        print(e)
        return {
            "status": 500,
            "message": "something went wrong.",
            "Details": e
        }


@api_router.put("/user/{userid}", status_code=200)
def update_user(userid: int, data: UserDetail, db: Session = Depends(get_database_session)) -> dict:
    try:
        db.execute(f'UPDATE user_details SET firstname = "{data.firstname}", lastname = "{data.lastname}", phone_no = "{data.phone_no}", email = "{data.email}", dob = "{data.dob}", address =  "{data.address}" WHERE id = {userid};')
        db.commit()
        return {
            "status": 200,
            "message": "User updated successfully",
            "payload": data
        }
    except Exception as e:
        return {
            "status": 500,
            "message": "something went wrong.",
            "Details": e
        }


@api_router.get("/user", status_code=200)
def fetch_user(db: Session = Depends(get_database_session)) -> dict:
    try:
        datas = db.execute(f'SELECT * FROM user_details').fetchall()
        return {
            "status": 200,
            "message": "Data fetched successfully",
            "payload": datas
        }
    except Exception as e:
        print(e)
        return {
            "status": 500,
            "message": "something went wrong.",
            "Details": e
        }


@api_router.get("/user/{userid}", status_code=200)
def fetch_user_by_id(userid: int, db: Session = Depends(get_database_session)) -> dict:
    try:
        datas = db.execute(f'SELECT * FROM user_details WHERE id="{userid}"').first()
        return {
            "status": 200,
            "message": "Data fetched successfully",
            "payload": datas
        }
    except Exception as e:
        print(e)
        return {
            "status": 500,
            "message": "something went wrong.",
            "Details": e
        }


@api_router.delete("/user/{userid}", status_code=200)
def delete_user_by_id(userid: int, db: Session = Depends(get_database_session)) -> dict:
    try:
        db.execute(f'DELETE FROM user_details WHERE id="{userid}";')
        db.commit()
        return {
            "status": 200,
            "message": f"Data Deleted successfully with id {userid}"
        }
    except Exception as e:
        print(e)
        return {
            "status": 500,
            "message": "something went wrong.",
            "Details": e.args
        }


app.include_router(api_router)
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=5555, log_level="debug")
