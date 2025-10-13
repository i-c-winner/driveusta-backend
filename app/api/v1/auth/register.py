from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Annotated
from starlette import status
from app.services.security.auth.token import create_tokens, create_hash_password

from app.db.dependencies import get_db
from app.models import WorkShop
from app.models.auth import Tokens
from app.schemas.auth import ResponseCreateToken

router = APIRouter(
    prefix="/register",
    tags=["register"]
)


@router.post(path="/", response_model=ResponseCreateToken)
async def create_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    work_shop = db.query(WorkShop).filter(
        WorkShop.username == form_data.username,
    ).first()
    print(work_shop)
    if work_shop:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Такой пользователь существует"
        )
    else:
      result=   create_tokens({"work_shop_username": form_data.username})
      print('PSWWORD', form_data.password)
      new_work_shop = WorkShop(
          username=form_data.username,
          hash_password=create_hash_password(form_data.password),
          work_shop_name= '',
          telephone='',
          street_name='',
          address='',
          site='',
          rating= 0.0)
      tokens = Tokens(
          access_token = result["access_token"],
          refresh_token= result["refresh_token"],
          work_shop_username= form_data.username
      )
      db.add(tokens)
      db.add(new_work_shop)
      db.commit()
      db.refresh(new_work_shop)
      print(result)
      return result