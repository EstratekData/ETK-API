import requests



# Define the base URL for the API server
base_url = "http://localhost:5000"

# Define the endpoints we want to consume
time_endpoint        = base_url + "/time"
date_endpoint        = base_url + "/date"
etk_finance_endpoint = base_url + "/etk_finance"

# Send requests to the API server and print the responses
time_response = requests.get(time_endpoint)
print("Current time:", time_response.text)

date_response = requests.get(date_endpoint)
print("Current date:", date_response.text)

etk_ticker_list_response = requests.get(etk_finance_endpoint)
if etk_ticker_list_response.status_code == 200:
    print (etk_ticker_list_response.text)
    try:
        print("Lista de Tickers: ")
        print(etk_ticker_list_response.json())
    except ValueError as e:
        print("Error: Unable to decode response as JSON.")
        print("Response content:", etk_ticker_list_response.content)
else:
    print("Error: Unable to retrieve list of strings.")

