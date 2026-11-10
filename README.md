# Lite Cabs – Cab Pool Matcher

An introductory project to create a cab pool matcher for high passenger traffic situation , creating pools based off specified parameters of seniority and request times. 

## 1. Features

- Create ride requests with student details.
- Load existing cab and ride request data from JSON files.
- View waiting requests and available cabs.
- Preview possible passenger assignments without modifying actual data.
- Dispatch cabs while prioritising students based on seniority.
- Display cab details, including passengers, seat occupancy and departure status.
- Save application state to JSON files when exiting.
- Restore application state when restarting.

## 2. Requirements

- Python 3.14.4

The application uses Python's standard library, including:
- `json` for data persistence.
- `datetime` for recording submission timestamps.
- `heapq` for priority queue operations.

## 3. Running the Application

Navigate to the project directory:

```bash
cd cab_app
```

Run the application:

```bash
python main.py
```

The application provides an interactive command-line menu.

## 4. Matching and Dispatch Logic

### Finding Matches

The matching preview groups open cabs by destination and pickup time.

For each waiting request, the application checks whether a matching cab has available seats and assigns seats on basis of priority factors which are namely year of study and time of request creation (for ties).

The preview does not modify the actual cab objects or request statuses.

### Seniority-Based Dispatch

Dispatching follows academic seniority:

1. Students in higher academic years receive priority.
2. Students in the same academic year are prioritised by earlier submission time.
3. If submission timestamps are identical, their original request-list order is preserved.

The application uses Python's `heapq` module to implement this priority system.

Each priority queue is associated with a destination and pickup-time combination.

A heap entry has the structure:

```python
(-req.year, req.req_time, index, req)
```
max-heap implemented by using a negative sign in front of year of study.

The submission timestamp provides FIFO ordering within the same academic year.

The index acts as a final tie-breaker which is guaranteed to be unique.

### Priority Queue Generation

Priority queues are generated on the fly loading data from the json files.

Only requests with the status `WAITING` are inserted into the heaps.

The heaps themselves are not persisted because they can be reconstructed from the saved request data.

After a successful dispatch:
- Assigned students are added to the cab's passenger list.
- Their request status is changed to `FULFILLED`.
- The cab is marked as departed.
- Fulfilled requests are excluded from subsequent priority queues.

### Loading

At startup, the application reads the cab and request JSON files and reconstructs the corresponding Python objects.

Submission timestamps are converted back into `datetime` objects using `datetime.fromisoformat()`.


## 5. Time Complexity

Let:

- `N` = Number of waiting ride requests.
- `C` = Number of cabs.
- `K` = Number of passengers assigned during a dispatch.

| Operation | Time Complexity |
|---|---|
| Loading JSON data | $O(N + C)$ |
| Building priority queues using repeated `heappush` | $O(N \log N)$ |
| Extracting $K$ passengers from a heap | $O(K \log N)$ |
| Displaying all requests and cabs | $O(N + C)$ |
| Sorting requests for matching preview | $O(N \log N)$ |
| Adding $N$ ride requests | $O(N)$ |
| Finding an open cab | $O(C)$ |
| Sending one cab (including queue construction) | $O(N \log N + K \log N + C)$  ~ $O(N \log N)$ |



## 6. Design Decisions

- Ride requests remain in the request list after dispatch, with their status updated to `FULFILLED`. This preserves request history.
- Passenger assignments in the form (Name,ID) are stored separately within each cab.
- JSON was chosen because it is lightweight, human-readable and supported directly by Python.
- Data is saved when the application exits rather than after every individual operation to reduce write costs.

## 7. Task questions

- Half empty cabs are perfectly fine to leave as the program logic dispatches a cab either when its full or the queue is empty
- If there are no available cabs , no request disappear it always persists in the JSON file , even fulfilled ones.
- For students in same year , the time of request submission is taken as the tiebreaker , and if even that is the same ,an index maintained checks which request was added to the waitlist first and prioritizes that.