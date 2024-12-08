from passlib.context import CryptContext

pwd_ctx= CryptContext(schemes=["bcrypt"], deprecated="auto")
class Hash():
    @staticmethod
    def bcrypt(password:str):
         return pwd_ctx.hash(password)
    
    @staticmethod
    def verify(real_password, plain_password):
        return pwd_ctx.verify(plain_password, real_password )