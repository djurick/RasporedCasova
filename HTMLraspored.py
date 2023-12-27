from model.GlobalneKonstante import GlobalneKonstante
from model.RezervacijaUcionice import RezervacijaUcionice
from collections import defaultdict


class HTMLRaspored:
    ROOM_COLUMN_NUMBER = GlobalneKonstante.DAYS_NUM + 1
    ROOM_ROW_NUMBER = GlobalneKonstante.DAY_HOURS + 1
    COLOR1 = "#319378"
    COLOR2 = "#CE0000"
    CRITERIAS = ('R', 'S', 'L', 'P', 'G')
    OK_DESCR = ("Current room has no overlapping", "Current room has enough seats",
                       "Current room with enough computers if they are required",
                       "Professors have no overlapping classes", "Student groups has no overlapping classes")
    FAIL_DESCR = ("Current room has overlapping", "Current room has not enough seats",
                       "Current room with not enough computers if they are required",
                       "Professors have overlapping classes", "Student groups has overlapping classes")
    PERIODS = (
                "08:00 - 08:30","08:30 - 09:00", "09:00 - 09:30", "09:30 - 10:00", "10:00 - 10:30", 
                  "10:30 - 11:00", "11:00 - 11:30", "11:30 - 12:00","12:00 - 12:30", "12:30 - 13:00", 
                  "13:00 - 13:30", "13:30 - 14:00", "14:00 - 14:30", "14:30 - 15:00","15:00 - 15:30", 
                  "15:30 - 16:00","16:00 - 16:30","16:30 - 17:00", "17:00 - 17:30", "17:30 - 18:00",
                  "18:00 - 18:30", "18:30 - 19:00", "19:00 - 19:30", "19:30 - 20:00"
                )
    WEEK_DAYS = ("PONEDELJAK", "UTORAK", "SREDA", "CETVRTAK", "PETAK", "SUBOTA")

    @staticmethod
    def getCourseClass(cc, criterias, ci):
        COLOR1 = HTMLRaspored.COLOR1
        COLOR2 = HTMLRaspored.COLOR2
        CRITERIAS = HTMLRaspored.CRITERIAS
        length_CRITERIAS = len(CRITERIAS)

        sb = [cc.Course.Name, "<br />", cc.Professor.Name, "<br />", "/".join(map(lambda grp: grp.Name, cc.Groups)),
                  "<br />"]
        if cc.LabRequired:
            sb.append("Racunarska ucionica <br />")

        for i in range(length_CRITERIAS):
            sb.append("<span style='color:")
            if criterias[ci + i]:
                sb.append(COLOR1)
                sb.append("' title='")
                sb.append(HTMLRaspored.OK_DESCR[i])
            else:
                sb.append(COLOR2)
                sb.append("' title='")
                sb.append(HTMLRaspored.FAIL_DESCR[i])
            sb.append("'> ")
            sb.append(CRITERIAS[i])
            sb.append(" </span>")

        return sb

    @staticmethod
    def generateTimeTable(solution, slot_table):
        ci = 0

        time_table = defaultdict(list)
        items = solution.classes.items        
        ROOM_COLUMN_NUMBER = HTMLRaspored.ROOM_COLUMN_NUMBER
        getCourseClass = HTMLRaspored.getCourseClass

        for cc, reservation_index in items():
            reservation = RezervacijaUcionice.parse(reservation_index)
            dayId = reservation.Day + 1
            periodId = reservation.Time + 1
            roomId = reservation.Room
            dur = cc.Duration

            key = (periodId, roomId)
            if key in slot_table:
                room_duration = slot_table[key]
            else:
                room_duration = ROOM_COLUMN_NUMBER * [0]
                slot_table[key] = room_duration
            room_duration[dayId] = dur

            for m in range(1, dur):
                next_key = (periodId + m, roomId)
                if next_key not in slot_table:
                    slot_table[next_key] = ROOM_COLUMN_NUMBER * [0]
                if slot_table[next_key][dayId] < 1:
                    slot_table[next_key][dayId] = -1

            if key in time_table:
                room_schedule = time_table[key]
            else:
                room_schedule = ROOM_COLUMN_NUMBER * [None]
                time_table[key] = room_schedule

            room_schedule[dayId] = "".join(getCourseClass(cc, solution.criteria, ci))
            ci += len(HTMLRaspored.CRITERIAS)

        return time_table

    @staticmethod
    def getHtmlCell(content, rowspan):
        if rowspan == 0:
            return "<td></td>"

        if content is None:
            return ""

        sb = []
        if rowspan > 1:
            sb.append("<td style='border: .1em solid black; padding: .25em' rowspan='")
            sb.append(rowspan)
            sb.append("'>")
        else:
            sb.append("<td style='border: .1em solid black; padding: .25em'>")

        sb.append(content)
        sb.append("</td>")
        return "".join(str(v) for v in sb)

    @staticmethod
    def getResult(solution):
        configuration = solution.configuration
        nr = configuration.numberOfRooms
        getRoomById = configuration.getRoomById

        slot_table = defaultdict(list)
        time_table = HTMLRaspored.generateTimeTable(solution, slot_table)
        if not slot_table or not time_table:
            return ""

        sb = []
        for roomId in range(nr):
            room = getRoomById(roomId)
            for periodId in range(HTMLRaspored.ROOM_ROW_NUMBER):
                if periodId == 0:
                    sb.append("<div id='room_")
                    sb.append(room.Name)
                    sb.append("' style='padding: 0.5em'>\n")
                    sb.append("<table style='border-collapse: collapse; width: 95%'>\n")
                    sb.append(HTMLRaspored.getTableHeader(room))
                else:
                    key = (periodId, roomId)
                    room_duration = slot_table[key] if key in slot_table.keys() else None
                    room_schedule = time_table[key] if key in time_table.keys() else None
                    sb.append("<tr>")
                    for dayId in range(HTMLRaspored.ROOM_COLUMN_NUMBER):
                        if dayId == 0:
                            sb.append("<th style='border: .1em solid black; padding: .25em' scope='row' colspan='2'>")
                            sb.append(HTMLRaspored.PERIODS[periodId-1])
                            sb.append("</th>\n")
                            continue

                        if room_schedule is None and room_duration is None:
                            continue

                        content = room_schedule[dayId] if room_schedule is not None else None
                        sb.append(HTMLRaspored.getHtmlCell(content, room_duration[dayId]))
                    sb.append("</tr>\n")

                if periodId == HTMLRaspored.ROOM_ROW_NUMBER - 1:
                    sb.append("</table>\n</div>\n")

        return "".join(str(v) for v in sb)

    @staticmethod
    def getTableHeader(room):
        if(room.Lab):
              sb = ["<tr><th style='border: .1em solid black' scope='col' colspan='2'>Racunarska ucionica: ", room.Name, "</th>\n"]
        else:
              sb = ["<tr><th style='border: .1em solid black' scope='col' colspan='2'>Ucionica: ", room.Name, "</th>\n"]
        for weekDay in HTMLRaspored.WEEK_DAYS:
            sb.append("<th style='border: .1em solid black; padding: .25em; width: 15%' scope='col' rowspan='2'>")
            sb.append(weekDay)
            sb.append("</th>\n")
        sb.append("</tr>\n")
        sb.append("<tr>\n")
        sb.append("</th>\n")
        sb.append("<th style='border: .1em solid black; padding: .25em'>Broj mesta: ")
        sb.append(room.NumberOfSeats)
        sb.append("</th>\n")
        sb.append("</tr>\n")
        return "".join(str(v) for v in sb)
    
