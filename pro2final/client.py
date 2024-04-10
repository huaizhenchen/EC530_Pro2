from requests import get, post, delete, put

base_url = "http://localhost:5000/datasets/"

inp = input("Enter number: \n\t1. GET a dataset \n\t2. POST a new dataset \n\t3. DELETE a dataset \n\t4. UPDATE a dataset \n\t5. Quit\n")
while inp != '5':
    match inp:
        # GET
        case '1':
            dataset_id = input("Enter Dataset ID: ")
            try:
                response = get(base_url + dataset_id)
                if response.status_code == 200:
                    print(response.json())
                else:
                    print("Failed to get dataset. Status code:", response.status_code)
            except Exception as e:
                print(f"ERROR: Failed to get dataset with ID {dataset_id}:", e)

        # POST
        case '2':
            name = input("Enter Dataset Name: ")
            description = input("Enter Dataset Description: ")
            type = input("Enter Dataset Type: ")
            creation_date = input("Enter Creation Date (YYYY-MM-DD): ")

            try:
                response = post(base_url, json={"Name": name, "Description": description, "Type": type, "CreationDate": creation_date})
                if response.status_code == 201:
                    print(response.json())
                else:
                    print("Failed to create dataset. Status code:", response.status_code)
            except Exception as e:
                print("ERROR: Failed to create dataset:", e)

        # DELETE
        case '3':
            dataset_id = input("Enter Dataset ID: ")
            try:
                response = delete(base_url + dataset_id)
                if response.status_code == 200:
                    print(response.json())
                else:
                    print("Failed to delete dataset. Status code:", response.status_code)
            except Exception as e:
                print(f"ERROR: Failed to delete dataset with ID {dataset_id}:", e)

        # UPDATE
        case '4':
            dataset_id = input("Enter Dataset ID: ")
            name = input("Enter new Dataset Name (press Enter to skip): ")
            description = input("Enter new Dataset Description (press Enter to skip): ")
            type = input("Enter new Dataset Type (press Enter to skip): ")
            creation_date = input("Enter new Creation Date (YYYY-MM-DD, press Enter to skip): ")

            update_data = {key: value for key, value in [
                ('Name', name),
                ('Description', description),
                ('Type', type),
                ('CreationDate', creation_date)
            ] if value}

            try:
                response = put(base_url + dataset_id, json=update_data)
                if response.status_code == 200:
                    print(response.json())
                else:
                    print("Failed to update dataset. Status code:", response.status_code)
            except Exception as e:
                print(f"ERROR: Failed to update dataset with ID {dataset_id}:", e)

        # DEFAULT
        case _:
            print("Invalid option, please enter a number between 1 and 5.")

    inp = input("Enter number: \n\t1. GET a dataset \n\t2. POST a new dataset \n\t3. DELETE a dataset \n\t4. UPDATE a dataset \n\t5. Quit\n")
