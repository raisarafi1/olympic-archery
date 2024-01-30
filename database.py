import mysql.connector


# Connect to server 
cnx = mysql.connector.connect(
    host = "127.0.0.1",
    port = 3306,
    user = "root",
    password = "Ucantcme123")

# Get a cursor 
cur = cnx.cursor()

# Execute a query 
# Will not return any value, the cursor itself will 
# Hold this value
cur.execute("SELECT CURDATE()")

# Fetch one result
# Fetches one row from return value (from execute)
# So if execute returns 10 rows from a table, fetch one will return one entry from
# That table then move to the next entry
row = cur.fetchone()
print("Current date is: {0}".format(row[0]))

# Execute a query
# The statement "use olympicarchery" allows us to not have
# To write olympicarchery.athlete when selecting athletes
cur.execute("use olympicarchery")
cur.execute("select * from athlete")

# Fetch results
col_names = cur.column_names
print("Attribute List:\n")
att_size=len(col_names)

for i in range(att_size):
    #use length of data type that you have
    print(col_names[i],'\t',end = '')
print()
print(120*'-')

print(" Attribute List:\n", col_names)
rows = cur.fetchone()
print("number of entries in table\n", len(rows))
print("Curent athlete table content:\n", rows)
# Here the first entry will be removed because of fetchone so when you fetchall the first entry is gone
rows = cur.fetchall()
# Length is the length of the list of tuples
print("number of entries in table\n", len(rows))
print("Current athlete table content:\n", rows)

# a slightly better way 
cur.execute("select * from athlete")
rows = cur.fetchall()
print("Current athlete table content:\n ")
size=len(rows)
for i in range(size):
    # This prints the tuple but needs to be formatted by respective type
    for x in range(len(rows[i])):
        print(rows[i][x], end ='\t')



# Inserting new values into table
delete_sudan = "delete from country where CName = 'Sudan'"
cur.execute(delete_sudan)
cnx.commit()
insert_country = ("insert into country "
                   "values (%s,%s,%s,%s)")
country_data = ('Sudan', '0', '0','0')
cur.execute(insert_country,country_data)
cnx.commit()

# Updating values in table 
update_country = "update country set AllTimeGold = '3' where CName = 'Sudan'"
cur.execute(update_country)
cnx.commit()



# Close connection
cnx.close()
