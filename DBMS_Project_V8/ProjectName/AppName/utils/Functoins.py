import mysql.connector as m


#functionn to get the data from the query
def get_data_fromQuery(query,DatabaseSelected):
    demodb=m.connect(host="localhost",user="root",passwd="root@123",database=DatabaseSelected)
    democursor=demodb.cursor()

    Data_dit={"TableColumnHeadings":[],"TableRowData":[]}
    data=[]
    democursor.execute(query)
    column_headings = [col[0] for col in democursor.description]
    for i in democursor:
        data.append(list(i))
    Data_dit["TableColumnHeadings"]=column_headings
    Data_dit["TableRowData"]=data
    return Data_dit

#function to get data from tables
def get_data_fromTable(tablename,DatabaseSelected):
    demodb=m.connect(host="localhost",user="root",passwd="root@123",database=DatabaseSelected)
    democursor=demodb.cursor()

    Records=[]
    democursor.execute(f"select* from {tablename}")
    for j in democursor:
        Records.append(list(j))
    
    return Records


def get_table_column_name(tablename,DatabaseSelected):
    demodb=m.connect(host="localhost",user="root",passwd="root@123",database=DatabaseSelected)
    democursor=demodb.cursor()

    Table_col_name=[]
    democursor.execute(f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = '{DatabaseSelected}' AND TABLE_NAME = '{tablename}' ORDER BY ORDINAL_POSITION; ")
    for i in democursor:
        Table_col_name.append(i[0])
    return Table_col_name


def get_TableName_from_Database(DatabaseSelected):
    demodb=m.connect(host="localhost",user="root",passwd="root@123",database=DatabaseSelected)
    democursor=demodb.cursor()
    table_list=[]
    democursor.execute("show tables")
    for i in democursor:
        table_list.append(i[0])
    return table_list

def Get_All_Table_Data(Tables_selected,DatabaseSelected):
    demodb=m.connect(host="localhost",user="root",passwd="root@123",database=DatabaseSelected)
    democursor=demodb.cursor

    Data_dict={"TableNames":[],"TableColumns":[],"TableData":[],"AllTableNames":[]}

    All_Table_Names=get_TableName_from_Database(DatabaseSelected)
    Table_Names =Tables_selected
    Table_Columns=[]
    Table_Data=[]

    for i in range(len(Table_Names)):
        table_heading=get_table_column_name(Table_Names[i],DatabaseSelected)
        records=get_data_fromTable(Table_Names[i],DatabaseSelected)

        Table_Columns.append(table_heading)
        Table_Data.append(records)

    Data_dict["TableNames"]=Table_Names
    Data_dict["TableColumns"]=Table_Columns
    Data_dict["TableData"]=Table_Data
    Data_dict["AllTableNames"]=All_Table_Names

    return Data_dict