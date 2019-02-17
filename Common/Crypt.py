'''

@author: Vova
'''

from Crypto.Cipher import AES
import hashlib
import UsConfig as Config

# Basic class for Encription/ Decription



class Crypt():
    def __init__(self, password=""):
        self.__password = password
        
    def sipher(self, message):
        print "Cipher"
    
    def decipher(self, message):
        print "Decipher"
        
    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, value):
        self.__password = value    

 

class CryptAES(Crypt): 
    def __init__(self):
        Crypt.__init__(self)
        self.__VI = 'This is an IV456'
        
    def cipher(self, message, password):
        if not Config.CRYPTO_ENABLE:
            return message
        message = self.__fitMessageToBase(message)
        password = self.__fitPasswordToBase(password)
              
        obj = AES.new(password, AES.MODE_CBC, self.__VI)
        return obj.encrypt(message)
    
    def decipher(self, message, password):
        if not Config.CRYPTO_ENABLE:
            return message
        password = self.__fitPasswordToBase(password) 
           
        obj = AES.new(password, AES.MODE_CBC, self.__VI)
        return  obj.decrypt(message).rstrip()
    
    def hashSHA1(self, message):
        return hashlib.sha1(message).hexdigest()
    
    
    def __fitMessageToBase(self, message):
        #fill the message with spaces to fit it to crypt base (16, 32...)
        spaces = Config.AES_CRYPTO_BASE - (len(message) % Config.AES_CRYPTO_BASE)
        message += " "*spaces
        return message
    
    def __fitPasswordToBase(self, password):
        #fit the password to crypt base - count hash sha1 and take first symbols
        hash = hashlib.sha1(password).hexdigest()
        password = hash[0:Config.AES_CRYPTO_BASE]  
        return password                
    
c = CryptAES()
cipher = c.cipher("That is a password for database ", "password")
print cipher, "SIPHER" 

decipher = c.decipher(cipher, "password")  
print decipher

d = c.hashSHA1("25387623784623 ksjdhfskjdhf")
print d

