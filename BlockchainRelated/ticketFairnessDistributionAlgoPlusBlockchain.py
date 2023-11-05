import hashlib
import datetime
import random


class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        data_string = str(self.index) + str(self.timestamp) + str(self.data) + str(self.previous_hash)
        return hashlib.sha256(data_string.encode()).hexdigest()


def create_genesis_block():
    return Block(0, datetime.datetime.now(), "Genesis Block", "0")


class Blockchain:
    def __init__(self):
        self.chain = [create_genesis_block()]
        self.ticketing_system = TicketingSystem(100)  # Initialize your TicketingSystem with an acceptable range

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        new_block.previous_hash = self.get_latest_block().hash
        new_block.hash = new_block.calculate_hash()
        self.chain.append(new_block)

    def print_chain(self):
        for block in self.chain:
            print("Block Index:", block.index)
            print("Timestamp:", block.timestamp)
            print("Data:", block.data)
            print("Previous Hash:", block.previous_hash)
            print("Hash:", block.hash)
            print("--------------------")


class User:
    def __init__(self, id, arrival_time):
        self.id = id
        self.arrival_time = arrival_time
        self.queue_position = None


class Ticket:
    def __init__(self, id):
        self.id = id
        self.locked = False

    def is_locked(self):
        return self.locked

    def try_lock(self):
        if not self.locked:
            self.locked = True
            return True
        return False


class WaitingRoomService:
    def __init__(self):
        self.waiting_room = []

    def add_user(self, user):
        self.waiting_room.append(user)

    def get_waiting_room(self):
        return self.waiting_room


class QueueManagerService:
    def __init__(self, waiting_room_service, acceptable_range):
        self.waiting_room_service = waiting_room_service
        self.acceptable_range = acceptable_range

    def manage_queue(self):
        users = self.waiting_room_service.get_waiting_room()

        for user in users:
            queue_position = self.calculate_queue_position(user, users)
            user.queue_position = queue_position

    def calculate_queue_position(self, user, users):
        if not users:
            return 0
        else:
            lower_bound = max(0, len(users) - self.acceptable_range)
            return random.randint(lower_bound, len(users))


class QueueService:
    def __init__(self, waiting_room_service, tickets):
        self.waiting_room_service = waiting_room_service
        self.tickets = tickets.copy()

    def process_queue(self):
        users = sorted(self.waiting_room_service.get_waiting_room(), key=lambda user: user.queue_position)
        for user in users:
            self.attempt_purchase(user)

    def attempt_purchase(self, user):
        for ticket in self.tickets:
            if ticket.try_lock():
                print(f"User {user.id} arriving at time {user.arrival_time} purchased ticket {ticket.id}")
                self.waiting_room_service.get_waiting_room().remove(user)
                self.tickets.remove(ticket)
                break


class TicketingSystem:
    def __init__(self, acceptable_range):
        self.acceptable_range = acceptable_range
        self.waiting_room_service = WaitingRoomService()
        self.queue_manager_service = QueueManagerService(self.waiting_room_service, acceptable_range)
        self.tickets = []

    def setup_tickets(self, ticket_count):
        for i in range(ticket_count):
            self.tickets.append(Ticket(i))

    def add_user_to_waiting_room(self, user_id, arrival_time):
        user = User(user_id, arrival_time)
        self.waiting_room_service.add_user(user)
        self.queue_manager_service.manage_queue()

    def start_sale(self):
        queue_service = QueueService(self.waiting_room_service, self.tickets)
        queue_service.process_queue()


# Create a new instance of the blockchain
blockchain = Blockchain()

# Simulate a series of transactions and record them in the blockchain
blockchain.add_block(Block(1, datetime.datetime.now(), "Transactions recorded in the blockchain", ""))
blockchain.add_block(Block(2, datetime.datetime.now(), "More transactions", ""))

# Print the blockchain
blockchain.print_chain()

# Use the ticket allocation system
blockchain.ticketing_system.setup_tickets(1000)
blockchain.ticketing_system.add_user_to_waiting_room(0, 0)
blockchain.ticketing_system.start_sale()

#if __name__ == '__main__':
 #   blockchain.print_chain()
