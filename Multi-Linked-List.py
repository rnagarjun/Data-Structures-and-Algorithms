class InvalidEventError(Exception):
    '''An error to be raised when the user requests to retrieve/create an event
    with impossible/invalid data'''


class NoSuchEventError(Exception):
    '''An error to be raised when the user attempts to access an event that
    does not exist'''


class IncompatableCalendarError(Exception):
    '''An error to be raised when the user attempts to add calendars with
    incompatable types/durations'''


class EventNode():
    '''A node representing an event'''

    def __init__(self, event_name=None, day=None, time=None, room=None,
                 next_time=None, next_day=None, next_room=None,
                 next_in_day=None, next_in_time=None, next_in_room=None):
        '''(EventNode, str[, EventNode, EventNode, EventNode]) -> NoneType

        Create a new event with the name event_name, and set the next events
        that will be held on this day (next_in_day), in this time-slot
        (next_in_time), and in this room (next_in_room) if available'''
        # the name of the event
        self._event_name = event_name
        # the day of an event
        self._day = day
        # the time of an event
        self._time = time
        # the location of an event
        self._room = room

        # a reference to the next day in the calendar
        self.next_day = next_day
        # a reference to the next time in the calendar
        self.next_time = next_time
        # a reference to the next room in the calendar
        self.next_room = next_room

        # a reference to the next event that will happen on this day
        self.next_in_day = next_in_day
        # a reference to the next event that will happen in this time-slot
        self.next_in_time = next_in_time
        # a reference to the next event that will happen in this room
        self.next_in_room = next_in_room

    def get_event_name(self):
        '''Return the name of this event'''
        return self._event_name

    def get_day(self):
        '''Return the day of this event'''
        return self._day

    def get_time(self):
        '''Return the time of this event'''
        return self._time

    def get_room(self):
        '''Return the room of this event'''
        return self._room


class Calendar():
    '''A general calendar'''

    def __init__(self, number_of_days):
        '''(Calendar, int) -> NoneType

        Create a new calendar for the next number_of_days days
        '''
        # Initializing the head of the day, time and room
        self._number_of_days = number_of_days
        self._HD = None
        self._HT = None
        self._HR = None

    def sortedInsertTime(self, head, new_node):
        '''(Calendar, linked list) -> EventNode

        A helper function that adds the given EventNode, in the given linked
        list by sorted room and returns the current node'''
        # If the head of the LL is None, then make the new node to be the head
        if head is None:
            new_node.next_in_time = head
            head = new_node
            return head
        # If the head exist, then keep traversing through the LL while the time
        # value of LL is less than the new_node's time value
        else:
            current = head
            while(current.next_in_time is not None and
                  current.next_in_time.get_day() < new_node.get_day()):
                current = current.next_in_time
            # When the position is found, set the new node to point to the next
            # node and make the current node to be the new node
            new_node.next_in_time = current.next_in_time
            current.next_in_time = new_node
            return current.next_in_time

    def sortedInsertDay(self, head, new_node):
        '''(Calendar, linked list) -> EventNode

        A helper function that adds the given EventNode, in the given linked
        list by sorted day and returns the current node'''
        # If the head of the LL is None, then make the new node to be the head
        if head is None:
            new_node.next_in_day = head
            head = new_node
            return head
        # If the head exist, then keep traversing through the LL while the day
        # value of LL is less than the new_node's day value
        else:
            current = head
            while(current.next_in_day is not None and
                  current.next_in_day.get_time() < new_node.get_time()):
                current = current.next_in_day
            # When the position is found, set the new node to point to the next
            # node and make the current node to be the new node
            new_node.next_in_day = current.next_in_day
            current.next_in_day = new_node
            return current.next_in_day

    def sortedInsertRoom(self, head, new_node):
        '''(Calendar, linked list) -> EventNode

        A helper function that adds the given EventNode, in the given linked
        list by sorted room and returns the current node'''
        # If the head of the LL is None, then make the new node to be the head
        if head.next_in_room is None:
            head.next_in_room = new_node
            return head
        # If the head exist, then keep traversing through the LL while the time
        # value of LL is less than the new_node's time value
        else:
            current = head
            while(current.next_in_room is not None and
                  current.next_in_room.get_day() < new_node.get_day()):
                current = current.next_in_room

            if current.next_in_room is not None:

                if current.next_in_room.get_day() == new_node.get_day():
                    while(current.next_in_room is not None and current.next_in_room.get_day() == new_node.get_day() and current.next_in_room.get_time() < new_node.get_time()):
                        current = current.next_in_room

            # When the position is found, set the new node to point to the next
            # node and make the current node to be the new node
            new_node.next_in_room = current.next_in_room
            current.next_in_room = new_node
            return current.next_in_room

    def insert_day(self, new_node):
        '''(Calendar, EventNode) -> EventNode

        A helper function that adds the day, to the linked list head returns
        the head'''
        # If the head of the LL is None, then make the new node to be the head
        if self._HD is None:
            new_node.next_day = self._HD
            self._HD = new_node
            return self._HD
        # Special case if to compare the head of the LL
        elif new_node.get_day() < self._HD.get_day():
            new_node.next_day = self._HD
            self._HD = new_node
            return self._HD
        else:
            # Loop through and compare the time values
            # Find the node before the the new_node and insert if right after
            current = self._HD
            while(current.next_day is not None and (current.next_day.get_day() < new_node.get_day())):
                current = current.next_day
            new_node.next_day = current.next_day
            current.next_day = new_node
            return current.next_day

    def insert_time(self, new_node):
        '''(Calendar, EventNode) -> EventNode

        A helper function that adds the time, to the linked list head returns
        the head'''
        # If the head of the LL is None, then make the new node to be the head
        if self._HT is None:
            new_node.next_time = self._HT
            self._HT = new_node
            return self._HT
        # Special case if to compare the head of the LL
        elif new_node.get_time() < self._HT.get_time():
            new_node.next_time = self._HT
            self._HT = new_node
            return self._HT
        else:
            # Loop through and compare the time values
            # Find the node before the the new_node and insert if right after
            current = self._HT
            while(current.next_time is not None and (current.next_time.get_time() < new_node.get_time())):
                current = current.next_time
            new_node.next_time = current.next_time
            current.next_time = new_node
            return current.next_time

    def insert_room(self, new_node):
        '''(Calendar, EventNode) -> EventNode

        A helper function that adds the room, to the linked list head returns
        the head'''
        # If the head of the LL is None, then make the new node to be the head
        if (self._HR is None):
            self._HR = new_node
            return self._HR
        else:
            current = self._HR
            # as long as next is not None
            # keep moving further into the LL
            while (current.next_room is not None):
                current = current.next_room
            # Append the new_node into the LL
            current.next_room = new_node
            return current.next_room

    def find_prev_in_day(self, day, time, room):
        '''(Calendar, int, int, int) -> EventNode

        Return the previous EventNode of a day given the day, time and room
        values'''
        # Find the day node
        curr = self.find_day(self._HD, day)
        # Raise exception if the day node does not exist
        if curr is None:
            raise NoSuchEventError
        # set current node to be prev and and curr to be next node
        prev = curr
        curr = curr.next_in_day
        # loop through until room and and time are found
        while (curr is not None and curr.get_time() != time and curr.get_room() != room):
            prev = curr
            curr = curr.next_in_day
        # return the previous node
        return prev

    def find_prev_in_time(self, day, time, room):
        '''(Calendar, int, int, int) -> EventNode

        Return the previous EventNode of a time given the day, time and room
        values'''
        # Find the time node
        curr = self.find_time(self._HT, time)
        # Raise exception if the time node DNE
        if curr is None:
            raise NoSuchEventError
        prev = curr
        curr = curr.next_in_time
        # loop through until day and room are found
        while (curr is not None and curr.get_day() != day and curr.get_room() != room):
            prev = curr
            curr = curr.next_in_time
        # return the previous node
        return prev

    def find_prev_in_room(self, day, time, room):
        '''(Calendar, int, int, int) -> EventNode

        Return the previous EventNode of a day given the day, time and room
        values'''
        # Find the room node
        curr = self.find_room(self._HR, room)
        # Raise exception if the room DNE in the calendar
        if curr is None:
            raise NoSuchEventError
        prev = curr
        curr = curr.next_in_room
        # Loop through until the node is found by comparing time and day
        while (curr is not None and curr.get_time() != time and curr.get_day() != day):
            prev = curr
            curr = curr.next_in_room
        # return the previous node
        return prev

    def find_day(self, head, day):
        """ (Calendar, EventNode, int) -> IntNode

        Finds and returns the EventNode, given the day head and the day value
        """
        # loop through and find the current day node by comparing the day
        curr = head
        while curr is not None and curr.get_day() != day:
            curr = curr.next_day
        return curr if curr is not None else None

    def find_time(self, head, time):
        """ (Calendar, EventNode, int) -> IntNode

        Finds and returns the EventNode, given the time head and the time value
        """
        # loop through and find the current time node by comparing the time
        curr = head
        while curr is not None and curr.get_time() != time:
            curr = curr.next_time
        return curr if curr is not None else None

    def find_room(self, head, room):
        """ (Calendar, EventNode, int) -> IntNode

        Finds and returns the EventNode, given the room Head and the room value
        """
        # loop through and find the current room node by comparing the room
        curr = head
        while curr is not None and curr.get_room() != room:
            curr = curr.next_room
        return curr if curr is not None else None

    def prev_day(self, head, day):
        """ (Calendar, EventNode, int) -> IntNode

        Find and returns the previous day, given the day head and the day value
        """
        # loop through and and compare the day, then return the node before it
        curr = head
        prev = None
        while curr is not None and curr.get_day() != day:
            prev = curr
            curr = curr.next_day
        return prev

    def prev_time(self, head, time):
        """ (Calendar, EventNode, int) -> IntNode

        Finds and returns the previous time, given the time head and the time
        value
        """
        # loop through and and compare the time, then return the node before it
        curr = head
        prev = None
        while curr is not None and curr.get_time() != time:
            prev = curr
            curr = curr.next_time
        return prev

    def prev_room(self, head, room):
        """ (Calendar, EventNode, int) -> IntNode

        Finds and returns the previous room, given the room head and the room
        value
        """
        # loop through and and compare the room, then return the node before it
        curr = head
        prev = None
        while curr is not None and curr.get_room() != room:
            prev = curr
            curr = curr.next_room
        return prev

    def add_event(self, title, day, time, room):
        '''(Calendar, str, int, int, str) -> NoneType

        Add a new event to this calendar to be held in room on the day'th
        day at time (assuming the calendar starts on day 0, and all times
        are given in hourly increments with 0 being 12AM and 23 being 11PM)

        '''
        # Cases of exceptions that are required when adding an event
        day_exceptions = (not isinstance(day, int) or day >= self._number_of_days if str(self.__class__.__name__) == 'Calendar' else False)
        time_exceptions = (not isinstance(time, int) or time < 0 or time > 23)
        room_exceptions = (not isinstance(room, str))
        event = self.find_event(day, time, room)
        event_exist = (event is not None)
        # Executes the exceptions and raises error if any found
        if (day_exceptions or time_exceptions or event_exist or room_exceptions):
                raise InvalidEventError
        # Findt he day, time and room that the event is in
        curr_day = self.find_day(self._HD, day)
        curr_time = self.find_time(self._HT, time)
        curr_room = self.find_room(self._HR, room)
        # If the day DNE then make a new day node
        if curr_day is None:
            day_node = EventNode('Day '+str(day), day)
            curr_day = self.insert_day(day_node)
        # If the time DNE then make a new day node
        if curr_time is None:
            time_node = EventNode('Time '+str(time), None, time)
            curr_time = self.insert_time(time_node)
        # If the room DNE then make a new day node
        if curr_room is None:
            room_node = EventNode('Room '+str(room), None, None, room)
            curr_room = self.insert_room(room_node)
        # Make a new node, and keep inserting that node through the each helper
        # function after it is returned from the prev ones to combine the LL
        new_node = EventNode(title, day, time, room)
        day_done = self.sortedInsertDay(curr_day, new_node)
        time_done = self.sortedInsertTime(curr_time, day_done)
        room_done = self.sortedInsertRoom(curr_room, time_done)

    def add_calendar(self, calendar_to_add):
        '''(Calendar, Calendar) -> NoneType

        Add all events from calendar_to_add to this calendar
        '''
        # get teh head of the calendar that needs to be added
        day_head = calendar_to_add._HD
        # loop through day
        while day_head is not None:
            curr_event = day_head.next_in_day
            # for every node in each day, add the node to this calendar
            while curr_event is not None:
                # If a event already exist, raise Incompatible calendar error
                try:
                    title, day, time, room = (curr_event.get_event_name(),
                                              curr_event.get_day(),
                                              curr_event.get_time(),
                                              curr_event.get_room())
                    self.add_event(title, day, time, room)
                except InvalidEventError:
                    raise IncompatableCalendarError
                curr_event = curr_event.next_in_day
            day_head = day_head.next_day

    def get_event(self, time, day, room):
        '''(Calendar, int, int, int) -> str

        Return the title of the event held in room on day at time
        '''
        # Call on the find_event method to find the event, and raise exception
        # if no event is found
        curr = self.find_event(day, time, room)
        if curr is not None:
            return curr.get_event_name()
        else:
            raise NoSuchEventError

    def find_event(self, day, time, room):
        # find the day node
        curr = self.find_day(self._HD, day)
        if curr is None:
            return curr
        # loop through and compare the times in that specific day and return
        # the node if it exists
        curr = curr.next_in_day
        while curr is not None and curr.get_time() != time:
            curr = curr.next_in_day
        return curr

    def get_first_event(self):
        '''(Calendar) -> (str, int, int, str)

        Return a tuple of (event name, event day, event time, event room) for
        the first event in this calendar
        '''
        # Try to get the event, if u can't, raise an exception
        try:
            first_event = self._HD.next_in_day
            return (first_event.get_event_name(), first_event.get_day(),
                    first_event.get_time(), first_event.get_room())
        except:
            raise NoSuchEventError

    def get_first_in_day(self, day):
        '''(Calendar, int) -> (str, int, str)

        Return a tuple of (event name, event time, event room) for
        the first event in this calendar on the given day.
        '''
        # Try to get the event, if u can't, raise an exception
        if self._HD is None:
            raise NoSuchEventError
        curr_day = self.find_day(self._HD, day)
        curr_day = curr_day.next_in_day

        return (curr_day.get_event_name(), curr_day.get_time(),
                curr_day.get_room())

    def get_first_at_time(self, time):
        '''(Calendar, int) -> (str, int, str)

        Return a tuple of (event name, event day, event room) for
        the first event in this calendar to occur at the given time
        '''
        # Try to get the event, if u can't, raise an exception
        if self._HT is None:
            raise NoSuchEventError
        curr_time = self.find_time(self._HT, time)
        curr_time = curr_time.next_in_time

        return (curr_time.get_event_name(), curr_time.get_day(),
                curr_time.get_room())

    def get_first_in_room(self, room):
        '''(Calendar, int) -> (str, int, int)

        Return a tuple of (event name, event day, event time) for
        the first event in this calendar held in the given room
        '''
        # Try to get the event, if u can't, raise an exception
        if self._HR is None:
            raise NoSuchEventError
        curr_room = self.find_room(self._HR, room)
        curr_room = curr_room.next_in_room

        return (curr_room.get_event_name(), curr_room.get_day(),
                curr_room.get_time())

    def get_all_in_day(self, day):
        '''(Calendar, int) -> DailyCalendar

        Return a calendar of all events for the specified day
        '''
        # find the day nead and raise error if day head DNE
        day_head = self.find_day(self._HD, day)
        if day_head is None:
            raise NoSuchEventError
        # made a daily calendar and set the day head of the calendar to be
        # the day head of this calendar
        daily_calendar = DailyCalendar(day)
        daily_calendar._HD = day_head
        # return a daily_calendar class
        return daily_calendar

    def get_all_in_room(self, room):
        '''(Calendar, str) -> RoomCalendar

        Return a calendar of all events in a specific room
        '''
        # find the day nead and raise error if day head DNE
        room_head = self.find_room(self._HR, room)
        if room_head is None:
            raise NoSuchEvent
        # made a daily calendar and set the day head of the calendar to be
        # the day head of this calendar
        room_calendar = RoomCalendar(self._number_of_days, room)
        room_calendar._HR = room_head
        # return a daily_calendar class
        return room_calendar

    def remove_event(self, day, time, room):
        '''(Calendar, int, int, str) -> NoneType

        Delete the specified event from the calendar
        '''
        # Get the previous day, time and room
        prev_day = self.find_prev_in_day(day, time, room)
        prev_time = self.find_prev_in_time(day, time, room)
        prev_room = self.find_prev_in_room(day, time, room)
        # Set the previous node of each LL, to the next next node to
        # remove that required node
        prev_day.next_in_day = prev_day.next_in_day.next_in_day
        prev_time.next_in_time = prev_time.next_in_time.next_in_time
        prev_room.next_in_room = prev_room.next_in_room.next_in_room

    def remove_room(self, room):
        '''(Calendar, str) -> NoneType

        Delete all events held in the specified room
        '''
        # If the head of the room is empty, then raise error
        if self._HR is None:
            raise NoSuchEventError
        # find the room, and set curr to be next node
        curr_room = self.find_room(self._HR, room)
        curr_room = curr_room.next_in_room
        # loop through while the current node is not none
        while curr_room is not None:
            self.remove_event(curr_room.get_day(), curr_room.get_time(),
                              curr_room.get_room())
            curr_room = curr_room.next_in_room
        # find the previous room
        prev_room = self.prev_room(self._HR, room)
        # if the node is the head, then set next node to be the head
        if prev_room is None:
            self._HR = self._HR.next_room
        # else set next node to be next next node
        else:
            prev_room.next_room = prev_room.next_room.next_room

    def remove_day(self, day):
        '''(Calendar, int) -> NoneType

        Delete all events on the specified day
        '''
        # If the head of the day is empty, then raise error
        if self._HD is None:
            raise NoSuchEventError
        # find the day, and set curr to be next node
        curr_day = self.find_day(self._HD, day)
        curr_day = curr_day.next_in_day
        # loop through while the current node is not none
        while curr_day is not None:
            self.remove_event(curr_day.get_day(), curr_day.get_time(),
                              curr_day.get_room())
            curr_day = curr_day.next_in_day
        # find the previous day
        prev_day = self.prev_day(self._HD, day)
        # if the node is the head, then set next node to be the head
        # else set next node to be next next node
        if prev_day is None:
            self._HD = self._HD.next_day
        else:
            prev_day.next_day = prev_day.next_day.next_day

    def remove_time(self, time):
        '''(Calendar, int) -> NoneType

        Delete all events at the specified time
        '''
        # If the head of the day is empty, then raise error
        if self._HR is None:
            raise NoSuchEventError
        # find the day, and set curr to be next node
        curr_time = self.find_time(self._HT, time)
        curr_time = curr_time.next_in_time
        while curr_time is not None:
            self.remove_event(curr_time.get_day(), curr_time.get_time(),
                              curr_time.get_room())
            curr_time = curr_time.next_in_time
        # find the previous time
        prev_time = self.prev_time(self._HT, time)
        # if the node is the head, then set next node to be the head
        # else set next node to be next next node
        if prev_time is None:
            self._HT = self._HT.next_time
        else:
            prev_time.next_time = prev_time.next_time.next_time

    def _get_event_node(self, time, day, room):
        '''(Calendar, int, int, str) -> EventNode

        A private method used to be used by the auto-marker

        Return the EventNode corresponding to the event held in the given
        room at the given time on the given day
        '''
        # call on find_event helper function to find the event
        curr = self.find_event(day, time, room)
        # if event doesn't exist, raise exception, else return the node
        if curr is not None:
            return curr
        else:
            raise NoSuchEventError


class DailyCalendar(Calendar):
    '''A calendar with all events in a day'''
    def __init__(self, day):
        '''(Calendar, int) --> None
        '''
        # preset the number of day to be only 1
        number_of_days = 1
        Calendar.__init__(self, number_of_days)
        self._day = day

    def add_event(self, title, time, room):
        '''(Calendar, str, int, str) -> NoneType

        Add a new event to this calendar to be held in room and all times
        are given in hourly increments with 0 being 12AM and 23 being 11PM)

        '''
        # Call on the add_event method from the calendar class
        Calendar.add_event(self, title, self._day, time, room)


class RoomCalendar(Calendar):
    '''A calendar with all events specific room'''
    def __init__(self, number_of_days, room):
        '''(Calendar, int, str) --> None
        '''
        # Initializing Variables
        Calendar.__init__(self, number_of_days)
        self._number_of_days = number_of_days
        self._room = room

    def add_event(self, title, day, time):
        '''(Calendar, str, int, int, str) -> NoneType

        Add a new event to this calendar to be held in room on the day'th
        day at time (assuming the calendar starts on day 0, and all times
        are given in hourly increments with 0 being 12AM and 23 being 11PM)

        '''
        # Calls on add_event in calendar class
        Calendar.add_event(self, title, day, time, self._room)

    def get_usage(self):
        '''(RoomCalendar) -> float

        Return the percentage of the time (from 0-1) that
        this room is in use
        '''
        # total hours is the number of day multiplied by 24 hours
        total_hours = self._number_of_days*24
        # if head is none
        if self._HR is None:
            percentage = 1
        else:
            curr = self._HR
            count = 0
            # go through and add 1 to counter for every event
            while curr.next_in_room is not None:
                curr = curr.next_in_room
                count += 1
            # do percentage calculator
            percentage = count/total_hours
        return percentage


class DailyRoomCalendar(DailyCalendar, RoomCalendar):
    '''A calendar with all events in a speicifc room for a given day'''

    def __init__(self, day, room):
        DailyCalendar.__init__(self, day)
        RoomCalendar.__init__(self, 1, room)
        self._room = room
        self._day = day

    def add_event(self, title, time):
        '''(Calendar, str, int) -> NoneType

        Add a new event to this calendar and all times
        are given in hourly increments with 0 being 12AM and 23 being 11PM)

        '''
        # raise error if the room enter and day enters do not match the
        # initialization day and room
        Calendar.add_event(self, title, self._day, time, self._room)

    def find_cleaning_times(self):
        '''(DailyRoomCalendar) -> list of int

        Return a sorted list of all hours that this room is free for
        cleaning
        '''
        # initialize an empty list
        cleaning_list = []
        curr = self._HD
        count = 0
        curr = curr.next_in_day
        # while count < 24, go through the loop
        while count < 24:
            # if the curr node's time value equals count then go to next node
            if curr.get_time() == count:
                if curr.next_in_day is not None:
                    curr = curr.next_in_day
            # if the time is not in the linked list, then add the count to list
            else:
                cleaning_list.append(count)
            count += 1
        # sort the list
        cleaning_list.sort()
        return cleaning_list
