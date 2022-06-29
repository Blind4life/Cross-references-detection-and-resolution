from operator import le


def is_number(alphaNum): # A method to identify numbers
    if len(alphaNum)== 0:
        return False
    
    try:        
        if int(alphaNum) >= 0 and int(alphaNum) <= 9:
            return True
    except ValueError:
        pass
    
    try:
        import unicodedata
        if unicodedata.numeric(alphaNum) >=0 and unicodedata.numeric(alphaNum) <=9: 
            return True
    except (TypeError, ValueError):
        pass
    
    return False