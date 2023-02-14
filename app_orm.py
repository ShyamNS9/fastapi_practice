import logging
from fastapi import FastAPI, APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse

from database.database import SessionLocal, engine
from schemas.schemas import UserDetail, UpdateDetail
from models import models

logger = logging.getLogger(__name__)  # the _name__ resolve to "main" since we are at the root of the project.
models.Base.metadata.create_all(bind=engine)
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
        get_database_session()
    except Exception as exc:
        print(str(exc))


@app.get("/")
def docs():
    return RedirectResponse(url="/docs")


@api_router.post("/user")
def create_user(data: UserDetail, db: Session = Depends(get_database_session)) -> dict:
    try:
        logger.info("logging from the create_user logger")
        add_user = models.CreateUserDetails(firstname=data.firstname, lastname=data.lastname, phone_no=data.phone_no,
                                            email=data.email, dob=data.dob, address=data.address)
        logger.info(f"adding user with details: {add_user}")
        db.add(add_user)
        db.commit()
        db.refresh(add_user)
        return {
            "status": 200,
            "message": "User created successfully",
            "payload": add_user
        }
    except Exception as e:
        logger.error(f"logging from the create_user error logger with error: {e}")
        return {
            "status": 500,
            "message": "something went wrong.",
            "Details": e.args
        }


@api_router.put("/user/{user_id}")
def update_user(user_id: int, data: UpdateDetail, db: Session = Depends(get_database_session)) -> dict:
    try:
        logger.info("logging from the update_user logger")
        db_check = db.get(models.CreateUserDetails, user_id)
        print(db_check)
        logger.info(f"data fetched with details: {db_check}")
        if db_check:
            details = data.dict(exclude_unset=True)
            for key, value in details.items():
                setattr(db_check, key, value)
            logger.info(f"updating user with details: {db_check}")
            db.add(db_check)
            db.commit()
            db.refresh(db_check)
            return {
                "status": 200,
                "message": "User updated successfully",
                "payload": db_check
            }
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        logger.error(f"logging from the update_user error logger with error: {e}")
        return {
            "status": 500,
            "message": "something went wrong.",
            "Details": e
        }


@api_router.get("/user")
def fetch_user(db: Session = Depends(get_database_session)):
    try:
        logger.info("logging from the fetch_user logger")
        datas = db.query(models.CreateUserDetails).all()
        return {
            "status": 200,
            "message": "Data fetched successfully",
            "payload": datas
        }
    except Exception as e:
        logger.error(f"logging from the fetch_user error logger with error: {e}")
        return {
            "status": 500,
            "message": "something went wrong.",
            "Details": e.args
        }


@api_router.get("/user/{user_id}")
def fetch_user_by_id(user_id: int, db: Session = Depends(get_database_session)):
    try:
        logger.info("logging from the fetch_user_by_id logger")
        db_check = db.get(models.CreateUserDetails, user_id)
        if not db_check:
            raise HTTPException(status_code=404, detail="User not found")
        datas = db.query(models.CreateUserDetails).filter(models.CreateUserDetails.id == user_id).first()
        return {
            "status": 200,
            "message": "Data Fetched Successfully",
            "payload": datas
        }
    except Exception as e:
        logger.error(f"logging from the fetch_user_by_id error logger with error: {e}")
        return {
            "message": "something went wrong.",
            "Details": e
        }


@api_router.delete("/user/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_database_session)):
    try:
        logger.info("logging from the delete_user logger")
        db_check = db.get(models.CreateUserDetails, user_id)
        if not db_check:
            raise HTTPException(status_code=404, detail="User not found")
        datas = db.query(models.CreateUserDetails).filter(models.CreateUserDetails.id == user_id).first()
        db.delete(datas)
        db.commit()
        return {
            "status": 200,
            "message": f"User With {user_id} Deleted Successfully"
        }
    except Exception as e:
        logger.error(f"logging from the delete_user error logger with error: {e}")
        return {
            "message": "something went wrong.",
            "Details": e
        }


app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, log_level="debug")
