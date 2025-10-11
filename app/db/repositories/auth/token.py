from sqlalchemy.orm import Session
from app.models.auth import Token
from app.schemas.auth.token import CreateToken, RemoveToken, ResponseCreateToken, ResponseRemoveToken


class TokenRepository:
    def __init__(self, db: Session):
        self.db = db


    def create_token(self, token: CreateToken)->ResponseCreateToken:
        db_tokens = self.db.query(Token).filter(Token.work_shop_id == token.work_shop_id).all()
        if db_tokens:
            return ResponseCreateToken(work_shop_id=False)
        db_token = Token(
          hash_token=token.hash_token,
          token_type=token.token_type,
          work_shop_id=token.work_shop_id
            )
        self.db.add(db_token)
        self.db.commit()
        self.db.refresh(db_token)


        return ResponseCreateToken(work_shop_id=token.work_shop_id)

    def remove_token(self, id: RemoveToken)->ResponseRemoveToken:
        with self.db.begin():
            db_tokens = self.db.query(Token).filter(Token.work_shop_id == id.work_shop_id).all()
            for db_token in db_tokens:
                self.db.delete(db_token)
        return ResponseRemoveToken(work_shop_id=id.work_shop_id)