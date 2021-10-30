import os
import sys

#터미널에서 파일명 불러오기
if len(sys.argv) == 2:
    file_name_r=sys.argv[1]
else:
    file_name_r="students.txt"

#저장할 dictionary와 키값을 저장할 list생성
global score_board_dict
score_board_dict =dict() 
global score_board_keys
score_board_keys =list()

#프로그램 종료 판단 Flag
global shut_down_flag
shut_down_flag= False

#시험점수 입력받아 학점 반환
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

#초기 txt파일 데이터 로딩
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
    score_board_keys=list(score_board_dict.keys())
    
#데이터 txt파일로 저장
def save_data():
    with open(file_name_w,"w") as f:
        for stu_num in range(len(score_board_dict)):
            
            stu_id = score_board_keys[stu_num]
            stu_name, stu_mid, stu_fin,stu_mean,stu_grade = score_board_dict[score_board_keys[stu_num]]
            f.write("{}\t {}\t {}\t{}\t{:.1f}\t{}\n".format(stu_id,stu_name,stu_mid, stu_fin,stu_mean,stu_grade))

#터미널에 표 양식 출력
def print_title():
    print("Student\t"+"  \t \t   Name".rjust(10)+"\t      Midterm \tFinal \tAverage \tGrade")
    print("-----------------------------------------------------------------------------")

#터미널에 한 학생 데이터 출력
def print_stu_info(stu_id):
    #stu_id = sorted_score_board_keys[stu_num]
    stu_name, stu_mid, stu_fin,stu_mean,stu_grade = score_board_dict[stu_id]
    print("{}\t".format(stu_id)+"{}".format(stu_name).rjust(15),end="")
    print(" \t{}\t{}\t{:.1f}\t\t{}".format(stu_mid, stu_fin,stu_mean,stu_grade))
    
#1.Show 명령 실행 -> 전체 학생 정보출력(평균 점수기준 내림차순)
def show_result(sort=0):
    
    #예외처리 : 목록에 아무도 없을 경우
    if len(score_board_dict) == 0:
        print("There is no data.")
        return
    
    print_title()
    global score_board_keys

    ##평균 기준으로 정렬
    sorted_score_board_list = sorted(score_board_dict.items(), key=lambda x : x[1][3],reverse=True)
    sorted_score_board_keys = list()
    for stu_num in range(len(sorted_score_board_list)):
        sorted_score_board_keys.append(sorted_score_board_list[stu_num][0])
    
    for stu_num in range(len(score_board_dict)):
        stu_id = sorted_score_board_keys[stu_num]
        stu_name, stu_mid, stu_fin,stu_mean,stu_grade = score_board_dict[sorted_score_board_keys[stu_num]]
        print("{}\t".format(stu_id)+"{}".format(stu_name).rjust(15),end="")
        print(" \t{}\t{}\t{:.1f}\t\t{}\n".format(stu_mid, stu_fin,stu_mean,stu_grade))
        
#2.Search 명령 실행 -> 특정학생 정보 출력
def search_result():
    input_stu_id = input("Student ID:")
    if input_stu_id in score_board_dict.keys():
        print_title()
        print_stu_info(input_stu_id)
    #예외처리 항목
    else:
        print("NO SUCH PERSON.")
        
#3.Changescore 명령 실행 -> 특정 학생의 점수 수정        
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
            #예외 처리 : mid or final값이 아닐경우 
            print("mid 또는 final 을 입력해주세요")
            return
        
        revised_score = input("Input new score:")
        
        #예외 처리 : 0~100 외의 값이 입력된 경우
        if 0 > int(revised_score) or int(revised_score) > 100:
            print("0~100 사이의 숫자를 입력하세요")
            return
        
        print_title()
        print_stu_info(input_stu_id)
        change_Dict_Inner_value(input_stu_id,Mid_or_Final_key,revised_score)
        
        print("Score changed.")
        print_stu_info(input_stu_id)
    
    #예외 처리 : 학번이 목록에 없을 경우
    else:
        print("NO SUCH PERSON.")
        return

#dictionary 내부 값 변경함수
def change_Dict_Inner_value(stu_id,Mid_or_Final,value):
    
    global score_board_dict
    
    stu_name, stu_mid, stu_fin, stu_average, stu_grade = score_board_dict[stu_id]
    
    if Mid_or_Final == 0:
        stu_mid = value
    elif Mid_or_Final == 1:
        stu_fin = value
    else:
        #mid or Final외의 값이 입력되었을때
        print("mid 또는 final 을 입력해주세요")
        return
    
    stu_average = float((int(stu_mid) + int(stu_fin))*0.5)
    stu_grade = get_rank(stu_average)
    
    revised_value = (stu_name, stu_mid, stu_fin, stu_average, stu_grade)
    score_board_dict[stu_id] =revised_value
    
#4.Add 명령 실행 -> dictionary 내부 값 추가 함수
def add_Dict_Inner_value():
    
    global score_board_dict
    
    stu_id = input("Student ID:")
    
    #에러처리 : 목록에 있는 학생의 학번 입력시
    if stu_id in score_board_dict.keys():
        print("ALREADY EXISTS.")
        return
    
    stu_name = input("Name:")
    stu_mid = input("Midterm Score:")
    
    #예외 처리 : 범위 밖의 점수를 입력하였을 경우
    if int(stu_mid)<0 or int(stu_mid)>100:
        print("값은 0~100사이의 값이어야합니다 다시 처음부터 추가해주세요")
        return
    stu_fin = input("Final Score:")
    if int(stu_mid)<0 or int(stu_mid)>100:
        print("값은 0~100사이의 값이어야합니다 다시 처음부터 추가해주세요")
        return
    
    stu_average = float((int(stu_mid) + int(stu_fin))*0.5)
    stu_grade = get_rank(stu_average)
    
    revised_value = (stu_name, stu_mid, stu_fin, stu_average, stu_grade)
    score_board_dict[stu_id] =revised_value
    
    print("Student added")
    
#5.Searchgrade 명령 실행 -> 특정 Grade의 학생 모두 출력
def search_grade():
    
    global score_board_dict
    
    stu_ids = list(score_board_dict.keys())
    
    Search_rank=input("Grade to search:")
    #예외처리 A,B,C,D,F 외의 값이 입력된 경우
    if Search_rank not in ['A','B','C','D','F']:
        print("학점은 A,B,C,D,F 중 하나여야 합니다.")
        return
    
    
    grade_stu_count = 0
    
    for stu_id in stu_ids:
        if score_board_dict[stu_id][4] == Search_rank:
            grade_stu_count+=1
    
    #예외처리 : 해당 grade의 학생이 없는 경우
    if grade_stu_count == 0:
        print("NO RESULTS.")
        return

    print_title()
    for stu_id in stu_ids:
        if score_board_dict[stu_id][4] == Search_rank:
            print_stu_info(stu_id)
        
#6. Remove 명령 실행 -> 특정 학생의 정보 삭제
def remove_stu_info():
    
    global score_board_dict
    global score_board_keys
    stu_ids = list(score_board_dict.keys())
    
    #예외처리 : 목록에 아무도 없을 경우
    if len(score_board_dict) == 0:
        print("List is empty")
        return
    
    stu_id=input("Student ID:")
    
    #예외 처리 : 학생이 목록에 없는 경우
    if stu_id not in stu_ids:
        print("NO SUCH PERSON.")
        return
    
    del score_board_dict[stu_id]
    score_board_keys = list(score_board_dict.keys())
    print("Student removed.")
    
#7. quit명령 실행 -> 데이터 txt파일로 저장 여부 선택 및 프로그램 종료
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
        for stu_num in range(len(score_board_dict)):
            stu_id = score_board_keys[stu_num]
            stu_name, stu_mid, stu_fin, stu_mean, stu_grade = score_board_dict[stu_id]
            f.write("{}\t {}\t {}\t{}\n".format(stu_id, stu_name, stu_mid, stu_fin))
def show_command_list():
    print("-"*32+"COMMAND LIST"+"-"*32)
    print("show | search | changescore | searchgrade | add | remove | quit")

def show_help():
    print("-------help--------")
    print("다음과 같은 명령어가 있습니다.")
    print("show -> 학생들의 정보를 보여줍니다.")
    print("search -> 학생의 학번을 이용하여 특정 학생의 정보를 보여줍니다.")
    print("add -> 정보에 없는 학생의 정보를 추가합니다.")
    print("searchgrade -> 특정 학점을 취득한 학생을 모아서 보여줍니다.")
    print("remove -> 특정 학생의 정보를 제거합니다.")
    print("quit -> 프로그램을 종료합니다.")
    print("help -> 명령어 목록을 보여줍니다.")
    
#메인 명령 대기 쓰레드            
def command_waiting():
    command_input=input("#")
    #입력한 명령어의 대소구분을 없애기 위해 다 소문자로 변환
    command_input = command_input.lower()
    
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
    
    #입력한 명령 이외의 명령이 들어왔을 때,아무 에러메세지 없이 다음명령을 받으라고 명시되있어서 아래 코드는 주석처리 하였다.
#     elif command_input == "help":
#         show_help()
#     else:
#         print('error : Enter the correct command, if you need help : enter the command help" ')


def main():
    
    load_data()
    show_result()
    show_command_list()
    
    while shut_down_flag == False:
        command_waiting()

if __name__ == '__main__' :
    main()
