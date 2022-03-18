import mysql.connector as mysql
import datetime as d
admin_name="admin"
admin_pass="password"

db=mysql.connect(
    host="localhost",
    user="root",
    password="",
    database="python_college"
    )
command=db.cursor(buffered=True)    # to run different sql queries

def admin_task():
    print("\nAdmin Login Successfull")
    while 1:
        print("\nAdmin Menu\n")
        print("1.Register a new Student\n2.Register a new Teacher\n3.Delete existing Student")
        print("4.Delete existing Teacher\n5.Logout")
        option=int(input("Option : ").strip())
        if option==1:
            print("\nRegister new Student\n")
            stud_name=input("New Student username : ").strip()
            stud_pass=input("New Student password : ").strip()
            vals=(stud_name,stud_pass)
            try:
                command.execute("INSERT INTO users (username,password) VALUES (%s,%s)",vals)
                db.commit()
                print('"'+stud_name.upper()+"' has been registered Successfuly")
            except Exception as e:
                print("Error occured : ",e)
        elif option==2:
            print("\nRegister new Teacher\n")
            teach_name=input("New Teacher username : ").strip()
            teach_pass=input("New Teacher password : ").strip()
            teach_pos=input(teach_name.upper()+"'s position : ").strip()
            vals=(teach_name,teach_pass,teach_pos)
            try:
                command.execute("INSERT INTO teachers (username,password,posting) VALUES(%s,%s,%s)",vals)
                db.commit()
                print("\n"+teach_name.upper()+" has been registered successfully ")
            except Exception as e:
                print("\n"+"Error occured : ",e)
        elif option==3:
            print("\nDelete existing Student\n")
            name=input("Student username : ").strip()
            vals=(name,)
            try:
                command.execute("DELETE FROM users WHERE username = %s",vals)
                db.commit()
                if command.rowcount<1:
                    print("No Student found")
                else:
                    print("\n"+name.upper()+" has been Deleted successfully")
            except Exception as e:
                print("Error occured : ",e)
        elif option==4:
            print("\nDelete existing Teacher\n")
            name=input("Teacher username : ").strip()
            vals=(name,)
            try:
                command.execute("DELETE FROM teachers WHERE username = %s",vals)
                db.commit()
                if command.rowcount<1:
                    print("No Teacher found")
                else:
                    print("\n"+name.upper()+" has been Deleted successfully")
            except Exception as e:
                print("Error occured : ",e)
        elif option==5:
            print("Logout successfull")
            break



            

def admin_auth():
    print("\nAdmin Login\n")
    username=input("Admin username : ").strip()
    password=input("Admin password : ").strip()
    if username ==admin_name:
        if password==admin_pass:
            admin_task()
            print("********************")
        else:
            print("\nCheck Your password")
    else:
        print('\nInvalid Username')

def teach_act():
    print("\nTeachers Menu")
    print("1.Enter or Update Student mark\n2.View\n3.Logout")
    ch=int(input("Option : ").strip())
    if ch==1:
        print("\nEnter or Update Student marks\n")
        name=input("Student name : ")
        mark=int(input("Student mark : "))
        if mark >25 or mark <0:
            print("\nInvalid Mark  (0<mark<25)")
            return 
        now=d.datetime.now()
        str_date=now.strftime('%Y-%m-%d %H:%M:%S')
        vals=(mark,str(str_date),name)
        try:
            command.execute("Update users set internal = %s , last_updated = %s  WHERE username = %s",vals)
            db.commit()
            if command.rowcount <1:
                print("\nNo Student found")
            else:
                print("\nMarks entered Successfuly")
        except Exception as e:
            print("Error occured : ",e)
    if ch==2:
        print("\nStudents Info\n")
        try:
            command.execute("SELECT id,username,internal from users")
            rows=command.fetchall()
            print("\n----------------------------------------------")
            print("ID\t     NAME \t\tMARKS")
            print("----------------------------------------------")
            for r in rows:
                print("{}.\t{:>10}\t\t{}\t".format(r[0],r[1],r[2]))
                print("----------------------------------------------")
        except Exception as e:
            print("Error occured : ",e)
    elif ch==3:
        print("Logout successfull")
        return
    

def teach_auth():
    teach_name=input("Teacher's username : ").strip()
    teach_pass=input("Teacher's Password : ").strip()
    vals=[teach_name,teach_pass]
    try:
        command.execute("SELECT * FROM teachers WHERE username = %s and password= %s",vals)
        db.commit()
        if command.rowcount >0:
            print("\nWelcome {}".format(vals[0].upper()))
            teach_act()
        else:
            print("\nInvalid Credentials , try to Enter data Correctly")

    except Exception as e:
        print("Error Occured : ",e)

def stud_auth():
    stud_name=input("Student name : ").strip()
    stud_pass=input("Student Password : ").strip()
    vals=[stud_name,stud_pass]
  
    command.execute("SELECT * FROM users where username =%s and password = %s",vals)
    rows=command.fetchall()
    if command.rowcount >0:
        print("\n{}'s Internal mark is : {}".format(stud_name.upper(),rows[0][3]))
    else:
        print("Invalid Credentials")

        
   



def main():
    while 1:
        print("\nWelcome to the college System\n")
        print("1.Login as Student\n2.Login as Teacher\n3.Login as Admin\n4.Exit")

        option=int(input("Option : ").strip())
        if option==1:
            stud_auth()
        elif option==2:
            teach_auth()
        elif option==3:
            admin_auth()
        elif option==4:
            print("\nExited")
            break
        else:
            print("Invalid Option")
main()