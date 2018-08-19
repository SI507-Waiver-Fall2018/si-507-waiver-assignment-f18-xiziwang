# these should be the only imports you need
import sys
import sqlite3

# write your code here
# usage should be 
#  python3 part2.py customers
#  python3 part2.py employees
#  python3 part2.py orders cust=<customer id>
#  python3 part2.py orders emp=<employee last name>

###############################################################################
# README																	  #
# Author: Xizi Wang															  #
# UMID: 24226806															  #
###############################################################################

def getCustomers():
    sql_conn = sqlite3.connect('Northwind_small.sqlite')
    cursor = sql_conn.cursor()
    
    # get and print list of customers
    cursor.execute("SELECT Id,CompanyName FROM Customer")
    print("ID   Customer Name")
    for (cid, cname) in cursor.fetchall():
        print(cid,"  ",cname)
   
    # close db
    sql_conn.close()


def getEmployees():
    # connect to db
    sql_conn = sqlite3.connect('Northwind_small.sqlite')
    cursor = sql_conn.cursor()
	
    # get and print list of employees
    cursor.execute("SELECT Id,LastName,FirstName FROM Employee")
    print("ID   Employee Name")
    for (eid, elastname, efirstname) in cursor.fetchall():
        print(eid,"  ",efirstname,elastname)

    # close db
    sql_conn.close()
    

def getOrdersManagedByEmp(emp_lastname): 
    # connect to db
    sql_conn = sqlite3.connect('Northwind_small.sqlite')
    cursor = sql_conn.cursor()
	
    # get list of id 
    cursor.execute("SELECT Id FROM Employee WHERE LastName = ?", (emp_lastname,))
    id_list = cursor.fetchall()
    # get and print list of order date
    for (eid,) in id_list:
        cursor.execute("SELECT OrderDate FROM 'Order' WHERE EmployeeId = ?", (eid,))
    print("Order dates")
    for (order_date,) in cursor.fetchall():
        print(order_date)

    # close db
    sql_conn.close()


def getOrdersPlacedByCust(cust_id): 
    # connect to db
    sql_conn = sqlite3.connect('Northwind_small.sqlite')
    cursor = sql_conn.cursor()

    # get list of order date
    cursor.execute("SELECT OrderDate FROM 'Order' WHERE CustomerId = ?", (cust_id,))
    print("Order dates")
    for (order_date,) in cursor.fetchall():
        print(order_date)	

    # close db
    sql_conn.close()


if __name__ == "__main__":
    lenArgv = len(sys.argv)
    if lenArgv<2 : print("ERROR: invalid input")
    elif lenArgv==2 :
        if sys.argv[1]=="customers": getCustomers()
        elif sys.argv[1]=="employees": getEmployees()
        else: print("ERROR: invalid input")
    elif lenArgv==3 :
        if sys.argv[1]!="orders": print("ERROR: invalid input")
        else: 
            lst = sys.argv[2].split("=")
            if len(lst)!=2: print("ERROR: invalid input")
            else:
                if lst[0]=="cust": getOrdersPlacedByCust(lst[1])
                elif lst[0]=="emp": getOrdersManagedByEmp(lst[1])
                else: print("ERROR: invalid input")
    else: print("ERROR: invalid input")

