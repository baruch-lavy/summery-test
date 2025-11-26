from fastapi import  FastAPI,HTTPException,Depends,middleware,UploadFile,Request,Response,File
from sqlalchemy.orm import Session
from sqlalchemy import desc
from database import Session_local,engine,Base,Soldier,Dorm
from model import SoldierCreate,SoldierResponse,SoldierToassign
from contextlib import asynccontextmanager
import csv
import io
import time

def get_db():
    db = Session_local()
    try:
        yield db
    finally:
        db.close()

def init_db():
    Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app:FastAPI):
    init_db()
    yield
    engine.dispose()
   
app = FastAPI(title='Soldiers API (SQLAlchemy)',lifespan=lifespan)
       
@app.middleware('http')
async def print_middleware(request:Request,call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers['X-process-time'] = str(process_time)
    return response
        
# @app.post('/Soldiers/',response_model=SoldierResponse)
# def create_Soldier(Soldier:SoldierCreate,db:Session = Depends(get_db)):
#     db_Soldier = db.query(Soldier).filter(Soldier.email == Soldier.email).first()
#     if db_Soldier:
#         raise HTTPException(status_code=400,detail='email already registered')
#     new_Soldier = Soldier(
#         name=Soldier.name,
#         email=Soldier.email,
#         age=Soldier.age
#         )
#     db.add(new_Soldier)
#     db.commit()
#     db.refresh(new_Soldier)
#     return new_Soldier

@app.post('/soldiers/upload-csv',description='create table from .csv file')
async def upload_csv(file:UploadFile = File(...),db:Session = Depends(get_db)):
    db_users = db.query(Dorm).all()
    
    for user in db_users:
        db.delete(user)
    db.commit()
    
    db_users = db.query(Soldier).all()
    
    for user in db_users:
        db.delete(user)
    db.commit()
    
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400,detail='file must be csv file')
    content = await file.read()
    imported_count = 0
    try:
        csv_text = content.decode('utf-8')
        csv_reader = csv.DictReader(io.StringIO(csv_text))
        
        for row in csv_reader:
            privet_number = row.get('privet_number')
            first_name = row.get('first_name')
            last_name = row.get('last_name')
            gender = row.get('sex')
            city = row.get('city')
            distance = row.get('distance')
            is_assign = False
            
            soldier = Soldier(
                privet_number=privet_number, 
                first_name=first_name,
                last_name=last_name,
                gender=gender,
                city=city,
                distance=distance,
                is_assign=is_assign
                
            )
        
            db.add(soldier)
            imported_count += 1
        db.commit() 
            
        sorted_soldiers = db.query(Soldier).order_by(desc('distance')).all()
        db.query(Dorm).all()
        soldiers_assigned = 0
        for i in range(0,160,8):
            if i < 80:
                dormid = 1
            else:
                dormid = 2
            soldiers = Dorm( 
                dormid = dormid,
                soldier_1=sorted_soldiers[i].privet_number,
                soldier_2=sorted_soldiers[i+1].privet_number,
                soldier_3=sorted_soldiers[i+2].privet_number,
                soldier_4=sorted_soldiers[i+3].privet_number,
                soldier_5=sorted_soldiers[i+4].privet_number,
                soldier_6=sorted_soldiers[i+5].privet_number,
                soldier_7=sorted_soldiers[i+6].privet_number,
                soldier_8=sorted_soldiers[i+7].privet_number
                )
            db.add(soldiers)
            db.commit()
            soldiers_assigned += 8
        
        assigned_doldiers = db.query(Dorm).all()
        for soldier in assigned_doldiers:
            db_soldiers = db.query(Soldier).filter(Soldier.privet_number.in_((soldier.soldier_1,soldier.soldier_2,soldier.soldier_3,soldier.soldier_4,soldier.soldier_5,soldier.soldier_6,soldier.soldier_7,soldier.soldier_8))).all()
            
            if db_soldiers:
                for db_soldier in db_soldiers:
                    db_soldier.is_assign = True
                    db.add(db_soldier)
                    db.commit()
        
        information = {}
        updated_soldiers = db.query(Soldier).all()
        for soldier in updated_soldiers:
            if soldier.is_assign:
                dorms = db.query(Dorm).all()
                for dorm in dorms:
                    if soldier.privet_number == dorm.soldier_1 or soldier.privet_number == dorm.soldier_2 or soldier.privet_number == dorm.soldier_3 or soldier.privet_number == dorm.soldier_4 or soldier.privet_number == dorm.soldier_5 or soldier.privet_number == dorm.soldier_6 or soldier.privet_number == dorm.soldier_7 or soldier.privet_number == dorm.soldier_8:
                
                        information[soldier.privet_number] = {"dorm":dorm.dormid,"room":dorm.id}
            else:
                information[soldier.privet_number] = "in waiting list"
        
        return {
                "message": f"Successfully imported {imported_count} Soldiers from CSV",
                "imported_count": imported_count,
                "soldiers assigned":soldiers_assigned,
                "soldiers in waiting list": len(sorted_soldiers) - soldiers_assigned,
                "information":information 
            }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400,detail=e) 
    
@app.get('/soldiers/',response_model=list[SoldierResponse])
def get_Soldiers(db:Session = Depends(get_db)):
    return db.query(Soldier).all() 

@app.delete('/soldiers/')
def delete_soldiers(db:Session = Depends(get_db)):
    db_users = db.query(Soldier).all()
    
    for user in db_users:
        db.delete(user)
    db.commit()
    
@app.delete('/dorms/')
def delete_dorms(db:Session = Depends(get_db)):
    db_users = db.query(Dorm).all()
    
    for user in db_users:
        db.delete(user)
    db.commit()

@app.get('/space')
def return_place(db:Session = Depends(get_db)):
    rooms = db.query(Dorm).all()
    filled_rooms = 0
    empty_rooms = 0
    semi_filed_rooms = 0
    for room in rooms:
        if room.soldier_1 == 'null' and room.soldier_2 == 'null' and room.soldier_3 == 'null' and room.soldier_4 == 'null' and room.soldier_5 == 'null' and room.soldier_6 == 'null' and room.soldier_7 == 'null' and room.soldier_8 == 'null':
            empty_rooms += 1
        elif room.soldier_1 == 'null' or room.soldier_2 == 'null' or room.soldier_3 == 'null' or room.soldier_4 == 'null' or room.soldier_5 == 'null' or room.soldier_6 == 'null' or room.soldier_7 == 'null' or room.soldier_8 == 'null':
            semi_filed_rooms += 1
        else:
            filled_rooms += 1
    
    return {
        "filled rooms":filled_rooms,
        "empty rooms":empty_rooms,
        "semi filled rooms":semi_filed_rooms
    }
    
@app.get('/waitingList')
def return_place(db:Session = Depends(get_db)):
    soldiers = db.query(Soldier).filter(Soldier.is_assign == False).order_by(desc(Soldier.distance)).all()
    
    return {"waiting list":soldiers}

@app.get('/search{soldier_id}')
def search_soldier(soldier_id:int,db:Session = Depends(get_db)):
    db_soldier = db.query(Soldier).filter(Soldier.privet_number == soldier_id).first()
    if not db_soldier:
        raise HTTPException(status_code=404,detail='soldier not found')
    information_to_return = {}
    if db_soldier.is_assign == True:
        dorms = db.query(Dorm).all()
        for dorm in dorms:
            if soldier_id == dorm.soldier_1 or soldier_id == dorm.soldier_2 or soldier_id == dorm.soldier_3 or soldier_id == dorm.soldier_4 or soldier_id == dorm.soldier_5 or soldier_id == dorm.soldier_6 or soldier_id == dorm.soldier_7 or soldier_id == dorm.soldier_8:
                information_to_return[soldier_id] = {"dorm":dorm.dormid,"room":dorm.id}
    else:
        information_to_return[soldier_id] = "in waiting list"
    return {"information":information_to_return}

@app.post('/release{soldier_id}')
def release_soldier(soldier_id,db:Session = Depends(get_db)):
    pass