from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.models import WorkShop
from app.models.auth import Tokens
from app.schemas.auth.token import CreateToken, RemoveToken, ResponseCreateToken, ResponseRemoveToken



class TokenRepository:
    def __init__(self, db: Session):
        self.db = db


    def create_token(self, token: CreateToken)->ResponseCreateToken:
        db_tokens = self.db.query(Tokens).filter(Tokens.work_shop_username == token.work_shop_username).all()
        if db_tokens:
            return ResponseCreateToken(work_shop_username=False)
        db_token = Tokens(
          access_token=token.access_token,
          refresh_token=token.refresh_token,
          work_shop_username=token.work_shop_username,
            )
        self.db.add(db_token)
        self.db.commit()
        self.db.refresh(db_token)


        return ResponseCreateToken(work_shop_username=token.work_shop_username)
    def get_tokens(self, username:  str, password: str)->ResponseCreateToken:
        db_work_shop = self.db.query(WorkShop).filter(WorkShop.username == username).first()
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        verification_password = pwd_context.verify(password, db_work_shop.hash_password)
        db_tokens= self.db.query(WorkShop).filter(WorkShop.username==username & verification_password).all()
        if not db_tokens:
            return ResponseCreateToken(work_shop_username='')
        else:
            db_tokens = self.db.query(Tokens).filter(Tokens.work_shop_username == username).first()
            return db_tokens

    def remove_token(self, id: RemoveToken)->ResponseRemoveToken:
        with self.db.begin():
            db_tokens = self.db.query(Tokens).filter(Tokens.work_shop_id == id.work_shop_id).all()
            for db_token in db_tokens:
                self.db.delete(db_token)
        return ResponseRemoveToken(work_shop_id=id.work_shop_id)