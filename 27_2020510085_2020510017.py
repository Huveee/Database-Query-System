# 2020510085 - Kübra Özalp
# 2020510017 - Hüveyda Başyurtlu

import csv
from operator import itemgetter
from tabulate import tabulate
import json

def isKeysValid(inputQuery, keys): #The function to control if the input keys is valid for the file
    
    if(inputQuery[1]=="all" or inputQuery[1] in keys or ',' in inputQuery[1]):
        
        if(',' in inputQuery[1]): #If there are more than one keys     
            headers= inputQuery[1].split(",")
            
            if(len(headers) <= len(keys)): # if the number of input keys are at most 5
                
                for i in range(len(headers)):
                    if(headers[i] not in keys): #If input keys are not valid 
                        return False
                if(not(len(set(headers)) == len(headers))): # if the input keys are unique
                    return False
                
                else:
                    return True
            else:
                return False 
        else:
            return True                       
    else:
        return False


def isQueryValid(string, inputQuery,keys ):# The function to control if the string is convertible to the intege
  
    condOpForString=["=","!="] #The condition operations valid for string keys
    condOp=["=" , "!=" , "<" , ">" , "<=" , ">=" , "!<" , "!>" ] #The condition operations valid for all keys
    stringKeys=["name","lastname","email"] #The string keys
    intKeys=["id","grade"] #The integer keys
    
    if(string=="select" and (len(inputQuery)==11 or len(inputQuery)==15 )): #To control the necessities of the select command
    
        if((inputQuery[2]=="from") and (inputQuery[3]=="students") and (inputQuery[4]=="where") and isKeysValid(inputQuery, keys) 
           and (inputQuery[8]=="or" or inputQuery[8]=="and" or inputQuery[8]=="order") 
           and ( (inputQuery[5] in stringKeys and inputQuery[6] in condOpForString and inputQuery[7].startswith('"') and inputQuery[7].endswith('"') )
               or ((inputQuery[5] in intKeys) and (inputQuery[6] in condOp) and inputQuery[7].isdigit()) ) ):
            
            #If there is an "and" or "or" operator in the input 
            if((inputQuery[8]=="or" or inputQuery[8]=="and") and ( ((inputQuery[9] in stringKeys) and (inputQuery[10] in condOpForString) and inputQuery[11].startswith('"') and inputQuery[11].endswith('"'))
               or ((inputQuery[9] in intKeys) and (inputQuery[10] in condOp) and inputQuery[11].isdigit()) )
               and (inputQuery[12]=="order") and (inputQuery[13]=="by") and (inputQuery[14]=="asc" or inputQuery[14]=="dsc")):                            
                return True
            
             #If there is no "and" or "or" operator in the input                   
            elif((inputQuery[8]=="order") and (inputQuery[9]=="by") and (inputQuery[10]=="asc" or inputQuery[10]=="dsc") ):              
                return True
                
            else: #input must be in one of these formats above
                return False
    
    elif(string=="insert" and len(inputQuery)==4 and inputQuery[1]=="into" and inputQuery[2]=="student" #To control the necessities of the insert command
          and inputQuery[3].count(",")==4): 
        
        lastPiece=inputQuery[3].split(',') #Parsing the last piece of the query
        
        if("(" in lastPiece[0] and lastPiece[0][:lastPiece[0].index("(")]=="values" and lastPiece[0][lastPiece[0].index("(")+1:].isdigit()
           and lastPiece[1].isalpha() and lastPiece[2].isalpha() 
           and "@" in lastPiece[3] and not lastPiece[3][:lastPiece[3].index("@")].isspace() and not lastPiece[3][lastPiece[3].index("@")+1:].isspace()
           and ")" in lastPiece[4] and lastPiece[4][:lastPiece[4].index(")")].isdigit() ):
            
            return True
        
        else:
            return False
        
    elif(string=="delete" and inputQuery[1]=="from" and inputQuery[2]=="student" and inputQuery[3]=="where" #To control the necessities of the delete command
         and  (len(inputQuery)==11 or len(inputQuery)==7 )
        and ( (inputQuery[4] in stringKeys and inputQuery[5] in condOpForString and inputQuery[6].startswith('"') and inputQuery[6].endswith('"'))
               or (inputQuery[4] in intKeys and inputQuery[5] in condOp and inputQuery[6].isdigit()) )):
            
        if(len(inputQuery)==7): #If there is no "and" or "or" operators
            return True
        elif(len(inputQuery)==11 and (inputQuery[7]=="or" or inputQuery[7]=="and") 
             and ( ((inputQuery[8] in stringKeys) and (inputQuery[9] in condOpForString) and inputQuery[10].startswith('"') and inputQuery[10].endswith('"'))
               or ((inputQuery[8] in intKeys) and (inputQuery[9] in condOp) and inputQuery[10].isdigit()) )):
            return True
        else:
            return False
    else:
        return False

def readAndSort(): #The function to read the csv file and put the data to the list of dictionaries
    with open('students.csv') as file: #Opening the file
        reader=csv.DictReader(file,delimiter=';') #To iterate in the file and create dictionaries for each row
        
        records=[] #List of dictionaries
    
        for row in reader: #To append the dictionaries of rows to the list
            lowercase_row = {k: v.lower() for k, v in row.items()}
            records.append(lowercase_row)
    for d in records:
        d['id']=int(d['id']) #To convert the id values from string to integer
        d['grade']=int(d['grade']) #To convert the grade values from string to integer
    
    records.sort(key=itemgetter('id')) #Sorting the records according to their id values
    return records

def fixcondOp(inputQuery,condOp): #To fix the condition operators given in input 
    
    if(condOp==inputQuery[6]):
        if(inputQuery[6]=="!<"):
            condOp=">="
        elif(inputQuery[6]=="!>"):
            condOp="<="
        elif(inputQuery[6]=="="):
            condOp="=="        
    else:
        if(inputQuery[10]=="!<"):
            condOp=">="
        elif(inputQuery[10]=="!>"):
            condOp="<="
        elif(inputQuery[10]=="="):
            condOp="=="        
            
    return condOp

def SELECT(records,inputQuery,keys): #The function to make select command
    
    condition=""  
    condOp=inputQuery[6]
    condOp2=inputQuery[10]
    
    condOp=fixcondOp(inputQuery,condOp) #If the first cond operator is not valid for python then fix it
    
    if(inputQuery[8]=="or" or inputQuery[8]=="and"):
        
        condOp2=fixcondOp(inputQuery,condOp2) #If the second cond operator is not valid for python then fix it
                
        condition="d['"+inputQuery[5]+"'] "+condOp+" "+inputQuery[7]+" "+inputQuery[8]+" "+"d['"+inputQuery[9]+"'] "+condOp2+" "+inputQuery[11]
              
    else: #inputQuery[8]=="order" #If there is just one condition
               
        condition="d['"+inputQuery[5]+"'] "+condOp+" "+inputQuery[7]
    
    tempList=[] #To keep dictionaries that meet the desired conditions 
    
    headers=[] #To keep the headers
    
    for d in records: #Looping over the list of dictionaries
        
        if(inputQuery[1]=="all"): #If the user wants to see data according to all headers
            if eval(condition): #If given conditions are met then add the dictionary to the tempList
                tempList.append(d)
                       
        elif(inputQuery[1] in keys): #If the user wants to see data according to just one header
            tempDict={}
            
            if eval(condition):
            #If given conditions are met then add the desired key-value to the temp dictionary, and add this dictionary to the tempList
                tempDict[inputQuery[1]]=d[inputQuery[1]]
                tempList.append(tempDict)
                
        else: #If the user wants to see data according to more than one headers
            headers=inputQuery[1].split(',')
            tempDict={}
            
            if eval(condition):
                #If given conditions are met then add the desired key-value pairs to the temp dictionary, and add this dictionary to the tempList
                for header in headers: #To add all headers and their values to the temp dictionary 
                    tempDict[header]=d[header]

                tempList.append(tempDict)
       
    
    if(inputQuery[1]=="all"):
       tempList.sort(key=lambda x: x["id"]) #Sorting by name
        
    elif(inputQuery[1] in keys):
        tempList.sort(key=lambda x: x[inputQuery[1]]) #Sorting by desired header
        
    else:
        tempList.sort(key=lambda x: x[headers[0]]) #Sorting by first desired header
               
    if(inputQuery[len(inputQuery)-1]=="dsc"): #If user wants the data in desscending order
        tempList.reverse() #Then reverse the list
    
    table = tabulate(tempList, headers="keys", tablefmt="grid")
    print(table)     
    
def findIndexesToDelete(dic, inputQuery, index4or8, index6or10, operation):
    if inputQuery[index4or8] == 'name' or inputQuery[index4or8] == 'lastname' or inputQuery[index4or8] == 'email':
        indexSet = set()#to store the elements' indexes which was entered as an input
        for i in range(len(dic)):
            ele =  dic[i]
            if operation == '=':
                if inputQuery[index6or10][1:-1] == ele.get(inputQuery[index4or8]).lower():
                    indexSet.add(i)
            elif operation == '!=':
                if inputQuery[index6or10][1:-1] != ele.get(inputQuery[index4or8]).lower():
                    indexSet.add(i)
            
    elif inputQuery[index4or8] == 'id' or inputQuery[index4or8] == 'grade':
        indexSet = set()
        for i in range(len(dic)):
            ele = dic[i]
            if operation == '=':
                    #     value from dic                 value taken from the input
                if ele.get(inputQuery[index4or8]) == int(inputQuery[index6or10]):
                    indexSet.add(i)
            elif operation == '!=':
                if  ele.get(inputQuery[index4or8]) != int(inputQuery[index6or10]):
                    indexSet.add(i)                    
            elif operation == '<':
                if  ele.get(inputQuery[index4or8]) < int(inputQuery[index6or10]):
                    indexSet.add(i)
            elif operation == '>':
                if  ele.get(inputQuery[index4or8]) > int(inputQuery[index6or10]):
                    indexSet.add(i)
            elif operation == '<=':
                if  ele.get(inputQuery[index4or8]) <= int(inputQuery[index6or10]):
                    indexSet.add(i)
            elif operation == '>=':
                if  ele.get(inputQuery[index4or8]) >= int(inputQuery[index6or10]):
                    indexSet.add(i)
            elif operation == '!<':
                if  ele.get(inputQuery[index4or8]) >= int(inputQuery[index6or10]):
                    indexSet.add(i)
            elif operation == '!>':
                if  ele.get(inputQuery[index4or8]) <= int(inputQuery[index6or10]):
                    indexSet.add(i)                
    return indexSet  
    
def DELETE(dic, inputQuery): 
    if len(inputQuery) == 7:

        set1 = findIndexesToDelete(dic, inputQuery, 4, 6, inputQuery[5])#find the element that matches the entered input
        count = 0
        sorted_list = sorted(set1, reverse = True)
        for i in sorted_list:
            print("This element is deleted", dic[i])   
            dic.pop(i)#delete the element of the list1[i] index                
            count = count + 1
        print("The number of deleted elements: ", count)
       
    elif len(inputQuery) == 11:
        if inputQuery[0] == 'delete' and inputQuery[1] == 'from' and inputQuery[2] == 'student' and inputQuery[3] == 'where':
            set1 = findIndexesToDelete(dic, inputQuery, 4, 6, inputQuery[5])#find the element that matches the entered input
            set2 = findIndexesToDelete(dic, inputQuery, 8, 10, inputQuery[9])#find the element that matches the entered input
            count = 0
            if inputQuery[7] == 'and':
                set3 = set1.intersection(set2)# find the intersection of two index sets to find the element that need to be deleted, because 'and' was used
                sorted_list = sorted(set3, reverse = True)
                for i in sorted_list:
                    print("This element is deleted", dic[i])
                    dic.pop(i)#delete the element of the list1[i] index                    
                    count = count + 1
            elif inputQuery[7] == 'or':
                set3 = set1.union(set2)# find the union of two index sets to find the element that need to be deleted, because 'or' was used
                sorted_list = sorted(set3, reverse = True)
                for i in sorted_list:
                    print("This element is deleted", dic[i])
                    count = count + 1
            
            if count == 0:
                print("There is no such person.")
            else:
                print("The number of deleted elements: ", count)
            
def INSERT(dic, inputQuery):
    if len(inputQuery) == 4 and len(inputQuery[3]) > 6:
        if inputQuery[0] == 'insert' and inputQuery[1] == 'into' and inputQuery[2] == 'student' and inputQuery[3][0:6] == 'values':
            inputQuery3 = inputQuery[3].split('(')
            datas = inputQuery3[1].split(',') #id,name,lastname,email,grade -> böyle ayrıldı
            datas[-1] = datas[-1][0:-1]#to get rid of the sign '(' at the end
            inputDict = {} # to add to the original, it will convert the given data into a dictionary and add it as a row/element
            if len(datas) == 5:#id;name;lastname;email;grade
                                    #getting the last element's id and addding 1 
                                    #to find the place for the inserted element
                inputDict =  {"id" : datas[0], "name" : datas[1], "lastname" : datas[2], "email" : datas[3], "grade" : int(datas[4])}
                print("Inserted element is: ", inputDict)
                dic.insert(len(dic), inputDict)
            
def convertToJSON(dic):
    jsonObject = json.dumps(dic, indent = 5,ensure_ascii=False)
    with open("27_2020510085_2020510017.json", "w") as outputFile:
        if not (jsonObject == ''):
            outputFile.write(jsonObject)
   
    

######################################################################################################################   
    
dic = readAndSort()#assigning the returned dictionary to a variable

print("\n(Write 'exit', if you want to end the program.)",end = '')   

keys=dic[0].keys() #Holding the key values of the dictionary

while True:
    
    inputQuery = input("Please enter the query:").lower().split(' ') #Taking the input query from the user and parsing it
    
    if inputQuery[0] == 'exit':
        print("\nThe End")
        convertToJSON(dic)
        break
        
    elif(inputQuery[0]=="select" and isQueryValid("select", inputQuery,keys)):
        SELECT(dic,inputQuery,keys)
                       
    elif((inputQuery[0]=="insert") and isQueryValid("insert", inputQuery,keys) ):
        INSERT(dic,inputQuery)
        
    elif((inputQuery[0]=="delete") and isQueryValid("delete", inputQuery,keys) ):          
        DELETE(dic, inputQuery)
            
    else:   
        print("Wrong query! Please enter again.")            
        
        
        
        
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    