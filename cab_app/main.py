from models import *
from datetime import datetime,timezone
import json

destinations = ["DELHI", "JAIPUR"]
times = ["MORNING","AFTERNOON","EVENING","NIGHT"]

def load_cabs():
    try:
        with open("data/cabs.json", "r") as file:
            data = json.load(file)
        #print(data)
        return [Cab(**cab) for cab in data]

    except FileNotFoundError:
        print("No cabs available")
        return []

    except (json.JSONDecodeError, KeyError, TypeError) as e:
        print(f"Broken File: {e}")
        return []


def load_requests():
    try:
        with open("data/requests.json", "r") as file:
            data = json.load(file)
        #print(data)
        return [RideRequests(**{**req,"req_time":datetime.fromisoformat(req["req_time"])}) for req in data]

    except FileNotFoundError:
        print("No previous requests found.")
        return []

    except (json.JSONDecodeError, KeyError, TypeError) as e:
        print(f"Broken File: {e}")
        return []

cabs = load_cabs()
requests = load_requests()

def save_data():
    with open("data/cabs.json", "w") as file:
        json.dump([
        {
            "driver": cab.driver,
            "seats": cab.seats,
            "destination": cab.destination,
            "pickup_time": cab.pickup_time,
            "has_left": cab.has_left,
            "passengers": cab.passengers
        }
        for cab in cabs],file,indent = 4)

    with open("data/requests.json", "w") as file:
        json.dump([
        {
            "name": req.name,
            "destination": req.destination,
            "pickup_time": req.pickup_time,
            "year": req.year,
            "sequence": req.sequence,
            "status": req.status,
            "req_time": req.req_time.isoformat()
        }
        for req in requests
        ], file, indent=4)



def create_request():
    pass

def display():
    #print(cabs)
    #print(requests) 
    for cab in cabs:
        print(cab)

    for request in requests:
        print(request)



def main():
    while True:
        print("\n========== LITE CABS ==========")
        print("1. Add a new ride request")
        print("2. View waiting requests and all cabs")
        print("3. Quit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            create_request()

        elif choice == "2":
            display()

        elif choice == "3":
            print("Sayonara Bitches")
            #save_data()
            break

        else:
            print("Invalid choice. Please select 1, 2 or 3.")


if __name__ == "__main__":
    main()