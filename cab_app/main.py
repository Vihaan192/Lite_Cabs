from models import *
from datetime import datetime,timezone
import json
import heapq


destinations = ["DELHI", "JAIPUR"]
times = ["MORNING","AFTERNOON","EVENING","NIGHT"]

save_flag = True;

def load_cabs():
    global save_flag
    try:
        with open("data/cabs.json", "r") as file:
            data = json.load(file)
        #print(data)
        return [Cab(**cab) for cab in data]

    except FileNotFoundError:
        print("No cabs available")
        return []

    except Exception as e:
        print(f"Broken File: {e}")
        save_flag = False;
        return []


def load_requests():
    global save_flag
    try:
        with open("data/requests.json", "r") as file:
            data = json.load(file)
        #print(data)
        return [RideRequests(**{**req,"req_time":datetime.fromisoformat(req["req_time"])}) for req in data]

    except FileNotFoundError:
        print("No previous requests found.")
        return []

    except Exception as e:
        print(f"Broken File: {e}")
        save_flag = False;
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
            "bits_id": req.bits_id,
            "destination": req.destination,
            "pickup_time": req.pickup_time,
            "year": req.year,
            "status": req.status,
            "req_time": req.req_time.isoformat()
        }
        for req in requests
        ], file, indent=4)


def create_request():
    name = input("Enter student name: ").strip()

    while not name:
        print("Name cannot be empty.")
        name = input("Enter student name: ").strip()

    bits_id = input("Enter student BITS id: ").strip()
    
    while not bits_id:
        print("Bits ID cannot be empty.")
        bits_id = input("Enter student ID: ").strip()

    destination = input("Enter destination (Delhi/Jaipur): ").strip().upper()

    while destination not in destinations:
        print("Invalid destination.")
        destination = input("Enter destination (Delhi/Jaipur): ").strip().upper()

    pickup_time = input("Enter pickup time (Morning/Afternoon/Evening/Night): ").strip().upper()

    while pickup_time not in times:
        print("Invalid pickup time.")
        pickup_time = input("Enter pickup time (Morning/Afternoon/Evening/Night): ").strip().upper()

    while True:
        try:
            year = int(input("Enter your year (1-5): "))
            if 1 <= year <= 5:
                break
            print("Year must be between 1 and 5.")
        except:
            print("Please enter a valid number.")

    new_request = RideRequests(
        name=name,
        bits_id = bits_id,
        destination=destination.title(),
        pickup_time=pickup_time.title(),
        year=year,
        status="WAITING",
        req_time=datetime.now(timezone.utc)
    )

    requests.append(new_request)

    print("Ride request successfully created")

def display():
    #print(cabs)
    #print(requests) 

    print("============= Cabs =====================")
    for cab in cabs:
        print(cab)
    print("==========================================")

    print("==========Requests (waiting) ===================")
    for request in requests:
        if request.status != "FULFILLED":
            print(request)

    print("================================================")

def find_matches():
    waitlist = [req for req in requests if req.status == "WAITING"]
    cab_groups = {}
    for cab in cabs:
        if not cab.has_left and len(cab.passengers) < cab.seats:
            key = (cab.destination,cab.pickup_time)
            if key not in cab_groups:
                cab_groups[key] = []

            cab_groups[key].append({
                "cab": cab,
                "seats": cab.seats - len(cab.passengers),
                "passengers": []
            })

    waitlist.sort(key = lambda req:(-req.year,req.req_time))
    unassigned = []
    for req in waitlist:
        #print(req)
        key = (req.destination,req.pickup_time)
        cab_match = cab_groups.get(key,[])
        if cab_match == []:
            print(req)
            unassigned.append((req.name,req.bits_id))
            print(unassigned)
        assigned = False
        for match in cab_match:
            if match["seats"]>0:
                match["passengers"].append((req.name,req.bits_id))
                match["seats"]-=1
                assigned = True
                break

        if not assigned:
            unassigned.append((req.bits_id,req.name))

    print("\n========== MATCHING PREVIEW ==========")

    for group in cab_groups.values():
        for match in group:
            if not match["passengers"]:
                continue

            cab = match["cab"]

            print(f"\nDriver: {cab.driver}")
            print(f"Destination: {cab.destination}")
            print(f"Pickup: {cab.pickup_time}")
            print(f"Passengers ({len(match['passengers'])}/{cab.seats}):")

            for bits_id, name in match["passengers"]:
                print(f"  {bits_id} - {name}")

    print("\n========== UNASSIGNED REQUESTS ==========")

    if not unassigned:
        print("All done")
    else:
        for bits_id, name in unassigned:
            print(f"{bits_id} - {name}")
        
def show_cabs():
    if not cabs:
        print("No cabs available.")
        return

    print("\n========== CAB DETAILS ==========")

    for cab in cabs:
        print(cab)

    print("\n=================================")

def build_priority_queues():
    queues = {}

    for index, req in enumerate(requests):
        if req.status != "WAITING":
            continue

        key = (req.destination, req.pickup_time)

        if key not in queues:
            queues[key] = []

        heapq.heappush(queues[key],(-req.year, req.req_time, index, req)) #index for worst case tiebreaker)

    return queues

def dispatch():
    open_cabs = [cab for cab in cabs if not cab.has_left and len(cab.passengers) < cab.seats]

    if not open_cabs:
        print("No available cabs.")
        return
    
    print("\nAvailable Cabs:")

    for i, cab in enumerate(open_cabs, start=1):
        print(f"{i}. {cab.driver} ,"f"{cab.destination} , {cab.pickup_time} , "f"{len(cab.passengers)}/{cab.seats} seats occupied")

    while True:
        try:
            choice = int(input("\nSelect a cab (0 to cancel): "))

            if choice == 0:
                return

            if 1 <= choice <= len(open_cabs):
                break

            print("Invalid choice.")

        except:
            print("Enter a valid number.")

    cab = open_cabs[choice - 1]

    queues = build_priority_queues()
    key = (cab.destination, cab.pickup_time)
    queue = queues.get(key)

    if not queue:
        print("No students waiting for this trip.")
        return

    available_seats = cab.seats - len(cab.passengers)
    while queue and available_seats > 0:
        _, _, _, req = heapq.heappop(queue)
        cab.passengers.append((req.name,req.bits_id))
        req.status = "FULFILLED"
        available_seats -= 1

    cab.has_left = True
    print("Selected cab dispatch success")
    print(f'Passengers - {cab.passengers}')
    print(f"\nSeats occupied: {len(cab.passengers)}/{cab.seats}")

def main():
    while True:
        print("\n========== LITE CABS ==========")
        print("1. Add a new ride request")
        print("2. View waiting requests and all cabs")
        print("3. Find matches (preview)")
        print("4. Show cabs")
        print("5. Dispatch Cabs")
        print("6. Quit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            create_request()

        elif choice == "2":
            display()

        elif choice == "3":
            find_matches()

        elif choice == "4":
            show_cabs()

        elif choice == "5":
            dispatch()

        elif choice == "6":
            print("Sayonara Bitches")
            if save_flag:
                save_data()
            break
        
        else:
            print("Invalid choice. Please select 1, 2 ,3,4,5,6")


if __name__ == "__main__":
    main()