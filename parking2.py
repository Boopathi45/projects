from datetime import datetime,date
import json
import os
import csv
import xlsxwriter

users_data=[]
token_increment= 1
token_count= 1
total_collection= 0

if os.path.exists("parking_json.json"):
    file=open("parking_json.json","r")
    retrived_data = file.read()
    try:
        users_data = json.loads(retrived_data)
        for x in users_data:
            total_amount_collected=total_collection 
        file.close()
        for x in users_data:
            token_count+= 1
            total_amount_collected=total_collection        

    except json.decoder.JSONDecodeError as json_error:
        print()
        print("json_error")
        file=open("parking_json.json","w")
        users_data=[]

else:
    file=open("parking_json.json","w")
    user_details=json.dumps(users_data)
    file.write(user_details)

while True:

    print()
    print("1-checkin")
    print("2-checkout")
    print("3-show details")
    print("4-report")
    print("5-csv file")
    print("6-xlsx writer")
    option=input("Choose your option :")
    print()

    if option == "1":
        print("Note : 2,3 and 4 wheelers only")
        vehicle_type = int (input("vehicle type :"))
        while vehicle_type > 4 or vehicle_type < 2:
            print("please enter valid vehicle type")
            vehicle_type = int (input("vehicle type :"))
         
        if token_count == 0:
            token_number = str(vehicle_type)+"WH"+str(token_increment)
            print("Token number is :"+token_number)
        elif token_count != 0:
            token_number = str(vehicle_type)+"WH"+str(token_count)
            print("Token number is :"+token_number)

        name = input ("Enter your name :")
        vehicle_number = input ("vehicle number :")

        checkin_date = input ("Enter the date :")

        details ={ "vehicle_type":vehicle_type, "token_number":token_number, "name":name, "vehicle_number":vehicle_number, "checkin_date":checkin_date }
        users_data.append(details)
        token_increment+= 1
        token_count+=1
        
    elif option == "2":
        checkout_token = input("Enter your token number :")
        is_token_exists = False

        for record in users_data:
            if record["token_number"] == checkout_token:
                is_token_exists = True
                break
        
        if is_token_exists:
            checkout_date = input("Enter the date :")
            record.update({"checkout_date":checkout_date})
        
            exit_date = datetime.strptime(checkout_date, "%d-%m-%Y")
            entry_date = datetime.strptime(record["checkin_date"], "%d-%m-%Y")
            total_days = exit_date-entry_date
            total_duration =total_days.days

            if record["vehicle_type"] == 2:
                price = total_duration * 20
                total_collection+= price
                print( "Amount is :"+ str(price) )
                record.update({"amount":price})
            
            elif record["vehicle_type"] == 3:
                price2 = total_duration * 30
                total_collection+= price2
                print( "Amount is :"+str(price2) )
                record.update({"amount":price2})
            
            elif record["vehicle_type"] == 4:
                price3 = total_duration * 40
                total_collection+= price3
                print( "Amount is :"+ str(price3) )
                record.update({"amount":price3})
        else:
            print("Token not exists")

    elif option == "3":
        details_token = input("Enter your token :")
        is_token_exist=False

        for record in users_data:
            if record["token_number"] == details_token:
                is_token_exist=True
                break
        if is_token_exist:
            print("-----Details-----")
            for users_keys,users_values in record.items(): 
                print(users_keys ,":",users_values) 
        else:
            print("Token not exists")             

    elif option == "4":
        print("----- Report -----")
        print()
        for record in users_data:
            print(record)
        print("Total Collection Amount :"+str(total_collection))
        users_data.append({total_collection})

    
    elif option == "5":
        print("----- csv file updated -----")
        with open("parking.csv","w",newline='') as csvfile:
            fields = ['vehicle_type','token_number','name','vehicle_number','checkin_date','checkout_date','amount']
            writer = csv.DictWriter(csvfile,fieldnames=fields)
            writer.writeheader()
            writer.writerows(users_data)

    elif option == "6":
        print("------ xlsx writer updated ------")
        workbook=xlsxwriter.Workbook('boopathi.xlsx')
        worksheet=workbook.add_worksheet()
        users_info=['vehicle_type','token_number','name','vehicle_number','checkin_date','checkout_date','amount']
   
        vehicle_type_2=workbook.add_format({'bg_color':'orange','font_color': 'white'})
        vehicle_type_3=workbook.add_format({'bg_color':'white','font_color': 'black'})
        vehicle_type_4=workbook.add_format({'bg_color':'green','font_color': 'black'})
        head_align=workbook.add_format({'bg_color':'gray', 'font_size':20,'align':'center'})
        total_align=workbook.add_format({'bg_color':'gray', 'align':'center','font_size':12})

        col_calc=0
        row=1
        for col,info in enumerate(users_info):
            col_calc=col
            worksheet.write(row,col,info)

        row=2
        for user_values in users_data:
            for keys,values in user_values.items():
                col=users_info.index(keys)
                if user_values["vehicle_type"] == 2:
                    worksheet.write(row,col,values,vehicle_type_2)

                elif user_values["vehicle_type"] == 3:
                    worksheet.write(row,col,values,vehicle_type_3)

                elif user_values["vehicle_type"] == 4:
                    worksheet.write(row,col,values,vehicle_type_4)
            row+=1  
        col_value=col_calc-1

        worksheet.write(row,col_value,'Grand Total',total_align)
        worksheet.write_formula(row,col_calc,'=SUM(G3:G{})'.format(row),total_align)
        worksheet.set_column('A:G',15)
        worksheet.merge_range('A1:G1','Parking Details',head_align)
        workbook.close()

    file = open("parking_json.json","w")
    user_details =json.dumps(users_data)
    file.write(user_details)
    file.close()



