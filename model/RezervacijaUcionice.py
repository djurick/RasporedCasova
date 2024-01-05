from .GlobalneKonstante import GlobalneKonstante

class RezervacijaUcionice:
    NR = -1
    _reservationPool = {}

    def __init__(self, day: int, time: int, room: int):
        self.Day = day
        self.Time = time
        self.Room = room

    @staticmethod
    def parse(hashCode):
        reservation = RezervacijaUcionice._reservationPool.get(hashCode)
        if reservation is None:
            day = hashCode // (GlobalneKonstante.DAY_HOURS * RezervacijaUcionice.NR)
            hashCode2 = hashCode - (day * GlobalneKonstante.DAY_HOURS * RezervacijaUcionice.NR)
            room = hashCode2 // GlobalneKonstante.DAY_HOURS
            time = hashCode2 % GlobalneKonstante.DAY_HOURS
            reservation = RezervacijaUcionice(day, time, room)
            RezervacijaUcionice._reservationPool[hashCode] = reservation
        return reservation

    @staticmethod
    def getHashCode(day: int, time: int, room: int) -> int:
            return day * RezervacijaUcionice.NR * GlobalneKonstante.DAY_HOURS + room * GlobalneKonstante.DAY_HOURS + time

    @staticmethod
    def getReservation(nr: int, day: int, time: int, room: int):
        if nr != RezervacijaUcionice.NR and nr > 0:
            RezervacijaUcionice.NR = nr
            RezervacijaUcionice._reservationPool.clear()

        hashCode = RezervacijaUcionice.getHashCode(day, time, room)
        reservation = RezervacijaUcionice.parse(hashCode)

        if reservation is None:
            reservation = RezervacijaUcionice(day, time, room)
            RezervacijaUcionice._reservationPool[hashCode] = reservation
        return reservation

    def __hash__(self) -> int:
        return RezervacijaUcionice.getHashCode(self.Day, self.Time, self.Room)


    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return hash(self) == hash(other)
            
    def __ne__(self, other):
        return not self.__eq__(other)
        
    def __str__(self):
        return "Day: " + str(self.Day) + ", " + "Room: " + str(self.Room) + ", Time: " + str(self.Time)
