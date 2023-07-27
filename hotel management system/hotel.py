
class User:
    pass

class Admin(User):
    pass

class Guest(User):
    pass

class HouseKeeper(User):
    pass

class Receptionist(User):
    pass




data_type -> view_type




class Hotel:
    id: int
    name: string
    location: Location
    rooms: []Room

class Location:
    country: Country
    pin: string
    area: string
    city: string

class Room:
    type: "Standard", "Deluxe", "Suite"
    number
    status: "Available", "Reserved", "ServiceInProgress", "Occupied", "NotAvaialble"
    price
    housekeeping_logs: []HouseKeepingLog
    keys: []RoomKey
    
class RoomKey:
    id: string
    barCode: string
    issuedAt: Date
    is_active: bool
    is_master: bool

    assign_room(room: Room)

class HouseKeepingLog:
    id
    start_time
    end_time
    housekeeper: HouseKeeper
    description: string


class Inventory:
    rooms
    bookedRooms
    availableRooms


class Booking
    pass
    