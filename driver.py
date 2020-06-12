from parser import *


print("Enter Ticker")
choice = input().upper()
print("The IV for "+choice+" is "+str(parser.getIVMean(choice))+"%")
