"""
Start of event handler class

Goal:
    Design a basic object to handle and dispatch events. At the most
    basic level we will react saying an event has happened. At a Higher
    Level we will pass along the object that sent the event as well as
    a list of event parameters
"""


class EventHandler:
    """
    The event handler will hold a dictionary of subscriptions and a list of events to handle
    it should be called once per frame, and the event list should be cleared after passing events to be handled
    This means that there must be an active listener or an event will be received but not handled

    for each event in the event list check dictionary for matching key
    if there is a match there will be a list of handler functions.
    For each function in this list pass the event

    Need to create a standard event object structure
    """

    def __init__(self):
        self.lstEvents = []
        # subscription hash table will look like such
        # [eventName, [list of events]
        self.htblSubscriptions = {}

    def EventListener(self, eventName, handler): # set a function to listen for a specific event
        # save the handler into the hashtable for this event
        # first check if there is an event in the table
        if self.htblSubscriptions.get(hash(eventName)) is None:
            # we need to add a new entry into the hash table for this event
            self.htblSubscriptions[hash(eventName)] = [eventName, [handler]]
        else:
            # Add to handler list
            self.htblSubscriptions[hash(eventName)][1].append(handler)

    def RaiseEvent(self, eventName, event=None):
        self.lstEvents.append((eventName, event))

    def HandleEvents(self):
        for currentEvent in self.lstEvents:
            if hash(currentEvent[0]) in self.htblSubscriptions:  # look to see if this is handled
                # if there are handlers, pass each one the event
                # [eventName, [handler]] - this is the values int eh hash table - get the list of handlers
                for handler in self.htblSubscriptions[hash(currentEvent[0])][1]:
                    # event structure is ((EventName, event))
                    handler(currentEvent[1])
        # prevent handling the same event multiple times
        self.lstEvents = []


if __name__ == "__main__":
    """Test scripts here"""
    class TESTCLASS:
        def __init__(self):
            objEventHandler.EventListener("testEvent", self.testFunction2)

        def testFunction2(self, events):
            print("this class handled this event without code specifying it should")


    objEventHandler = EventHandler()
    objTestclass = TESTCLASS()
    objEventHandler.RaiseEvent("testEvent")
    objEventHandler.HandleEvents()

