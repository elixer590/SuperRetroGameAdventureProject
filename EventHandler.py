"""
Start of event handler class

Goal:
    Design a basic object to handle and dispatch events. At the most
    basic level we will react saying an event has happened. At a Higher
    Level we will pass along the object that sent the event as well as
    a list of event parameters
"""

class Event_Handler:
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
        self.htblSubsriptions = {}

    def EventListener(self, eventName, handler): #set a function to listen for a specific event
        # save the handler into the hashtable for this event
        # first check if there is an event in the table
        if self.htblSubsriptions.get(hash(eventName)) == None:
            #we need to add a new entry into the hash table for this event
            self.htblSubsriptions[hash(eventName)] = [eventName, [handler]]
        else:
            # Add to handler list
            self.htblSubsriptions[hash(eventName)][1].append(handler)

    def RaiseEvent(self, eventName, event=None):
        self.lstEvents.append((eventName, event))

    def HandleEvents(self):
        for currentEvent in self.lstEvents:
            if self.htblSubsriptions[hash(currentEvent[0])] != None: #look to see if this is handled
                #if there are handlers, pass each one the event
                #[eventName, [handler]] - this is the values int eh hash table - get the list of handlers
                for handler in self.htblSubsriptions[hash(currentEvent[0])][1]:
                    #event structure is ((EventName, event))
                    handler(currentEvent[1])
        #prevent handling the same event multiple times
        self.lstEvents = []

if __name__ == "__main__":
    """Test scripts here"""
    class TESTCLASS:
        def __init__(self):
            objEventHandler.EventListener("testEvent", self.testFunction2)

        def testFunction2(self, events):
            print("this class handled this event without code specifying it should")


    objEventHandler = Event_Handler()
    objtestclass = TESTCLASS()
    objEventHandler.RaiseEvent("testEvent")
    objEventHandler.HandleEvents()