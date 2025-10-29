from typing import Optional
from sqlalchemy.orm import Session
from core.user.exception import CurrentPasswordException, DuplicatedEmailException, DuplicatedPhoneNumberException, DuplicatedUsernameException, UserNotFoundException
from core.user.model import User
from core.user.schema import CreateUserSchema, UpdateUserSchema
from utils.jwt import get_password_hash, verify_password


class RepositoryUser():

    def get_by_id(self, db: Session, *, id: int) -> User:
        return db.query(User).filter(User.id == id).first()

    def get_by_id_class(self, db: Session, *, id: int) -> User:
        return db.query(User).filter(User.id == id) # type: ignore
    
    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()
    
    def get_by_username(self, db: Session, *, username: str) -> Optional[User]:
        return db.query(User).filter(User.username == username).first()

    def get_by_phone_number(self, db: Session, *, phone_number: str) -> User:
        return db.query(User).filter(User.phone_number == phone_number).count()
        
    def create(self, db: Session, *, obj_in: CreateUserSchema) -> User:
        email = self.get_by_email(db, email=obj_in.email)
        username = self.get_by_username(db, username=obj_in.username)
        phone = self.get_by_phone_number(db, phone_number=obj_in.phone_number)

        if email:
            raise DuplicatedEmailException
        elif username:
            raise DuplicatedUsernameException        
        elif phone:
            raise DuplicatedPhoneNumberException
        
        obj_in.password = get_password_hash(obj_in.password)
        db_obj = User(**obj_in.dict())

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def authenticate(self, db: Session, *, email: str, password: str):
        user = self.get_by_email(db, email=email)
        if not user:
            raise UserNotFoundException
        if not verify_password(password, user.password):
            raise CurrentPasswordException
        return user
    
    def update(self, db: Session, id, *, obj_in: UpdateUserSchema) -> User:
        obj_user = self.get_by_id_class(db, id=id)
        user = self.get_by_id(db, id=id)
        phone_number = self.get_by_phone_number(db, phone_number=obj_in.phone_number) # type: ignore

        if not user:
            raise UserNotFoundException
        elif user.phone_number != obj_in.phone_number: # type: ignore
            if phone_number > 1:
                raise DuplicatedPhoneNumberException

        obj_user.update(obj_in.dict(exclude_unset=True), synchronize_session=False)
        db.commit()
        return obj_user.first()
        db.refresh(user)


repository_user = RepositoryUser()
