# this will be a class module for the inventory system
# this will need to define classes for an item first


class item:
    def __init__(self, blUseable = False, blEquipable = False,
                 strEquipmentType = "None", intValue = 0,
                 strInfoText = "This item is missing a description",
                 strItemName = "Nameless", strEngineName = "ItemNameError"):
        #put shit in here that all items have to have
        self.blUsable           = blUsable
        self.blEquipable        = blEquipable
        self.intEquipmentType   = intEquipmentType
        self.intValue           = intValue
        self.strInfoText        = strInfoText
        self.strItemName        = strItemName
        self.strEngineName      = strEngineName
        
