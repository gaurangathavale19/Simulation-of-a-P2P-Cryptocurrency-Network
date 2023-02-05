class Event:
    def __init__(self, curr_location, type, event_data, sender_id, receiver_id, event_start_time):
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.curr_location = curr_location
        self.event_start_time = event_start_time
        self.event_data = event_data
        self.type = type

    def __lt__(self, event):
        return self.event_start_time < event.event_start_time