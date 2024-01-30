# Code from lines 3 - 44 retrieved from SQL-basics-tutorial

import mysql.connector

def admin_consol(cur):
    pass
def guest_view(cur):
    print("What are you looking for:")
    print("1- Event information")
    print("2- Participant information")
    print("3- Country information")
    selection = input()

    if selection == '2':
        subselection = input('Please type 1 for Athletes or 2 for Coaches:\n')
        if subselection == '1':
            athlete_info(cur)
        if subselection == '2':
            coaches_info(cur)


def format(cur):
    col_names=cur.column_names
    search_result=cur.fetchall()
    print("Search found ",len(search_result)," Entries:\n")
    header_size=len(col_names)
    for i in range(header_size):
        print("{:<30s}".format(col_names[i]),end='')
    print()
    print(30*header_size*'-')
    for row in search_result:
        for val in row:
            print("{:<30s}".format(str(val)),end='')
        print()

def searchkey_provided(cur, searchkey):
    if searchkey != None:
        instr = "select * from athlete where olympicid = %(olympicid)s"
        cur.execute(instr, {'olympicid':searchkey})
        format(cur)
        startup()
    else:
        return

def athlete_info(cur):
    instr=""
    join=""
    att_selection = input("Do you want to see the athlete's name ? Y or N: ")
    # If OLYMPICID wasn't the same name then you wouldn't be able to do a natural join
    # Instead from athlete join participant on olympicID = olympicID 
    if att_selection == 'Y':
        join = 'select * from athlete natural join PARTICIPANT'
        searchkey=input("please insert the olympicid of the athlete you are looking for (press Enter to view all): ") or None
        searchkey_provided(cur, searchkey)
        cur.execute(join)
        format(cur)
        startup()

    elif att_selection == 'N':
        searchkey=input("please insert the olympicid of the athlete you are looking for (press Enter to view all): ") or None
        searchkey_provided(cur, searchkey)
        instr="select * from athlete"
        cur.execute(instr)
        col_names=cur.column_names
        search_result=cur.fetchall()
        print("Search found ",len(search_result)," Entries:\n")
        header_size=len(col_names)
        for i in range(header_size):
            print("{:<15s}".format(col_names[i]),end='')
        print()
        print(15*header_size*'-')
        for row in search_result:
            for val in row:
                print("{:<15s}".format(str(val)),end='')
            print()
        startup()

    else:
        retrying = input("Please enter Y or N: ")
        if retrying != 'Y' or 'N':
            startup()


def coaches_info(cur):
    instr=""
    join=""
    att_selection = input("Do you want to see the Athlete name ? Y or N: ")
    if att_selection == 'Y':
        join = 'from coach naturaljoin PARTICIPANT'
    instr="select * from coach"
    searchkey=input("please insert the olympicid of the athlete you are looking for (press Enter to view all): ") or None
    cur.execute(instr)
    col_names=cur.column_names
    search_result=cur.fetchall()
    print("Search found ",len(search_result)," Entries:\n")
    header_size=len(col_names)
    for i in range(header_size):
        print("{:<15s}".format(col_names[i]),end='')
    print()
    print(15*header_size*'-')
    for row in search_result:
        for val in row:
            print("{:<15s}".format(str(val)),end='')
        print()

def insert_country(cur,cnx):
    country_name = input("Please enter the name of the country: ") or None
    delete_country_name = "delete from country where CName = %s"
    val = (country_name,)
    cur.execute(delete_country_name, val)
    gnum = input("How many gold medals do this country have (press enter and leave blank if unknown): ") or None
    snum = input("How many silver medals do this country have (press enter and leave blank if unknown): ") or None
    bnum = input("How many bronze medals do this country have (press enter and leave blank if unknown): ") or None
    insert_country = ("insert into country "
                        "values (%s,%s,%s,%s)")
    country_data = (country_name,gnum,snum,bnum)
    cur.execute(insert_country,country_data)
    cnx.commit()
    instr = "select * from country"
    cur.execute(instr)
    format(cur)
    while country_name == None:
        print("Your country needs a name!")
        country_name = input("Please enter the name of the country: ") or None
        if country_name == None:
            continue
        else:
            delete_country_name = "delete from country where CName = %s"
            val = (country_name,)
            cur.execute(delete_country_name, val)
            gnum = input("How many gold medals do this country have (press enter and leave blank if unknown): ") or None
            snum = input("How many silver medals do this country have (press enter and leave blank if unknown): ") or None
            bnum = input("How many bronze medals do this country have (press enter and leave blank if unknown): ") or None
            insert_country = ("insert into country "
                                "values (%s,%s,%s,%s)")
            country_data = (country_name,gnum,snum,bnum)
            cur.execute(insert_country,country_data)
            cnx.commit()
            instr = "select * from country"
            cur.execute(instr)
            print("Displaying results...")
            format(cur)
            startup()

def admin_consol(cur,cnx): 
    print("Which operation would you like to execute?")
    print("1-Insert")
    print("2-Delete")
    print("3-Update")
    print("4-Create Table")
    print("5-Create View")
    print("6-Alter")
    print("7-Query")
    
    selection = input("Please type 1, 2, 3, 4, 5, 6, 7, or 8 to select: ")
    if selection == '1':
        print("Which table would you like to insert your data into?")
        print("1-Country")
        print("2-Particpant")
        print("3-Athlete")
        print("4-Coach")
        print("5-Team")
        print("6-Event_Schedule")
        print("7-Individual Results")
        print("8-Team Results")
        sub_selection = input("Please type 1, 2, 3, 4, 5, 6, 7 or 8 to select: ")
        if sub_selection == '1':
            insert_country(cur,cnx)
        elif sub_selection == '2':
            oid = input("Please input the olympic ID of the participant you would like to insert: ") or None
            all_oid = 'select OlympicID from participant'
            cur.execute(all_oid)
            column_of_oid = cur.fetchall()
            for i in column_of_oid:
                if oid == i:
                    print("This olympic ID already exists...")
                    oid = input("Please enter an olympic ID that does not exist: ")      
            last_name = input("Please enter the participants last name: ")
            first_name = input("Please enter the participants first name: ")
            country_name = input("Please enter the name of the country the participant is from: ")
            all_countries = 'select cname from country'
            cur.execute(all_countries)
            names_of_countries = cur.fetchall()
            if country_name not in names_of_countries:
                print('The country you have entered is not in the country table... would you like to insert it?')
                choice = input("Please enter Y or N: ")
                if choice == 'Y':
                    insert_country(cur, cnx)
                else: 
                    country_name = input("Please enter a country that is in the country table: ")
                    participant_data = (oid,last_name,first_name,country_name)
                    insert_participant = ("insert into participant " 
                                            "values (%s,%s,%s,%s)")
                    cur.execute(insert_participant,participant_data)
                    cnx.commit()
                    instr = "select * from participant"
                    cur.execute(instr)
                    format(cur)
                    while oid == None:
                        print("Your participant needs an olympic ID!")
                        oid = input("Please enter the olympic ID: ") or None
                        if oid == None:
                            continue
                        else:
                            last_name = input("Please enter the participant's last name: ") or None
                        while last_name == None: 
                            print("Your participant needs a last name!")
                            last_name = input("Please enter the last name: ")
                            if last_name == None: 
                                continue
                            else:
                                first_name = input("Please enter the participant's first name: ") or None
                                while first_name == None: 
                                    print("Your participant needs a first name!")
                                    last_name = input("Please enter the last name: ")
                                    if last_name == None: 
                                        continue
                                    else:
                                        country_name = input("Please enter the name of the country the participant is from: ")
                                        participant_data = (oid,last_name,first_name,country_name)
                                        insert_participant = ("insert into participant values" 
                                                                "values (%s,%s,%s,%s)")
                                        cur.execute(insert_participant,participant_data)
                                        cnx.commit()
                                        instr = "select * from particpant"
                                        cur.execute(instr)
                                        print("Displaying results...")
                                        format(cur)
                                        startup()
        elif sub_selection == '3':
            oid = input("Please enter the olympic ID of the athlete you would like to insert: ")
            sex = input("Please enter the athlete's sex (M or F): ")
            year = input("Please enter the athlete's birthyear: ")
            firstgames = input("Please enter the city and year of their competition: ")
            insert_athlete = ("insert into athlete" 
                                    "values (%s,%s,%s,%s)")

            athlete_data = (oid, sex, year, firstgames)
            cur.execute(insert_athlete, athlete_data)
            cnx.commit()
            instr = "select * from athlete"
            cur.execute(instr)
            format(cur)
        elif sub_selection == '4': 
            oid = input("Please enter the olympic ID of the coach you would like to insert: ")
            orientation = input("Please enter whether their orientation is complete or pending: ")
            insert_coach = ("insert into coach "
                                "values (%s,%s)")
            coach_data = (oid, orientation)
            cur.execute(insert_coach,coach_data)
            cnx.commit()
            instr = "select * from coach"
            format(cur)
        elif sub_selection == '5': 
            tid = input("Please enter the team ID of the member you would like to insert: ") or None
            member1 = input("Please enter the first member: ")
            member2 = input("Please enter the second member: ")
            member3 = input("Please enter the third member: ")
            member4 = input("Please enter the fourth member: ")
            member5 = input("Please enter the fifth member: ")
            member6 = input("Please enter the sixth member: ")
            insert_team = ("insert into team "
                                "values (%s,%s,%s,%s,%s,%s,%s)")
            team_data = (tid, member1, member2, member3, member4, member5, member6)
            cur.execute(insert_team,team_data)
            cnx.commit()
            instr = "select * from team"
            format(cur)
        elif sub_selection == '6': 
            event_id = input("Please enter the event ID of the event you would like to insert: ") 
            event_date = input('Please enter the date of the event')
            event_location = input('Please enter the location of the event')
            insert_event = ("insert into event_schedule "
                                "values (%s,%s,%s)")
            event_data = (event_id, event_date, event_location)
            cur.execute(insert_event, event_data)
            cnx.commit()
            instr = "select * from event_schedule"
            format(cur)
        elif sub_selection == '7': 
            event_id = input("Please enter the event ID of the event you would like to insert: ") 
            olympian = input('Please enter the olympian')
            medal = input('Please enter the medal of the individual')
            insert_iresult = ("insert into individual_results "
                                "values (%s,%s,%s)")
            iresult_data = (event_id, olympian, medal)
            cur.execute(insert_iresult, iresult_data)
            cnx.commit()
            instr = "select * from individual_results"
            format(cur)
        elif sub_selection == '8': 
            event_id = input("Please enter the event ID of the event you would like to insert: ") 
            team = input('Please enter the team')
            medal = input('Please enter the medal of the team')

            insert_tresult = ("insert into team_results "
                                "values (%s,%s,%s)")
            tresult_data = (event_id, team, medal)
            cur.execute(insert_tresult, tresult_data)
            cnx.commit()
            instr = "select * from team_results"
            format(cur)
        

    elif selection == '2':
        country_name = input("Please enter the name of the country you would like to delete: ") or None
        delete_country_name = "delete from country where CName = %s"
        val = (country_name,)
        cur.execute(delete_country_name, val)
        cnx.commit()
        instr = "select * from country"
        cur.execute(instr)
        format(cur)
    elif selection == '3': 
        country_name = input("Please enter the name of the country you would like to update: ")


    
def startup():
  
    # Connect to server
    print()
    print("Welcome to the Archery Olympics Database:")
    print("In order to proceed please select your role from the list below:")
    print("1-DB Admin")
    print("2-Data Entry")
    print("3-Browse as guest")
    print("4-Exit application")

    selection = input("Please type 1, 2, 3 or 4 to select: ")

    if selection in ['1','2']:
        username= input("user name: ")
        passcode= input("password: ")
    else:
        username="guest"
        passcode=None
  
    cnx = mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        user=username,
        password= passcode)    
    # Get a cursor
    cur = cnx.cursor()
    # Execute a query
    cur.execute("use olympicarchery")


    if selection == '1':
        admin_consol(cur,cnx)
    elif selection == '2':
        admin_consol(cur,cnx)
    elif selection == '3':
        guest_view(cur)
    else:
        quit


if __name__ == "__main__":
    startup()
