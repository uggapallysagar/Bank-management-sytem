import mysql.connector as db
con=db.connect(user='root',password='sagar@123',\
           host='localhost',database='bank')
import datetime
import random
import string   

print(datetime.datetime.now())
cur=con.cursor()
while True:
    print("1.admin")
    print('2.user')
    print('3.exit')
    choice=input("enter the options")
    if choice=='1':
        admin_id = input("Enter Admin ID: ")
        admin_pass = input("Enter Admin Password: ")
     
        cur.execute("SELECT * FROM admins WHERE id=%s AND password=%s", (admin_id, admin_pass))
        result = cur.fetchone()

        if result:
            print("Admin login successful!")
            while True:
                print('1.view all users')
                print('2.view complete account details of particular user')
                print('3.view complete transaction of particular user')
                print('4.view complete transaction of particular day')
                print('5.logout')
                admin_choice=input('enter the options')
                if admin_choice=='1':
                    cur.execute('select * from user')
                    data= cur.fetchall()
                    if data:
                        for row in data:
                            print(row)
                    

                elif admin_choice=='2':
                    acc_detail=input("enter the account_number")
                    cur.execute("select*from user where account_number=%s",(acc_detail,))
                    result=cur.fetchone()
                    if result:
                        print(result)
                    else:
                        print("no user found with that account number")
                            
                elif admin_choice=='3':
                    acc_number=input("enter account number")
                    cur.execute("select*from transactions where account_number=%s",(acc_number,))
                    transactions=cur.fetchall()
                    if transactions:
                        print("transaction for account:",acc_number)
                        for t in transactions:
                            print(t)
                    else:
                        print("no transation found for the user")
                    
                elif admin_choice=='4':
                    date=input("enter data(yyyy-mm-dd:")
                    cur.execute("select*from transactions where date(date_time)=%s",(date,))
                    transactions=cur.fetchall()
                    if transactions:
                        for t in transactions:
                            print(t)
                    else:
                        print("No transactions found for this date.")
                
                
                    
                    
                    
                if admin_choice=='5':
                    break
                #else:
                   # print("invalid choice")  
        else:
            print("Invalid Admin ID or Password")
            
#user login or register
    elif choice=='2':
        while True:
            print('1.login')
            print('2.new_registation')
            print('3.exit')
            user=input('enter the options')
            if user=='1':
                account_number=input('enter the account number')
                pin=input('enter the account pin')
                cur.execute("SELECT * FROM user WHERE account_number=%s AND pin=%s", (account_number, pin))
                result = cur.fetchone()
                if result:
                    print('login successful!',result[1],)
                    
                #else:
                   # print('inavlid id or password')
                    while True:
                        print('1.view account details')
                        print('2.debit amount')
                        print('3.credit amount')
                        print('4.pin change')
                        print('5.statement')
                        print('6.logout')
                        user_choice=input('enter the options')
                        if user_choice=='1':
                            cur.execute("SELECT * FROM user WHERE account_number=%s", (account_number,))
                            print(cur.fetchone())

                        elif user_choice=='2':
                            amount = float(input('Enter amount to debit: '))
                            amount=float(amount)
                            cur.execute("SELECT balance FROM user WHERE account_number=%s", (account_number,))
                            balance = cur.fetchone()[0]
                            if amount <= balance:
                                new_balance = balance - amount
                                cur.execute("UPDATE user SET balance=%s WHERE account_number=%s", (new_balance, account_number))
                                con.commit()
                        # Insert into transactions
                                cur.execute("INSERT INTO transactions (account_number, action, amount) VALUES (%s, %s, %s)",
                                            (account_number, 'debit', amount))
                                con.commit()
                                print("Amount debited successfully. New Balance:", new_balance)
                            else:
                                print("Insufficient balance.")
                       
                            
                            


                    
                        if user_choice=='3':
                            amount = float(input('Enter amount to credit: '))
                            cur.execute("SELECT balance FROM user WHERE account_number=%s", (account_number,))
                            result=cur.fetchone()
                            if result:
                                balance=result[0]
                                new_balance=balance+amount
                                cur.execute("UPDATE user SET balance=%s WHERE account_number=%s", (new_balance, account_number))
                                con.commit()
                        # Insert into transactions
                                cur.execute("INSERT INTO transactions (account_number, action, amount) VALUES (%s, %s, %s)",
                                        (account_number, 'credit', amount))
                                con.commit()
                                print("Amount credited successfully. New Balance:", new_balance)
                            else:
                                print("Error: Account not found!")
                        
                            
                    
                        elif user_choice=='4':
                            new_pin=input('enter the new pin')
                            new_conform=input('enter the new confirm pin')
                            if new_pin==new_conform and len(new_pin)==4 and new_pin.isdigit():
                                cur.execute("update user set pin=%s where account_number =%s",(new_pin, account_number))
                                con.commit()
                                print(" new pin is updated")
                            else:
                                print("newpin and confirm pin does not match")
                        # paricular transations details with data
                        if user_choice == '5':
                            start_date = input("Enter start date (YYYY-MM-DD): ")
                            end_date = input("Enter end date (YYYY-MM-DD): ")
                            if len(start_date) == 10 and start_date[4] == '-' and start_date[7] == '-' and \
                               len(end_date) == 10 and end_date[4] == '-' and end_date[7] == '-':
                               
                                cur.execute("""
                                    SELECT * FROM transactions
                                    WHERE account_number = %s AND DATE(date_time) BETWEEN %s AND %s
                                    ORDER BY date_time DESC
                                """, (account_number, start_date, end_date))
                                transactions = cur.fetchall()
                                if transactions:
                                    print("----- Account Statement -----")
                                    for t in transactions:
                                        print(t)
                                else:
                                    print("No transactions found for this period.")
                            else:
                                print("Please enter correct date")
                            # exiting from user
                        elif user_choice=='6':
                            print("exiting from the user")
                            break
                        else:
                            print('enter the valid option')
                else:
                    print("invalid account number or pin") 

            
            elif user=='2':
                firstname=input('enter the firstname')
                lastname=input('enter the lastname')
                name=firstname+lastname

                def get_gmail():
                    gmail = input("Enter your Gmail address (must end with @gmail.com): ")
                    if gmail.endswith("@gmail.com"):
                        return gmail
                    print("Error: Invalid email.")
                    return get_gmail()
                gmail = get_gmail()

                def phone_number():
                    phone_no=input('enter the phone number')
                    if phone_no.isdigit() and len(phone_no)==10 and phone_no[0]in'6789' :
                        return phone_no
                    else:
                        print("invalid phone number try again")
                phone_no = phone_number()
                def account():
                    account_type = input("Enter account type (savings/current): ").lower().strip()
                    while account_type not in ["savings", "current"]:
                        print("Invalid account type! Please enter either 'savings' or 'current'.")
                        account_type = input("Enter account type (savings/current): ").lower().strip()
                    return account_type
                account_type = account() 
              
                    
                while True:
                    pin=input('enter the 4 digit pin')
                    confirm=input('enter the confirm pin 4 digit pin')
                    if pin.isdigit()and len(pin)==4 and pin==confirm:
                        print('pin set successfuly')
                        
                        
                        account_number = "acc" + str(random.randint(1000000, 9999999))
                       
                        cur.execute("""
                        INSERT INTO user (account_number,name, gmail, phone_no, pin,account_type)
                        VALUES (%s, %s, %s, %s, %s, %s)""", (account_number, name, gmail, phone_no, pin,account_type))                    
                        con.commit()
                                        
                                     
                        print(" Registration successful!")
                        print("Account Number:", account_number)
                        print("Name:", firstname, lastname)
                        print("Gmail:", gmail)
                        print("Phone:", phone_no)
                        print(f"account_type:{account_type}")
                       
                        break
                    else:
                        print("invalid!! pin does not match enter exactly 4 digit pin")
            elif user=='3':
                print("exiting from user ")
                break
    elif choice=='3':
        print('exiting from the bank thanking for visiting!!!!!')
        break
    
        
        
    else:
        print("enter the valid option")
       
           

cur.close()
con.close()
        
