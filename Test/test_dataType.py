import unittest
from MIND2.dataType import DataType
from MIND2.dataNode import DataNode
from MIND2.graphNode import GraphNode


class Test_DataNode(unittest.TestCase):

    def setUp(self):
        def letterMatch(test):
            returnVal = False
            if type(test) is str and test in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']:
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

        def wordMatch(test):
            if not len(test) == len(self.parsedData):
                return False
            for i in range(0, len(test)):
                if not test[i].matches(self.parsedData[i]):
                    return False
            return True

        self.letterDataType = DataType("letter", letterMatch)
        self.numberDataType = DataType("number", numberMatch)
        self.whiteSpaceDataType = DataType("whiteSpace", whiteSpaceMatch)
        self.punctuationDataType = DataType("punctuation", punctuationMatch)
        self.wordDataType = DataType("word", wordMatch)

    def test_letter_matches(self):
        DataType1 = DataType("char", lambda i: i == 'a')
        DataNode1 = DataNode(DataType1, parsedData='a')
        DataType2 = DataType("char", lambda i: i == 'A')
        DataNode2 = DataNode(DataType2, parsedData='A')
        DataType3 = DataType("char", lambda i: i == ' ')
        DataNode3 = DataNode(DataType3, parsedData=' ')
        DataType4 = DataType("char", lambda i: i == '1')
        DataNode4 = DataNode(DataType4, parsedData='1')
        self.assertTrue(self.letterDataType.matches(DataNode1.parsedData))
        self.assertTrue(self.letterDataType.matches(DataNode2.parsedData))
        self.assertFalse(self.letterDataType.matches(DataNode3.parsedData))
        self.assertFalse(self.letterDataType.matches(DataNode4.parsedData))

    def test_number_matches(self):
        DataType1 = DataType("char", lambda i: i == 'a')
        DataNode1 = DataNode(DataType1, parsedData='a')
        DataType2 = DataType("char", lambda i: i == 'A')
        DataNode2 = DataNode(DataType2, parsedData='A')
        DataType3 = DataType("char", lambda i: i == ' ')
        DataNode3 = DataNode(DataType3, parsedData=' ')
        DataType4 = DataType("char", lambda i: i == '1')
        DataNode4 = DataNode(DataType4, parsedData='1')
        self.assertFalse(self.numberDataType.matches(DataNode1.parsedData))
        self.assertFalse(self.numberDataType.matches(DataNode2.parsedData))
        self.assertFalse(self.numberDataType.matches(DataNode3.parsedData))
        self.assertTrue(self.numberDataType.matches(DataNode4.parsedData))

    def test_whiteSpace_matches(self):
        DataType1 = DataType("char", lambda i: i == 'a')
        DataNode1 = DataNode(DataType1, parsedData='a')
        DataType2 = DataType("char", lambda i: i == 'A')
        DataNode2 = DataNode(DataType2, parsedData='A')
        DataType3 = DataType("char", lambda i: i == ' ')
        DataNode3 = DataNode(DataType3, parsedData=' ')
        DataType4 = DataType("char", lambda i: i == '1')
        DataNode4 = DataNode(DataType4, parsedData='1')
        self.assertFalse(self.whiteSpaceDataType.matches(DataNode1.parsedData))
        self.assertFalse(self.whiteSpaceDataType.matches(DataNode2.parsedData))
        self.assertTrue(self.whiteSpaceDataType.matches(DataNode3.parsedData))
        self.assertFalse(self.whiteSpaceDataType.matches(DataNode4.parsedData))

    def test_punctuation_matches(self):
        DataType1 = DataType("char", lambda i: i == 'a')
        DataNode1 = DataNode(DataType1, parsedData='a')
        DataType2 = DataType("char", lambda i: i == ' ')
        DataNode2 = DataNode(DataType2, parsedData=' ')
        DataType3 = DataType("char", lambda i: i == ',')
        DataNode3 = DataNode(DataType3, parsedData=',')
        DataType4 = DataType("char", lambda i: i == '?')
        DataNode4 = DataNode(DataType4, parsedData='?')
        self.assertFalse(self.punctuationDataType.matches(DataNode1.parsedData))
        self.assertFalse(self.punctuationDataType.matches(DataNode2.parsedData))
        self.assertTrue(self.punctuationDataType.matches(DataNode3.parsedData))
        self.assertTrue(self.punctuationDataType.matches(DataNode4.parsedData))

if __name__ == '__main__':
    unittest.main()
