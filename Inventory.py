"""
Will contain an inventory container and item management classes
"""
import EventHandler


class InventoryContainer:
    # the inventory should be a dictionary of items
    # "Key: value" will be "Item Name: [Item name, Quantity]"
    def __init__(self):
        self._Inventory = {}

    def Add(self, ItemName, Quantity):
        self._Inventory[ItemName] = [ItemName, Quantity]

    def Remove(self, ItemName, Quantity=1):
        # check if quantity will be 0 or less and delete from inventory if so
        if self._Inventory[ItemName][1] <= Quantity:
            del self._Inventory[ItemName]
        else:
            # if not, subtract removed quantity
            self._Inventory[ItemName][1] -= Quantity


class Item:
    """
    Item class will hold specific information about items. attributes will be added as they are found to be needed
    Name        - description shown to player, and identifier in inventory
    Strength    - level of effect - most effects will have multiple tiers (3-5)
    defaultTarget- What the default target will be when used in battle, or from the menu screen
                - items with "None" can only be used in the menu screen
    Usable      - if the item can be used, and if so where? always, in battle, out of battle, or never.
    EffectType  - function that should handle this
    Icon        - image object to represent the item
    """

    def __init__(self, name, effectType=None, strength=0, defaultTarget=None, keyItem=False):
        self.Name = name
        self.EffectType = effectType
        self.Strength = strength
        self.DefaultTarget = defaultTarget
        self.blKeyItem = keyItem
        self.Icon = None

    def use(self):
        # concept use of the item?
        # call use item and then item returns a event to be raised?
        return EventHandler.Event(self.EffectType, self.Strength)