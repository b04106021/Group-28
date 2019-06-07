#檢查使用者是否輸入有效的學號
#(因為不清楚學士班以外的學號編制，所以以下只檢查學士班的學號編制)
def is_student_number(studentidstr):
    
    
    #check length
    if len(studentidstr) != 9:
        return False
        
    #check  first letter 
    code1 = studentidstr[0]
    if code1 != "B" or code1 != "b"
        return False
    
    
    #skip checking  admission year
    
    
    #check college
    code_college = studentidstr[3]
        
    #先檢查法律學院(A)&生命科學院(B)
    if code_college =="A" or code_college == "B":
        continue    
        
    #已排除法律學院(A)&生命科學院(B)，檢查是否為剩下的學院
    else:
        #如果不是數字就return false
        try:
            code_college = int(studentidstr[3])
        except:
            return False
            
        #檢查是否為剩下的學院
        if code_college > 9 or code_college < 1:
            return False


    #check department
    #法律 政治 工館 學號編制特殊(分組) 在前面先特別處理
    code_department = studentidstr[4:6]
    special_code_for_law_politic_ba = studentidstr[4:7]
    
    try:
        int_code_department = int(code_department)
    except:
        return False
    
    if code_college =="A" and (special_code_for_law_politic_ba not in [str(011), str(012), str(013)] ):
        return False
    if code_college =="3" and studentidstr[5] == "2" and (special_code_for_law_politic_ba not in [str(021), str(022), str(023)] ):
        return False
    if code_college =="7" and  studentidstr[5] == "1" and (special_code_for_law_politic_ba not in [str(011), str(012)]):
        return False

    if str(code_college) == "1" and (int_code_department > 9 or int_code_department < 1):
        return False
    elif str(code_college) == "2" and (int_code_department > 9 or int_code_department < 1):
        return False
    elif str(code_college) == "3" and (int_code_department > 5 or int_code_department < 1) and int_code_department != 10:
            return False
    elif str(code_college) == "4" and (int_code_department > 9 or int_code_department < 1):
        return False
    elif str(code_college) == "5" and (int_code_department > 7 or int_code_department < 1):
        return False
    elif str(code_college) == "6" and (int_code_department > 13 or int_code_department < 1):
        return False
    elif str(code_college) == "7" and (int_code_department > 5 or int_code_department < 1):
        return False
    elif str(code_college) == "8" and int_code_department != 1:
        return False
    elif str(code_college) == "9"  and (int_code_department > 2 or int_code_department < 1):
        return False
    elif code_college == "B" and  (int_code_department > 2 or int_code_department < 1):
        return False
    
    #check seat number inaccurately
    code_seat_number = studentidstr[6:9]
    try:
        int_code_seat_number = int(code_seat_number)
    except:
        return False
        
    if int_code_seat_number > 350:
        return False