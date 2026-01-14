# Airline-Ticket-Reservation-System
airline_reservation


Description
This is a simple Python program that lets you book and manage airline seats. It uses a 5-row by 6-column seat layout and saves bookings to a text file so you can load them later.

Features
•	View seat map (0 = available, 1 = booked) (5 rows × 6 columns)
•	Book a seat by name and seat label (e.g., 1A)
•	Cancel a booking
•	Search passenger by name
•	Save bookings to a file
•	Load bookings from a file

Requirements
Python 3.x installed on your computer. 
How to Run
1.	Download the files (airline_reservation.py and README).
2. Open a terminal or command prompt in the folder.
3. Type: python airline_reservation.py
4. Follow the menu instructions.










File Structure
```
Airline-Ticket-Reservation-System/
│
├── airline_reservation.py   # Main program
├── bookings.txt             # Saved bookings (generated after saving)
├── README.md                # Project documentation
└── Airline_Ticket_Reservation_Report.docx  # Mandatory report
```
Notes
Seat labels range from 1A to 5F.
Bookings are saved in a text file called bookings.txt using the format: name|seat|flight.
