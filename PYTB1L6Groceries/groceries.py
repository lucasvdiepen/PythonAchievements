GroceryList = ["Milk", "Cheese", "Sausage"]
ShoppingCart = ["Sausage", "Milk", "Cheese"]

ShoppingDone = True

for GroceryItem in GroceryList:
    if (GroceryItem in ShoppingCart):
        ShoppingCart.remove(GroceryItem)
    else:
        ShoppingDone = False
        break

if(ShoppingDone):
    print("Done shopping")
else:
    print("Continue Shopping")
