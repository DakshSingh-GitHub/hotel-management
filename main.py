import mysql.connector as sql
from datetime import datetime
import mysql.connector.errors
import time
from colorama import Fore, Style
import matplotlib as mt
import matplotlib.pyplot as plt


class GenderInputException(Exception): pass
class DateLimitCheckError(Exception): pass
class EndCode(Exception): pass
class DateLimitExceedError(Exception): pass
class MonthLimitExceedError(Exception): pass

countToExpire = 5

def countdown(c=30):  
    """
    A function that counts down from a given number 'c' in minutes and seconds format, displaying a message indicating the remaining time. It uses the 'Fore.BLUE' color to display the countdown message. Once the countdown reaches 0, it displays a message indicating that the login session has expired. This function does not return any value.
    """
    while c:  
        m, s = divmod(c, 60)  
        text = 'Login Session Out in: {:02d}:{:02d}'.format(m, s)  
        print(Fore.BLUE + text, end="\r")  
        time.sleep(1)  
        c -= 1 
    text = "Login Session Expired [ERR] {MAKE NEW LOGIN SESSION}"
    print(Fore.RED + text)
    print(Style.RESET_ALL,end="")


for i in range(5):
    # ---------------------------------USER BYPASS LOGIN---------------------------------------- #
    # userID: str = str(input(Fore.GREEN + "User: "))
    # passwd: str = str(input("Password: "))
    # print(Style.RESET_ALL, end="")
    userID = "DakshSingh"
    passwd = "dakshsingh"
    # passwd = "tmkcbcccmc@69"
    # ---------------------------------USER BYPASS LOGIN---------------------------------------- #
    try:
        conn = sql.connect(host="localhost", user=userID, password=passwd, database="hotel")
        break
    except mysql.connector.errors.ProgrammingError:
        print(Fore.RED +'Wrong UserId or Password')
        print(Style.RESET_ALL,end="")
else:
    countdown(countToExpire)
    print(Fore.RED + '[DENIED] USER ID OR PASSWORD WRONG')
    print(Style.RESET_ALL, end="")
    
try:
    cursor = conn.cursor(buffered=True)

    c_id = 1001
    book_id = 5001
    room_id = 2001

    s_room = [2002, 2003]
    np_room = [2001, 2004]
    room_list_indexer_s = 0
    room_list_indexer_np = 0


    def checkAvailableRoom(checkin:str, date_format="%Y-%m-%d", type="np"):
        """
        This function checks the availability of a room based on the check-in date, room type, and date format.
        It returns the room ID and tariff if available, otherwise, it returns an error message or expiration message.
        """
        global room_list_indexer_s          # UNBOUND ERROR: import from global scope
        global room_list_indexer_np
        global cursor
        cursor.execute("SELECT * FROM av_room")
        roomdata = cursor.fetchall()
        for i in roomdata:
            if tuple(i)[-2] == type:
                date = str(tuple(i)[2])
                try:
                    date1 = datetime.strptime(date, date_format)
                    date2 = datetime.strptime(checkin, date_format)
                except ValueError:
                    return "Invalid date format. Please ensure the dates match the format specified."
                
                if date1 < date2: return [int(tuple(i)[0]), tuple(i)[-1]] # type: ignore
                else: continue
        else:
            if type == "s":
                tariff = 600
                result = [s_room[room_list_indexer_s], tariff]
                room_list_indexer_s += 1 
                return result
            elif type == "np":
                tariff = 400
                result = [np_room[room_list_indexer_np], tariff]
                room_list_indexer_np += 1
                return result

    def gstChecker(bill):
        if bill > 7500: return 0.18
        else: return 0.12

    def createBooking(date_format="%Y-%m-%d"):
        """
        This function creates a booking for a customer by taking their name, address, age, gender, check-in and check-out dates, service preference, and room preference. 
        It then inserts the customer details into the customer table and the booking details into the booking table in the database. 
        If an error occurs during the insertion due to access denial or integrity constraints, appropriate error messages are displayed. 
        After successful insertion, the changes are committed to the database. 
        """
        cursor.execute("SELECT * FROM room")
        try:
            print("Enter '!END' to exit anytime !")
            name:str = str(input(Fore.CYAN + "Enter Name: "))
            if name == "!END": raise EndCode
            address:str = str(input("Enter Address: "))
            if address == "!END": raise EndCode
            age:int = int(input("Enter Age (!END doesn't work): "))
            gender:str = str(input("Gender (M/F): "))
            if gender == "!END": raise EndCode
            if gender not in ["M", "m", "F", "f"]: raise GenderInputException
        
            print(Fore.BLUE + "Check-in Format:-")
            date: int = int(input(Fore.LIGHTBLUE_EX + "Date: "))
            if date > 31: raise DateLimitExceedError
            month: int = int(input("Month: "))
            if month > 12: raise MonthLimitExceedError
            year: int = int(input("Year: "))
            chc1i = f"{year}-{month}-{date}"
            checkin = datetime.strptime(chc1i, date_format)
            
            print(Fore.BLUE + "Check-out Format:-")
            date: int = int(input(Fore.LIGHTBLUE_EX + "Date: "))
            if date > 31: raise DateLimitCheckError
            month: int = int(input("Month: "))
            if month > 12: raise MonthLimitExceedError
            year: int = int(input("Year: "))
            chc2o = f"{year}-{month}-{date}"
            checkout = datetime.strptime(chc2o, date_format)
            
            if checkout >= checkin: pass
            else: raise DateLimitCheckError
            
            
            service:int = int(input(Fore.CYAN + "Enter Service (3001(catering), 3002(full), 3003(evening stay), 3004(None)): "))
            type:str = str(input("Room preference (np = 'Normal', s = 'super'): "))
            print(Style.RESET_ALL, end="")

            extractor = checkAvailableRoom(chc1i, type=type)

            room_id = int(list(extractor)[0]) # type: ignore
            tariff = 1000

            if type == "s": discount = 10
            else: discount = 0
            
        except EndCode:
            print(Fore.RED + "[END] __main__.createBooking() stopped")
        
        except TypeError:
            print(Fore.RED + "[ERROR] Invalid Input. Please try again.")

        except ValueError:
            print(Fore.RED + '[ERROR] Invalid date format. Please ensure the dates match the format specified')

        except mysql.connector.errors.InterfaceError:
            print(Fore.RED + "[ERROR] Database connection failed. Please try again.")
        
        except GenderInputException:
            print(Fore.RED + "Enter the Correct Gender")
            
        except DateLimitExceedError:
            print(Fore.RED + f"{date} Date Limits should be bound to 31")
        
        except MonthLimitExceedError:
            print(Fore.RED + f"{month} Month Limits should be bount to 12")
        
        except DateLimitCheckError:
            print(Fore.RED + "Check-in date cannot be greater than check-out date")

        finally:
            print(Style.RESET_ALL, end="")

        try:
            sql_customerTable = f"INSERT INTO customer (c_id, c_name, address, age, gender, checkin, checkout) VALUES ({c_id}, '{name}', '{address}', {age}, '{gender}', '{checkin}', '{checkout}')"
            sql_bookingTable = f"INSERT INTO booking (book_id, guest_id, room_id, tariff, service, discount) VALUES ({book_id}, {c_id}, {room_id}, {tariff}, {service}, '{discount}')"
            cursor.execute(sql_customerTable)
            cursor.execute(sql_bookingTable)            
            print(Fore.GREEN + f"[SUCCESS] Booking successful for customer") # type:ignore
            
        except mysql.connector.errors.ProgrammingError:
            print("[404] ACCESS DENIED !!")
            
        except mysql.connector.errors.IntegrityError:
            cursor.execute("SELECT c_id FROM customer")
            data = cursor.fetchall()
            last_book = int(tuple(data[-1])[0]) # type: ignore
            new_book = last_book + 4000
            sql_customerTable = f"INSERT INTO customer (c_id, c_name, address, age, gender, checkin, checkout) VALUES ({last_book + 1}, '{name}', '{address}', {age}, '{gender}', '{checkin}', '{checkout}')"
            sql_bookingTable = f"INSERT INTO booking (book_id, guest_id, room_id, tariff, service, discount) VALUES ({new_book + 1}, {last_book + 1}, {room_id}, {tariff}, {service}, '{discount}')"
            cursor.execute(sql_customerTable)
            cursor.execute(sql_bookingTable)
            print(Fore.GREEN + f"[SUCCESS] Booking successful for customer") # type:ignore
            
        except UnboundLocalError:
            print(Fore.RED + "[ERROR] can't access some variables")
        
        finally:
            print(Style.RESET_ALL, end="")
            
        
        conn.commit()


    def getBill():  
        """
        Prompt the user to enter the ID of a customer, retrieve the bill amount associated with the customer ID, calculate the final bill amount including GST, and print the bill details in a proper format.
        """
        id:str = str(input("[FETCH] Enter the ID of customer: "))

        try:

            query1 = f"SELECT * FROM bill WHERE `customer id`={id}"
            cursor.execute(query1)
            customer = cursor.fetchone()
            bill = int(list(customer)[-1]) # type: ignore
            query2= f"SELECT * FROM customer WHERE `c_id`={id}"
            query3 = f"SELECT tariff FROM av_room WHERE `room id`={tuple(customer)[2]}" # type: ignore
            query4= f"SELECT `service package` FROM customer_list WHERE `customer id`={id}"

            gst = gstChecker(bill)
            bill = bill + bill * gst

            cursor.execute(query2)
            CID=cursor.fetchone()

            cursor.execute(query3)
            av_room = cursor.fetchone()

            cursor.execute(query4)
            c_list=cursor.fetchone()

            customer += (bill,) # type: ignore
            
            # Calculate the final bill amount including GST
            # Print the bill in a proper format
            print(Fore.CYAN +"-----------------------------------")
            print("Hotel Shahi Rajdarbar Bill".upper())
            print("-----------------------------------")
            print(f"Customer ID: {id}")
            print(f"Name: {tuple(customer)[1]}")
            print(f"Address: {tuple(CID)[2]}") # type: ignore
            gen = tuple(CID)[5] # type: ignore
            if gen in ["M", "m"]: gen = "Male"
            else: gen = "Female"
            print(f"Gender: {gen}") # type: ignore
            print(f"Check-in Date: {tuple(CID)[3]}") # type: ignore
            print(f"Check-out Date: {tuple(CID)[4]}") # type: ignore
            print(f"Room ID: {tuple(customer)[2]}")
            print(f"Tariff: {tuple(av_room)[0]}") # type: ignore
            print(f"Service: {tuple(c_list)[0]}") # type: ignore
            print(f"Discount: {tuple(customer)[7]}%")
            print("-----------------------------------")
            print(f"Subtotal: Rs. {bill - bill * (tuple(customer)[7]/100)}") # type: ignore
            print(f"GST ({gst*100}%): Rs. {bill * gst}")
            print("-----------------------------------")
            print(f"Total Bill: Rs. {bill}")
            print("-----------------------------------")
            print(Style.RESET_ALL, end="")

        except TypeError as e:
            print(Fore.RED + "Customer ID does not exist.")
            print(Style.RESET_ALL, end="")


    def getAllCustomers(date_format="%Y-%m-%d"):
        """
        Retrieves all customers from the 'customer' table and their corresponding bills.
        For each customer, the function retrieves the 'payable' value from the 'bill' table
        based on the customer's 'customer id'. The 'payable' value is then modified by
        applying the GST (Goods and Services Tax) using the 'gstChecker' function.
        The modified 'payable' value is appended to the customer's tuple and printed.

        Parameters:
            None

        Returns:
            None
        """
        cursor.execute("SELECT * FROM customer")
        data = cursor.fetchall()
        
        cursor.execute("SELECT checkin, checkout FROM customer")
        dates = cursor.fetchall()
        if data == []:
            print(Fore.GREEN + "No customers found.")
            print(Style.RESET_ALL, end="")
        else:
            c = 1
            for i in data:
                try:
                    cursor.execute(f"SELECT checkin, checkout FROM customer WHERE c_id = {1000+c}")
                    dates = cursor.fetchone()
                    checkindate = str(tuple(dates)[0])
                    checkoutdate = str(tuple(dates)[1])
                    c_id = tuple(i)[0]
                    query = f"SELECT `payable` FROM bill WHERE `customer id`={c_id}"
                    cursor.execute(query)
                    price = float(tuple(cursor.fetchone())[0]) # type: ignore
                    gst = gstChecker(price)
                    price = price + price * gst
                    i = tuple(i) + (price,)
                    print(Fore.RED + f"------------Customer List {1000+c}------------")
                    print(Fore.CYAN, end="")
                    print("Customer ID: " + str(i[0]))
                    print("Customer Name: " + str(i[1]))
                    print("Age: " + str(i[6]))
                    gen = str(i[5])
                    if gen in ["M", "m"]: gen = "Male"
                    else: gen = "Female"
                    print("Gender: " + gen)
                    print("Address: " + str(i[2]))
                    # dt = datetime.strptime(str(i[4]), date_format)
                    print("Check In Date: " + checkindate) # type: ignore
                    # del dt
                    # dt = datetime.strptime(str(i[5]), date_format)
                    print("Check Out Date: " + checkoutdate) # type: ignore
                    print("Total Payable Amount: " + str(i[8]))
                    print(Fore.RED + f"-------------------------------------------")
                except:
                    c += 1
                    cursor.execute(f"SELECT checkin, checkout FROM customer WHERE c_id = {1000+c}")
                    dates = cursor.fetchone()
                    checkindate = str(tuple(dates)[0])
                    checkoutdate = str(tuple(dates)[1])
                    c_id = tuple(i)[0]
                    query = f"SELECT `payable` FROM bill WHERE `customer id`={c_id}"
                    cursor.execute(query)
                    price = float(tuple(cursor.fetchone())[0]) # type: ignore
                    gst = gstChecker(price)
                    price = price + price * gst
                    i = tuple(i) + (price,)
                    print(Fore.RED + f"------------Customer List {1000+c}------------")
                    print(Fore.CYAN, end="")
                    print("Customer ID: " + str(i[0]))
                    print("Customer Name: " + str(i[1]))
                    print("Age: " + str(i[6]))
                    gen = str(i[5])
                    if gen in ["M", "m"]: gen = "Male"
                    else: gen = "Female"
                    print("Gender: " + gen)
                    print("Address: " + str(i[2]))
                    print("Check In Date: " + checkindate) # type: ignore
                    # del dt
                    # dt = datetime.strptime(str(i[5]), date_format)
                    print("Check Out Date: " + checkoutdate) # type: ignore
                    print("Total Payable Amount: " + str(i[8]))
                    print(Fore.RED + f"------------------------------------------")
                print(Style.RESET_ALL, end="")
                c += 1

    def updateStay(c_id, newDate, date_format="%Y-%m-%d"):
        """
        A function that updates the checkout date of a customer in the database.
        
        Parameters:
            c_id (int): The customer ID.
            newDate (str): The new checkout date in the format specified by date_format.
            date_format (str, Optional): The format of the newDate string (default is "%Y-%m-%d").
        
        Returns:
            None
        """
        date = datetime.strptime(newDate, date_format)
        query = f"UPDATE customer SET checkout='{date}' WHERE c_id={c_id}"
        cursor.execute(query)
        conn.commit()
        
        print(Fore.GREEN + f"[SUCCESS] Stay of customer {c_id} has successfully been changed to {date}")
        print(Style.RESET_ALL, end="")


    def getBookingForDay(date, date_format="%Y-%m-%d"):
        """
        Retrieves all bookings and customers for a specific day from the database.

        Args:
            date (str): The date for which bookings are to be retrieved, in the format '%Y-%m-%d'.
            date_format (str, optional): The format of the 'date' parameter. Defaults to '%Y-%m-%d'.

        Returns:
            None: This function does not return anything. Instead, it prints the fetched data to the console.
        """
        date = (str(datetime.strptime(date, date_format)))[0:10]
        query = f"SELECT * FROM booking, customer WHERE customer.c_id=booking.guest_id AND customer.checkin='{date}'"
        cursor.execute(query)
        data = cursor.fetchall()
        if data == []:
            print(Fore.GREEN + "No bookings found for the given date.")
            print(Style.RESET_ALL, end="")
        else:
            cid = 1
            print(Fore.LIGHTMAGENTA_EX,end='')
            for i in data:
                cursor.execute(f"SELECT checkin, checkout FROM customer WHERE c_id={1000+cid}")
                data = cursor.fetchone()
                if data == []:
                    cid += 1
                    continue
                else:
                    print(Fore.RED + "------------------------------------------------")
                    print(Fore.CYAN + "Booking ID: " + str(tuple(i)[0]))
                    print("Guest ID: " + str(tuple(i)[1]))
                    print("Customer Name: " + str(tuple(i)[7]))
                    print("Address: " + str(tuple(i)[8]))
                    gen = str(tuple(i)[11])
                    if gen in ["M", "m"]: gen = "Male"
                    else: "Female"
                    print("Gender: " + gen)
                    print("Age: " + str(tuple(i)[12]))
                    print("Room ID: " + str(tuple(i)[2]))
                    print("Booking Tariff: " + str(tuple(i)[3]))
                    print("Service ID: " + str(tuple(i)[4]))
                    print("Check In: " + str(tuple(data)[0]))
                    print("Check Out: " + str(tuple(data)[1]))
                    print(Fore.RED + "------------------------------------------------")
            print(Style.RESET_ALL, end="")


    def getBookingBetweenDays(start_date, end_date, date_format="%Y-%m-%d"):
        """
        Retrieves all bookings and customers for a specific date range from the database.

        Args:
            start_date (str): The start date of the date range, in the format '%Y-%m-%d'.
            end_date (str): The end date of the date range, in the format '%Y-%m-%d'.
            date_format (str, optional): The format of the date parameters. Defaults to '%Y-%m-%d'.

        Returns:
            None: This function does not return anything. Instead, it prints the fetched data to the console.
        """
        start_date = (str(datetime.strptime(start_date, date_format)))[0:10]
        end_date = (str(datetime.strptime(end_date, date_format)))[0:10]
        query = f"SELECT * FROM booking, customer WHERE customer.c_id=booking.guest_id AND customer.checkin BETWEEN '{start_date}' AND '{end_date}'"
        cursor.execute(query)
        data = cursor.fetchall()
        if data == []:
            print(Fore.GREEN + "No bookings found between the given dates.")
            print(Style.RESET_ALL, end="")
        else:
            print(Fore.LIGHTMAGENTA_EX, end='')
            c = 1
            for i in data:
                cursor.execute(f"SELECT checkin, checkout FROM customer WHERE c_id={1000+c}")
                data = cursor.fetchone()
                if data == []:
                    c += 1
                    continue
                else:
                    print(Fore.RED + "------------------------------------------------")
                    print(Fore.CYAN + "Booking ID: " + str(tuple(i)[0]))
                    print("Guest ID: " + str(tuple(i)[1]))
                    print("Customer Name: " + str(tuple(i)[7]))
                    print("Address: " + str(tuple(i)[8]))
                    gen = str(tuple(i)[11])
                    if gen in ["M", "m"]: gen = "Male"
                    else: "Female"
                    print("Gender: " + gen)
                    print("Age: " + str(tuple(i)[12]))
                    print("Room ID: " + str(tuple(i)[2]))
                    print("Booking Tariff: " + str(tuple(i)[3]))
                    print("Service ID: " + str(tuple(i)[4]))
                    print("Check In: " + str(tuple(data)[0]))
                    print("Check Out: " + str(tuple(data)[1]))
                    print(Fore.RED + "------------------------------------------------")
               
               
            print(Style.RESET_ALL, end="")


    def truncateAllRecords():
        """
        Truncates all records in the 'customer' and 'booking' tables after disabling foreign key checks and safe updates.
        """
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        cursor.execute("SET SQL_SAFE_UPDATES = 0")
        cursor.execute("TRUNCATE TABLE customer")
        conn.commit()
        cursor.execute("TRUNCATE TABLE booking")
        conn.commit()
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
        cursor.execute("SET SQL_SAFE_UPDATES = 1")
        conn.commit()
        print(Fore.GREEN + "[SUCCESS] All records are cleared")
        print(Style.RESET_ALL, end="")
        
    def deleteCustomerByID():
        """
        Deletes a customer from the database by their customer ID.

        Returns:
            None
        """
        global room_list_indexer_np
        global room_list_indexer_s
        c_id = int(input("Enter customer ID: "))
        query = f"DELETE FROM customer WHERE c_id={c_id}"
        cursor.execute(query)
        conn.commit()
        query = f"DELETE FROM booking WHERE guest_id={c_id}"
        cursor.execute(query)
        conn.commit()
        room_list_indexer_s -= 1
        room_list_indexer_np -= 1
        
    def plotGraphOfBookingsOnDates(list_t: list, date_format="%Y-%m-%d"):
        x = list_t
        y = []
        c = 0
        for i in list_t:
            cursor.execute(f"SELECT * FROM customer WHERE checkin={i}")
            a = len(cursor.fetchall())
            y.append(a)
            
        plt.bar(x, y)
        plt.show()


    def Menu():
        """
        Display a menu of options and prompt the user to choose one.

        Returns:
            int: The user's choice as an integer.

        Raises:
            ValueError: If the user's input is not a valid integer.
        """
        print("---------------------HOTEL SHAHI RAJDARBAR---------------------")
        print("1) Create Booking")
        print("2) Get Bill of a Customer")
        print("3) Get All Customers")
        print("4) Update Stay")
        print("5) Get Booking for a day")
        print("6) Get Bookings between two dates")
        print("7) Clear All Records")
        print("8) Delete Booking")
        print("9) Exit")
        print("=============================================================")
        try:
            choice = int(input("Enter your choice: "))
            print("=============================================================")
            return choice
        except ValueError as e:
            print(Fore.RED + "Invalid input. Please enter an integer.")
            print(Style.RESET_ALL, end="")
            print("=============================================================")
            return Menu()
    

    while True:
        choice = Menu()

        if choice == 1:
            createBooking()
            c_id += 1
            book_id += 1
        elif choice == 2:
            getBill()
        elif choice == 3:
            getAllCustomers()
        elif choice == 4:
            c_id = int(input("Enter customer ID: "))
            newDate = str(input("Enter new date: "))
            updateStay(c_id, newDate)
        elif choice == 5:
            date = str(input(Fore.BLUE + "Enter date: ")); print(Style.RESET_ALL, end="")
            getBookingForDay(date)
        elif choice == 6:
            start_date = str(input(Fore.BLUE + "Enter start date: "))
            if start_date == "!END": print(Style.RESET_ALL, end=""); continue
            end_date = str(input("Enter end date: "))
            if end_date == "!END": print(Style.RESET_ALL, end=""); continue
            print(Style.RESET_ALL, end="")
            getBookingBetweenDays(start_date, end_date)
        elif choice == 7:
            truncateAllRecords()
        elif choice == 8:
            deleteCustomerByID()
        elif choice == 9:
            conn.close()
            break
        elif choice == 10:
            plotGraphOfBookingsOnDates(["2024-01-01", "2024-01-05"])
        else:
            print("Invalid choice")
        

except TypeError as e: print(Fore.RED + "An error occured when opening database") 
except NameError as e: print(Fore.RED + "Conenction wouldn't be created with wrong password or username")  
except KeyboardInterrupt: print(Fore.RED + "\nProgram interrupted by user")

finally: print(Style.RESET_ALL, end="")
