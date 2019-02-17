'''
Classes and data for random password generation according to the information
provided by user
'''
import string, random

#defaults
DEFAULT_PASSWORD_LENGTH = 8
#number of passwords generated to the user for choice
DEFAULT_PASSWORD_RANGE = 10
LOOK_LIKE_SYMBOLS = 'l1O0|'


class PasswordGeneratorException(Exception):
    '''Base class for all password generator exceptions'''
    def __init__(self, value, message):
        self.value = value
        self.message = message
    def __str__(self):
        return repr(' {}, {}'.format(self.value, self.message)) 


class FewSymbolsProvidedException(PasswordGeneratorException):
    '''Raised if the user doesn't provided enough symbols for password generation'''
    def __init__(self, value, message):
        self.value = value
        self.message = message
    
class ZeroPasswordException(PasswordGeneratorException):
    '''Raised if the user doesn't provided enough length for password generation'''
    def __init__(self, value, message):
        self.value = value
        self.message = message
        
class InvalidSymbolsException(PasswordGeneratorException):
    '''Raised if the user provided invalid symbol(not printable ascii ) '''
    def __init__(self, value, message):
        self.value = value
        self.message = message
        
        


class PasswordSpecification(object):
    """DTO for froviding data to PasswordGenerator"""
    
    def __init__(self):
        self.__passwordLength = DEFAULT_PASSWORD_LENGTH
        self.__additionalSymbols = ''
        self.__excludedSymbols = ''
        self.__excludeLookLikeSymbols = False
        self.__lowerCase = False
        self.__upperCase = False
        self.__digit = False
        self.__minus = False
        self.__underline = False
        self.__space = False
        self.__dot = False
        self.__eachCaracterAtMostOne = False
    
    @property
    def passwordLength(self):
        return self.__passwordLength
    
    def setPasswordLength(self, value):
        """
        Set length for password
        @type value: integer
        """
        self.__passwordLength = int(value)
        
    @property
    def additionalSymbols(self):
        return self.__additionalSymbols
    
    def setAdditionalSymbols(self, value):
        """
        Add given symbols to password
        @type value: string
        """
        self.__additionalSymbols = value
        
    @property
    def excludedSymbols(self):
        return self.__excludedSymbols
    
    def setExcludedSymbols(self, value):
        """
        Exclude given symbols from password
        @type value: string
        """
        self.__excludedSymbols = value   
        
    @property
    def lowerCase(self):
        return self.__lowerCase
    
    def setLowerCase(self, value):
        """
        Lowercase symbol in password
        @type value: boolean
        """
        self.__lowerCase = value
        
    @property
    def upperCase(self):
        return self.__upperCase
    
    def setUpperCase(self, value):
        """
        Uppercase symbol in password
        @type value: boolean
        """
        self.__upperCase = value
        
    @property
    def digit(self):
        return self.__digit
    
    def setDigit(self, value):
        """
        Digit symbols (0-9) in password
        @type value: boolean
        """
        self.__digit = value
        
    @property
    def minus(self):
        return self.__minus
    
    def setMinus(self, value):
        """
        Minus symbol in password
        @type value: boolean
        """
        self.__minus = value
        
    @property
    def underline(self):
        return self.__underline
    
    def setUnderline(self, value):
        """
        Underline symbol in password
        @type value: boolean
        """
        self.__underline = value
        
    @property
    def space(self):
        return self.__space
    
    def setSpace(self, value):
        """
        Space symbol in password
        @type value: boolean
        """
        self.__space = value 
        
    @property
    def dot(self):
        return self.__dot
    
    def setDot(self, value):
        """
        Dot symbol in password
        @type value: boolean
        """
        self.__dot = value
        
    @property
    def excludeLookLikeSymbols(self):
        return self.__excludeLookLikeSymbols
    
    def setExcludeLookLikeSymbols(self, value):
        """
        Exclude symbols like l1, O0.. from password
        @type value: bool
        """
        self.__excludeLookLikeSymbols = value
        
    @property
    def eachCaracterAtMostOne(self):
        return self.__eachCaracterAtMostOne
    
    def setEachCaracterAtMostOne(self, value):
        """
        Each symbol doesn't repet in password
        @type value: bool
        """
        self.__eachCaracterAtMostOne = value                              
    
    

class PasswordGenerator:
    """Class for generation random password"""
    def __init__(self):
        #store entropy values taken from user actions, for example mouse movement, to 
        #increase the randomness by password generation
        self.__entropyValues = []
        
    def generatePassword(self, passwordSpecification):
        """
        Generate password according to provided requirements
        @type number: integer
        @param number: number of passwords to generate
        @type passwordSpecification: PasswordSpecification
        @param passwordSpecification: DTO object to pass conditions for password generation   
        @raise FewSymbolsProvidedException: if 0 symbols provided of their number isn't enough for 
                                            password generation (inclusion of each symbol only once)
        @return password(string)
        """
        #generate string of all possible symbols for the password
        genSymbols = ""
        if passwordSpecification.lowerCase:
            genSymbols += string.ascii_lowercase
        if passwordSpecification.upperCase:
            genSymbols += string.ascii_uppercase 
        if passwordSpecification.digit:
            genSymbols += string.digits
        if passwordSpecification.minus:
            genSymbols += '-'
        if passwordSpecification.underline:
            genSymbols += '_'
        if passwordSpecification.space:
            genSymbols += ' '
        if passwordSpecification.dot:
            genSymbols += '.'
        #add additional symbols if there are any
        for s in passwordSpecification.additionalSymbols:
            if s not in genSymbols:
                genSymbols += s
        #genSymbols += passwordSpecification.additionalSymbols
        
        self.__symbolList = list(genSymbols)
        #exclude excluded symbols
        for c in passwordSpecification.excludedSymbols:
            if c in self.__symbolList:
                self.__symbolList.remove(c)
        #exclude look like symbols if enabled
        if passwordSpecification.excludeLookLikeSymbols:
            for c in LOOK_LIKE_SYMBOLS:
                if c in self.__symbolList:
                    self.__symbolList.remove(c)                        
        
        #check if the password specification isn't contradictory
        self.__dataCheck(self.__symbolList, passwordSpecification)
        
        #shuffle the symbols   
        random.shuffle(self.__symbolList)
        
        #apply entropy
        for value in self.__entropyValues:
            print "Shuffle", value
            random.shuffle(self.__symbolList, lambda : value)
        self.__entropyValues = []
        
        #generate password from prepared symbol sequence
        passWord = ""
        for counter in range(0, passwordSpecification.passwordLength):
            symbol = random.choice(self.__symbolList)
            passWord += symbol
            if passwordSpecification.eachCaracterAtMostOne:
                self.__symbolList.remove(symbol)

        return passWord
    
    def generatePasswordRange(self, passwordSpecification, number=DEFAULT_PASSWORD_RANGE):
        """
        Generate sequence of passwords for user's choice
        @type number: integer
        @param number: number of passwords to generate
        @type passwordSpecification: PasswordSpecification
        @param passwordSpecification: DTO object to pass conditions for password generation   
        @raise FewSymbolsProvidedException: if 0 symbols provided of their number isn't enough for 
                                            password generation (inclusion of each symbol only once)
        @return list of passwords(string)
        """
        res = []
        for n in range(0, number):
            password = self.generatePassword(passwordSpecification)
            res.append(password)
            random.shuffle(self.__symbolList)
        return res
    
    
    def addEntropy(self, x, y):
        """For more randomness in password generation use the method. It's called before password generation"""
        x = float(abs(x))
        y = float(abs(y))
        random_entropy_value = 0.5
        if x > 0 and y > 0:
            #should be in 0-1 range
            random_entropy_value = y / x if y <= x else x / y 
        print "Adder Entropy" , random_entropy_value
        self.__entropyValues.append(random_entropy_value)
        
    
    def clearEntropy(self):
        """Remove collected entropy"""
        self.__entropyValues = []
        
        
    def __dataCheck(self, genSymbols, passwordSpecification):
        """Check whether data provided by user isn't contradictory"""
        if passwordSpecification.passwordLength == 0:
            raise ZeroPasswordException('0', "Can't generate empty password")
        
        if len(genSymbols) == 0:
            raise FewSymbolsProvidedException('0', 'No symbols provided for password generation')
        
        if (passwordSpecification.eachCaracterAtMostOne) and (passwordSpecification.passwordLength > len(genSymbols)):
            raise FewSymbolsProvidedException('{}'.format(len(genSymbols)),
                                               """Not enough symbols provided for password generation with inclusion of each symbol only once""") 
        for c in genSymbols:
            if c not in string.printable:
                raise InvalidSymbolsException(c, 'Invalid symbol. Should be only printable ascii')
                            
        
        
if __name__ == "__main__":
    gen = PasswordGenerator()
    data = PasswordSpecification()
    data.setPasswordLength(20)
    data.setLowerCase(True)
    data.setUpperCase(True)
    data.setDigit(True)
    data.setExcludedSymbols('2345678')
    data.setEachCaracterAtMostOne(True)
    data.setExcludeLookLikeSymbols(True)
    data.setDot(True)
    gen.addEntropy(54, 104)
    d = gen.generatePasswordRange(data, 10)
    for a in d:
        print a