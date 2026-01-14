
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Passenger:
    name: str
    seat_number: str
    flight_code: str

class ReservationSystem:
    def __init__(self, rows: int = 5, cols: int = 6, flight_code: str = "AK123"):
        self.rows, self.cols, self.flight_code = rows, cols, flight_code
        self.seat_map: List[List[Optional[Passenger]]] = [[None] * cols for _ in range(rows)]
        self.col_labels = [chr(ord('A') + i) for i in range(cols)]

    def _to_idx(self, seat: str) -> Optional[tuple]:
        s = seat.strip().upper()
        if len(s) < 2 or not s[:-1].isdigit(): return None
        r, c_letter = int(s[:-1]) - 1, s[-1]
        if not (0 <= r < self.rows): return None
        if c_letter not in self.col_labels: return None
        return r, self.col_labels.index(c_letter)

    def _each_seat(self):
        for r in range(self.rows):
            for c in range(self.cols):
                yield r, c, self.seat_map[r][c]

    def view_seats(self) -> None:
        print("    " + "  ".join(self.col_labels))
        print("    " + "  ".join(["—"] * self.cols))
        for r in range(self.rows):
            row_bits = ["1" if self.seat_map[r][c] else "0" for c in range(self.cols)]
            print(f"{str(r + 1).rjust(2)} | " + "  ".join(row_bits))
        print("\nLegend: 0 = available, 1 = booked\n")

    def book_seat(self, name: str, seat: str) -> bool:
        name, seat = name.strip(), seat.strip().upper()
        if not name: print("Error: Name cannot be empty."); return False
        pos = self._to_idx(seat)
        if pos is None: print("Error: Seat label is invalid."); return False
        r, c = pos
        if self.seat_map[r][c]: print(f"Sorry, seat {seat} is already booked."); return False
        self.seat_map[r][c] = Passenger(name, seat, self.flight_code)
        print(f"Booked: {name} -> {seat}")
        self.view_seats()
        return True

    def cancel_booking(self, seat: str) -> bool:
        pos = self._to_idx(seat)
        if pos is None: print("Error: Seat label is invalid."); return False
        r, c = pos
        p = self.seat_map[r][c]
        if not p: print(f"Seat {seat.strip().upper()} is not booked."); return False
        self.seat_map[r][c] = None
        print(f"Cancelled: {p.name} @ {p.seat_number}")
        self.view_seats()
        return True

    def search_passenger(self, query: str) -> List[Passenger]:
        q = query.strip().lower()
        if not q: print("Error: Search text cannot be empty."); return []
        matches = [p for _, _, p in self._each_seat() if p and q in p.name.lower()]
        if matches:
            print(f"Found {len(matches)} match(es):")
            for p in matches: print(f" - {p.name} at {p.seat_number} ({p.flight_code})")
        else:
            print(f"No passengers found matching '{query}'.")
        return matches

    def save_bookings(self, path: str = "bookings.txt") -> None:
        try:
            count = 0
            with open(path, "w", encoding="utf-8") as f:
                for _, _, p in self._each_seat():
                    if p:
                        f.write(f"{p.name}|{p.seat_number}|{p.flight_code}\n")
                        count += 1
            print(f"Saved {count} booking(s) to '{path}'.")
        except Exception as e:
            print(f"Error saving bookings: {e}")

    def load_bookings(self, path: str = "bookings.txt") -> None:
        import os
        if not os.path.exists(path): print(f"No file found at '{path}'."); return
        for r, c, _ in self._each_seat(): self.seat_map[r][c] = None
        loaded = skipped = 0
        try:
            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line: continue
                    parts = line.split("|")
                    if len(parts) != 3: skipped += 1; continue
                    name, seat, flight = parts[0].strip(), parts[1].strip().upper(), parts[2].strip()
                    pos = self._to_idx(seat)
                    if pos is None: skipped += 1; continue
                    r, c = pos
                    if self.seat_map[r][c]: skipped += 1; continue
                    self.seat_map[r][c] = Passenger(name, seat, flight); loaded += 1
            print(f"Loaded {loaded} booking(s). Skipped {skipped} line(s).")
            self.view_seats()
        except Exception as e:
            print(f"Error loading bookings: {e}")

def main():
    system = ReservationSystem(rows=5, cols=6, flight_code="AK123")
    actions = {
        "1": lambda: system.view_seats(),
        "2": lambda: system.book_seat(input("Name: ").strip(), input("Seat (e.g., 1A): ").strip()),
        "3": lambda: system.cancel_booking(input("Seat to cancel (e.g., 1A): ").strip()),
        "4": lambda: system.search_passenger(input("Search name: ").strip()),
        "5": lambda: system.save_bookings(),
        "6": lambda: system.load_bookings(),
    }
    while True:
        print("\n=== Airline Ticket Reservation System ===")
        print("1. View Seats\n2. Book a Seat\n3. Cancel a Booking\n4. Search Passenger\n5. Save Bookings\n6. Load Bookings\n0. Exit")
        choice = input("Select an option: ").strip()
        if choice == "0": print("Goodbye."); break
        action = actions.get(choice)
        print() if action else None
        action() if action else print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
