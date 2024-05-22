import sqlparse
from django.db import connections
from django.shortcuts import render,redirect
from AppName.utils import Functoins as f
from AppName.utils import togetAIanswer as ai
from AppName.utils import addingdatabase as ad


#the following is for getting .sql file and data from user
def upload_sql(request):
    if request.method == 'POST' and request.FILES['sql_file']:
        sql_file = request.FILES['sql_file']
        
        # Delete all existing tables in temp_db
        with connections['temp_db'].cursor() as cursor:
            cursor.execute("SHOW TABLES;")
            existing_tables = cursor.fetchall()

            for table in existing_tables:
                cursor.execute(f"DROP TABLE IF EXISTS {table[0]};")

        # Read and parse SQL file
        queries = sqlparse.split(sql_file.read().decode('utf-8'))

        # Create temporary database
        with connections['temp_db'].cursor() as cursor:
            for query in queries:
                cursor.execute(query)

        #get the database name
        selected_database=''
        with connections['temp_db'].cursor() as cursor:
            cursor.execute("SELECT DATABASE()")
            selected_database = cursor.fetchone()[0]
        
        request.session['current_database'] = selected_database
        
        return redirect('dat')
    return redirect('midl')


# Create your views here.
def home(request):
    return render(request,'home.html')
def contact(request):
    return render(request,'contact.html')
def guide(request):
    return render(request,'guide.html')
def mid(request):
    All_database_name=ad.getAllDatabaseName()
    return render(request,'mid.html',{"AllDatabaseNames":All_database_name})
    
def set_preference(request):
    if request.method == 'POST':
        if 'select_database' in request.POST:
            selected_database=request.POST.get('database_options')
            request.session['current_database'] = selected_database

    return redirect('dat')
def data(request):
    DatabaseSelected = request.session.get('current_database', 'akrity')
    #initially it shows all the tables from the database
    Tables_To_display=f.get_TableName_from_Database(DatabaseSelected)
    Display_Table_headings=[]
    Display_Table_Data=[]
    data_ofTextArea = {'textarea_field': ''}
    #this portion is for lower-left region
    if request.method == 'POST':
        if 'submit_checkboxes' in request.POST:
            # Retrieve the selected checkboxes using getlist()
            selected_options = request.POST.getlist('checkbox_options')
            Tables_To_display=selected_options
        elif 'submit_query' in request.POST:
            selected_options = request.POST.getlist('checkbox_options')
            Tables_To_display=selected_options

            text_data=request.POST.get('Query_asked')
            Query_Asked=text_data

            # process Tables_to_display and table columns
            answer=ai.getAnswer(Query_Asked,Tables_To_display,DatabaseSelected)
           
            data_ofTextArea['textarea_field'] = answer

        elif 'submit_textboxes' in request.POST:
            selected_options = request.POST.getlist('checkbox_options')
            Tables_To_display=selected_options
            
            textbox_data = request.POST.get('Query_generated')
            Query_Generated=textbox_data

            QueryTableDictionary=f.get_data_fromQuery(Query_Generated,DatabaseSelected)
            Display_Table_headings=QueryTableDictionary["TableColumnHeadings"]
            Display_Table_Data=QueryTableDictionary["TableRowData"]
            data_ofTextArea['textarea_field'] = Query_Generated
   
    #this portion is for showing the tables in lower-right region
    
    All_Data=f.Get_All_Table_Data(Tables_To_display,DatabaseSelected)

    zipped_data_all = zip(All_Data['TableNames'], All_Data['TableColumns'], All_Data['TableData'])
    
    return render(request, 'dd.html', {'TextArea_data':data_ofTextArea,'Display_table_data':Display_Table_Data,'Display_Table_head':Display_Table_headings,'zipped_data': zipped_data_all,'TablesSelected':All_Data['TableNames'],'AllTableNames': All_Data['AllTableNames']})
   
