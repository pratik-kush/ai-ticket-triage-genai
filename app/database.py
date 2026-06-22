import json
import os
from typing import Dict, List, Optional

DATA_FILE = os.getenv("TICKET_DATA_FILE", "tickets.json")


def initialize_database() -> None:
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump([], file, indent=4)


def read_tickets() -> List[Dict]:
    initialize_database()
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        content = file.read().strip()

        if not content:
            return []
        
        return json.load(file)


def write_tickets(tickets: List[Dict]) -> None:
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(tickets, file, indent=4)


def get_next_id() -> int:
    tickets = read_tickets()
    if not tickets:
        return 1
    return max(ticket["id"] for ticket in tickets) + 1


def save_ticket(ticket: Dict) -> Dict:
    tickets = read_tickets()
    tickets.append(ticket)
    write_tickets(tickets)
    return ticket


def find_ticket_by_id(ticket_id: int) -> Optional[Dict]:
    tickets = read_tickets()
    for ticket in tickets:
        if ticket["id"] == ticket_id:
            return ticket
    return None


def update_ticket_status(ticket_id: int, status: str) -> Optional[Dict]:
    tickets = read_tickets()
    for ticket in tickets:
        if ticket["id"] == ticket_id:
            ticket["status"] = status
            write_tickets(tickets)
            return ticket
    return None


def delete_ticket(ticket_id: int) -> bool:
    tickets = read_tickets()
    updated_tickets = [ticket for ticket in tickets if ticket["id"] != ticket_id]
    if len(updated_tickets) == len(tickets):
        return False
    write_tickets(updated_tickets)
    return True
