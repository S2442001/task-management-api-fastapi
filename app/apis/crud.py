from fastapi import APIRouter, Depends, HTTPException 
from sqlalchemy.ext.asyncio import AsyncSession 
from app.models.user import User 
from app.models.tasks import Task 
from app.core.security import decode_token, get_current_user, verify 
from app.db.database import get_db 
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.schemas.requests import TasksIn, UpdateIn
from sqlalchemy import select 

router=APIRouter(prefix="/crud", tags=["crud"])


@router.post("/create")
async def create_tasks(tasks_data:TasksIn,db:AsyncSession=Depends(get_db),user:User=Depends(get_current_user)):
    title=tasks_data.title
    description=tasks_data.description 
    status=tasks_data.status

    result=Task(title=title, description=description, status=status, owner_id=user.id)
    db.add(result)
    await db.commit()
    await db.refresh(result)

    return {
        "message": "Task created successfully",
        "task_id": result.id
    }

@router.get("/fetch")
async def fetch_tasks(db:AsyncSession=Depends(get_db), user:User=Depends(get_current_user)):
 
    res=await db.execute(select(Task).where(Task.owner_id==user.id))
    result=res.scalars().all()

    if not result:
        return {"message": "No tasks for Current User found in DB"}
    
    return {
        "Message":"Tasks found for current User.",
        "Tasks": result
    }

    

@router.get("/fetch/{task_id}")
async def get_tasks_by_id(task_id,db:AsyncSession=Depends(get_db), user:User=Depends(get_current_user) ):
    task_result=await db.execute(select(Task).where(Task.owner_id==user.id,Task.id==task_id))
    result=task_result.scalar_one_or_none()

    if not result:
        return {"message": "No tasks found for Given ID"}
    
    return {
        "Message":"Tasks found for current ID.",
        "Tasks": result
    }

@router.put("/update/{task_id}")
async def update_tasks_by_id(task_id,data:UpdateIn, db:AsyncSession=Depends(get_db), user:User=Depends(get_current_user) ):

    task_result=await db.execute(select(Task).where(Task.owner_id==user.id, Task.id==task_id))
    result=task_result.scalar_one_or_none()

    if not result:
        return {"message": "No tasks found  for Given ID"}
    
    description=data.description
    if description is None:
        description=result.description
    result.title=data.title
    result.description=description
    result.status=data.status
    
    await db.commit()
    await db.refresh(result)

    return {
        "Message":"Tasks Updated for given ID.",
        "Updated Task": result
    }

@router.delete("/delete/{task_id}")
async def update_tasks_by_id(task_id,db:AsyncSession=Depends(get_db), user:User=Depends(get_current_user) ):
    task_result=await db.execute(select(Task).where(Task.owner_id==user.id,Task.id==task_id))
    result=task_result.scalar_one_or_none()

    if not result:
        return {"message": "No tasks found  for Given ID"}
    
    await(db.delete(result))
    await db.commit()

    return {
        "Message":"Tasks Deleted for given ID",
        "Task ID": task_id
    }


