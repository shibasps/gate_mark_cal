import re
import urllib.request

qpaper_code=input("Put your course code in GATE (e.g for Chemistry- CY) ")
#print(response.read())

def info(questions):
    t= "Participant ID</td>  <td>"
    a=questions.find(t)
    b=questions.find("<",a+len(t)+1)
    print("\tParticipant ID\t", questions[a+len(t):b])
    t= "Participant Name</td>  <td>"
    a=questions.find(t)
    b=questions.find("<",a+len(t)+1)
    print("\tParticipant Name", questions[a+len(t):b])

def main():
    if (qpaper_code=="CY" or qpaper_code=="cy"):
        answer_file= "chemans"
        calculator(answer_file)
    elif (qpaper_code=="XL" or qpaper_code=="xl" ):
        answer_file= "biologyans"
        calculator(answer_file)
    elif (qpaper_code=="BT" or qpaper_code=="bt"):
        answer_file= "biotechans"
        calculator(answer_file)
    elif (qpaper_code=="PH" or qpaper_code=="ph"):
        answer_file= "phans"
        calculator(answer_file)
    elif (qpaper_code=="MA" or qpaper_code=="ma"):
        answer_file= "maans"
        calculator(answer_file)
    else:
        print("The calculator hasn't been configured for your course. Pleas keep visiting. Please abort")

def calculator(answer_file):
    url=input("Put your Response sheet url,\n")
    response = urllib.request.urlopen(url)

    with open(answer_file, 'r') as answer_file:
        array = [[float(x) for x in line.split()] for line in answer_file]
    data=str(response.read()).split('\n')
    questions=(data[0].split("src="))
    info(questions[2])
    
    qid_start=100000000000000
    for i in questions[3:]:
        chk= 'Question ID :</td><td class="bold">'
        a= i.find(chk)
        qid=float(i[a+len(chk): a+len(chk)+11])
        qid_start= min(qid_start,qid)
    mark=0
    n=0

    print("QN\t", "QID\t", "Given Ans\t", "Mark\t", "Off Ans")
    for i in questions[3:]:
        p=0
        chk= 'Question ID :</td><td class="bold">'
        ans='Chosen Option :</td><'
        a= i.find(chk)
        b= i.find(ans)
        if (b== -1):
            neg=0
            ans= 'Given Answer :</td><'
            b= i.find(ans)
            p=1
        else:
            neg=-1/3
        c= i.find(">", b+ len(ans)+1)
        d= i.find("<", b+len(ans)+1)
        if (i.find("Not Attempted and Marked For Review") == -1 and i.find('Not Answered') == -1):
             q_id=float(i[a+len(chk): a+len(chk)+11])
    #            print(q_id)
             giv_answer= float(i[c+1:d])
             for x in array:
                 qid = qid_start + x[0] -1
                 if qid==q_id:
                     if x[1]<=giv_answer<=x[2]:
                         mark+=x[3]
                         n+=1
                         if (p == 0):
                             print(int(n), "\t", int(q_id), "\t", int(giv_answer), "\t", int(x[3]), "\t", int(x[1]))
                         else:
                             print(int(n), "\t", int(q_id), "\t", giv_answer, "\t", int(x[3]), "\t", x[1], "to", x[2])
                     else:
                         mark+=(neg*x[3])
                         n+=1
    #                     print(n, "\t",q_id, "\t", giv_answer, "\t", neg*x[3])
                         if (p == 0):
                             print(int(n), "\t", int(q_id), "\t", int(giv_answer), "\t", "{0:.2f}".format(neg*x[3]), "\t", int(x[1]))
                         else:
                             print(int(n), "\t", int(q_id), "\t", giv_answer, "\t", "{0:.2f}".format(neg*x[3]), "\t", x[1], "to", x[2])
    
                     break
        else:
             q_id=float(i[a+len(chk): a+len(chk)+11])
             n+=1
             for x in array:
                 qid = qid_start + x[0] -1
                 if qid==q_id:
    #                 print(n, "\t",q_id, "\t", '--',"\t", 0)
                     if (p == 0):
                         print(int(n), "\t", int(q_id), "\t", '--', "\t", 0, "\t", int(x[1]))
                     else:
                         print(int(n), "\t", int(q_id), "\t", '--', "\t", 0, "\t", x[1], "to", x[2])
    print("\t","\t","Total Mark","\t","{0:.2f}".format(mark))

main()
