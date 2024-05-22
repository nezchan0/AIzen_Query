from AppName.utils import Functoins as f
from openai import OpenAI
import os
def askAI(Complete_System_Prompt1,Complete_System_Prompt2,User_Prompt):

    client = OpenAI(api_key=os.environ.get("API_KEY", "default_value_for_api_key"))
    response = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role":"system","content":Complete_System_Prompt1},
        {"role":"system","content":Complete_System_Prompt2},
        {"role": "user", "content":User_Prompt}
      ]
    )
    answer=response.choices[0].message.content
    return answer

def getAnswer(Query_Asked,Tables_To_display,DatabaseSelected):
   
    Table_Names =Tables_To_display
    Table_Columns=[]
   
    for i in range(len(Table_Names)):
        table_heading=f.get_table_column_name(Table_Names[i],DatabaseSelected)
        Table_Columns.append(table_heading)
    
    number_of_tables=len(Table_Names)
    table_Names_string=", ".join(Table_Names)

    detail_list=[]
    for i in range(number_of_tables):
        strin=f"'{Table_Names[i]}':{Table_Columns[i]}"
        detail_list.append(strin)
    table_details_string=", ".join(detail_list)

    System_Prompt_1="You are a MYSQL query solver. *Give me the Answer only in the form of MYSQL query, if you cannot solve or understand the Query then answer 'Cannot Comprehend'*."
    System_Prompt_2=f" I have {number_of_tables} MySQL tables."
    System_Prompt_3=f" The table names are- {table_Names_string}"
    System_Prompt_4=f". Each table details with column names are as stated- {table_details_string}"
    
    Complete_System_Prompt1=System_Prompt_1
    Complete_System_Prompt2=System_Prompt_2+System_Prompt_3+System_Prompt_4
    User_Prompt=Query_Asked

    answer=askAI(Complete_System_Prompt1,Complete_System_Prompt2,User_Prompt)
    return answer
    