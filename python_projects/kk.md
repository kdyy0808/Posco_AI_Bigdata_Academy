import os
import operator
import sys

if len(sys.argv) == 1:
    file_name_r="students.txt"
else:
    file_name_r=sys.argv[1]

global score_board_dict
score_board_dict =dict() 
global score_board_keys
score_board_keys =list()

global shut_down_flag
shut_down_flag= False

def get_total_score(midterm_score,final_score):
    total_score = 0.5*float(midterm_score) + 0.5*float(final_score)
    if total_score >= 90:
        total_result = "A"
    elif total_score >= 80:
        total_result = "B"
    elif total_score >= 70:
        total_result = "C"
    elif total_score >= 60:
        total_result = "D"
    else:
        total_result = "F"
    return str(total_score)+"({}".format(total_result)+")"

def get_rank(score):
    if score >= 90:
        total_result = "A"
    elif score >= 80:
        total_result = "B"
    elif score >= 70:
        total_result = "C"
    elif score >= 60:
        total_result = "D"
    else:
        total_result = "F"
    return total_result

def load_data():
    global score_board_keys
    
    if os.path.exists(file_name_r):
        with open(file_name_r,"r") as f:
            while True:
                line = f.readline()
                if line =="":
                    break
                line_list = line.split()
                if line_list[0] not in score_board_dict.keys():
                    mean_score = 0.5*(int(line_list[3])+int(line_list[4]))
                    score_board_dict[line_list[0]] = (line_list[1] +" "+ line_list[2], line_list[3],line_list[4],mean_score ,get_rank(mean_score))
    #print(score_board_dict)
    score_board_keys=list(score_board_dict.keys())
    #print(score_board_keys)
    #print("load end")
def save_data():
    with open(file_name_w,"w") as f:
        for stu_num in range(len(score_board_dict)):
            
            stu_id = score_board_keys[stu_num]
            stu_name, stu_mid, stu_fin,stu_mean,stu_grade = score_board_dict[score_board_keys[stu_num]]
            f.write("{}\t {}\t {}\t{}\t{}\t{}\n".format(stu_id,stu_name,stu_mid, stu_fin,stu_mean,stu_grade))
    #         print("{} {} {}\t{}".format(stu_id,stu_mid, stu_fin,stu_total))
    #print("Student\t"+"Name".rjust(10)+"\tMidterm \tFinal \tFinal \tAverage \tGrade")

def print_title():
    print("Student\t"+"  \t \t   Name".rjust(10)+"\t      Midterm \tFinal \tAverage \tGrade")
    print("-----------------------------------------------------------------------------")
def print_stu_info(stu_id):
    #stu_id = sorted_score_board_keys[stu_num]
    stu_name, stu_mid, stu_fin,stu_mean,stu_grade = score_board_dict[stu_id]
    print("{}\t".format(stu_id)+"{}".format(stu_name).rjust(15),end="")
    print(" \t{}\t{}\t{:.1f}\t\t{}\n".format(stu_mid, stu_fin,stu_mean,stu_grade))
    
def show_result(sort=0):

#     score_board_dict
    print_title()
    global score_board_keys
    #print(score_board_dict.items())

    ##평균 기준으로 정렬
    sorted_score_board_list = sorted(score_board_dict.items(), key=lambda x : x[1][3],reverse=True)
    sorted_score_board_keys = list()
    for stu_num in range(len(sorted_score_board_list)):
        sorted_score_board_keys.append(sorted_score_board_list[stu_num][0])
    
    #print(list(score_board_dict.keys))
    #print(sdict)
    for stu_num in range(len(score_board_dict)):
        #print(score_board_keys)
        #print(stu_num)
        stu_id = sorted_score_board_keys[stu_num]
        stu_name, stu_mid, stu_fin,stu_mean,stu_grade = score_board_dict[sorted_score_board_keys[stu_num]]
        print("{}\t".format(stu_id)+"{}".format(stu_name).rjust(15),end="")
        print(" \t{}\t{}\t{:.1f}\t\t{}\n".format(stu_mid, stu_fin,stu_mean,stu_grade))

def search_result():
    input_stu_id = input("Student ID:")
    #print(list(score_board_dict.keys()))
    if input_stu_id in score_board_dict.keys():
        print_title()
        print_stu_info(input_stu_id)
    else:
        print("NO SUCH PERSON.")
        
def change_score():
    input_stu_id = input("Student ID:")
    if input_stu_id in score_board_dict.keys():
        Mid_or_Final_key = 0 #Mid 고칠거면 0 Fin고칠거면 1
        
        chosed_case=input("mid/final? ")
        if chosed_case == "mid":
            Mid_or_Final_key = 0
        elif chosed_case == "final":
            Mid_or_Final_key = 1
        else :
            #mid or final값이 아닐경우 
            #print("Wrong_Input")
            return
        
        revised_score = input("Input new score:")
        
        #0~100 외의 값이 입력된 경우
        if 0 > int(revised_score) or int(revised_score) > 100:
            return
        
        print_title()
        print_stu_info(input_stu_id)
        
        #print(score_board_dict[input_stu_id])
        #print(score_board_dict[input_stu_id][Mid_or_Final_key+1])#인덱스 때문에 +1
        
        change_Dict_Inner_value(input_stu_id,Mid_or_Final_key,revised_score)
        
        print("Score changed.")
        print_stu_info(input_stu_id)
        #score_board_dict[input_stu_id][Mid_or_Final_key+1] = revised_score
        #print(score_board_dict[input_stu_id][Mid_or_Final_key+1])#인덱스 때문에 +1
        
        
    else:
        print("NO SUCH PERSON.")
        return

def change_Dict_Inner_value(stu_id,Mid_or_Final,value):
    
    global score_board_dict
    
    #stu_id = score_dict[]
    stu_name, stu_mid, stu_fin, stu_average, stu_grade = score_board_dict[stu_id]
    
    if Mid_or_Final == 0:
        stu_mid = value
    elif Mid_or_Final == 1:
        stu_fin = value
    else:
        #mid or Final외의 값이 입력되었을때
        return
    
    stu_average = float((int(stu_mid) + int(stu_fin))*0.5)
    stu_grade = get_rank(stu_average)
    
    revised_value = (stu_name, stu_mid, stu_fin, stu_average, stu_grade)
    #score_board_dict.update("{}".format(stu_id) = revised_value)
    score_board_dict[stu_id] =revised_value
    
    
def add_Dict_Inner_value():
    
    global score_board_dict
    
    
    stu_id = input("Student ID:")
    
    if stu_id in score_board_dict.keys():
        print("ALREADY EXISTS.")
        return
    
    stu_name = input("Name:")
    stu_mid = input("Midterm Score:")
    stu_fin = input("Final Score:")
    
    stu_average = float((int(stu_mid) + int(stu_fin))*0.5)
    stu_grade = get_rank(stu_average)
    
    revised_value = (stu_name, stu_mid, stu_fin, stu_average, stu_grade)
    #score_board_dict.update("{}".format(stu_id) = revised_value)
    score_board_dict[stu_id] =revised_value
    
    print("Student added")
    
def search_grade():
    
    global score_board_dict
    
    stu_ids = list(score_board_dict.keys())
    
    Search_rank=input("Grade to search:")
    if Search_rank not in ['A','B','C','D','F']:
        return
    print_title()
    
    grade_stu_count = 0
    
    for stu_id in stu_ids:
        if score_board_dict[stu_id][4] == Search_rank:
            print_stu_info(stu_id)
            grade_stu_count+=1
    if grade_stu_count == 0:
        print("NO RESULTS.")

def remove_stu_info():
    
    global score_board_dict
    global score_board_keys
    stu_ids = list(score_board_dict.keys())
    
    if len(score_board_dict) == 0:
        print("List is empty")
        return
    
    stu_id=input("Student ID:")
    if stu_id not in stu_ids:
        print("NO SUCH PERSON.")
        return
    
    del score_board_dict[stu_id]
    score_board_keys = list(score_board_dict.keys())
    print("Student removed.")
    
def quit_program():
    global score_board_dict
    global shut_down_flag
    global score_board_keys
    
    score_board_keys = list(score_board_dict.keys())
    
    sorted_score_board_list = sorted(score_board_dict.items(), key=lambda x : x[1][3],reverse=True)
    sorted_score_board_keys = list()
    for stu_num in range(len(score_board_dict)):
        sorted_score_board_keys.append(sorted_score_board_list[stu_num][0])
    score_board_keys = sorted_score_board_keys

    
    shut_down_flag = True
    answer = input("Save data?[yes/no]")    
    
    if answer =="no":
        print("quit without save ")
        return
    file_name = input("File name:")
    
    with open(file_name,"w") as f:
        for stu_num in range(len(score_board_dict)):#########################################
            stu_id = score_board_keys[stu_num]
            stu_name, stu_mid, stu_fin, stu_mean, stu_grade = score_board_dict[stu_id]
            f.write("{}\t {}\t {}\t{}\n".format(stu_id, stu_name, stu_mid, stu_fin))
            #print("{} {} {}\t{}".format(stu_id, stu_name, stu_mid, stu_fin))
        
    
    
    
def command_waiting():
    command_input=input("#")
    if command_input == "show":
        show_result()
    elif command_input == "search":
        search_result()
    elif command_input == "changescore":
        change_score()
    elif command_input == "add":
        add_Dict_Inner_value()
    elif command_input == "searchgrade":
        search_grade()
    elif command_input == "remove":
        remove_stu_info()
    
    elif command_input == "quit":
        quit_program()
    
    elif command_input == "0":
        return 0
    else:
        print("error")


def main():
    
    load_data()
    while shut_down_flag == False:
        if command_waiting() == 0:
            return

if __name__ == '__main__' :
    main()
