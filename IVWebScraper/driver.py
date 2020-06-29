import requests


class parser:
    def getIVMean(self):

        URL = 'https://www.ivolatility.com/options.j?ticker='+self+'&R=1'

        response = requests.get(URL)

        source = response.text

        begin = source.index('IV&nbsp;Index mean&nbsp')

        end = source.index('%', begin+190)

        IVMean = float(source[begin+190:end])

        return IVMean




print("Enter Ticker")
choice = input().upper()
print("The IV for "+choice+" is "+str(parser.getIVMean(choice))+"%")