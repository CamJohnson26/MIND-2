def letterMatch(test):
    returnVal = False
    if type(test) is str and test.lower() in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']:
        returnVal = True
    return returnVal


def numberMatch(test):
    returnVal = False
    if type(test) is str and test in ['1','2','3','4','5','6','7','8','9','0']:
        returnVal = True
    return returnVal


def whiteSpaceMatch(test):
    returnVal = False
    if type(test) is str and test in ['\t',' ','\n']:
        returnVal = True
    return returnVal


def punctuationMatch(test):
    returnVal = False
    if type(test) is str and test in ['!','@','#','$','%','^','&','*','(',')',',','.','?','\'','\"']:
        returnVal = True
    return returnVal


def charMatch(test):
    if type(test) is str and len(test) == 1:
        return True


def matchFunction(test):
    if not len(test) == len(self.parsedData):
        return False
    for i in range(0, len(test)):
        if not test[i].matches(self.parsedData[i]):
            return False
    return True