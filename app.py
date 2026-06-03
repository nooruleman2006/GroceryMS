from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# ─── IN-MEMORY STORAGE ────────────────────────────────────────────────────────

categories = []
items = []
suppliers = []
customers = []

category_counter = 0
item_counter = 0
supplier_counter = 0
customer_counter = 0

# ─── HELPER CLASSES ───────────────────────────────────────────────────────────

class Category:
    def __init__(self, category_id, name):
        self.category_id = category_id
        self.name = name

    def to_dict(self):
        return {"category_id": self.category_id, "name": self.name}

class Item:
    def __init__(self, item_id, name, qty_in_stock, unit_price, category_id):
        self.item_id = item_id
        self.name = name
        self.qty_in_stock = qty_in_stock
        self.unit_price = unit_price
        self.category_id = category_id
        self.sold_qty = 0
        self.status = 0

    def to_dict(self):
        return {
            "item_id": self.item_id,
            "name": self.name,
            "qty_in_stock": self.qty_in_stock,
            "unit_price": self.unit_price,
            "category_id": self.category_id,
            "sold_qty": self.sold_qty,
            "status": self.status
        }

class Supplier:
    def __init__(self, supplier_id, name, shop_no, city, society, item_supplied, day, month, year):
        self.supplier_id = supplier_id
        self.name = name
        self.shop_no = shop_no
        self.city = city
        self.society = society
        self.item_supplied = item_supplied
        self.day = day
        self.month = month
        self.year = year

    def to_dict(self):
        return {
            "supplier_id": self.supplier_id,
            "name": self.name,
            "shop_no": self.shop_no,
            "city": self.city,
            "society": self.society,
            "item_supplied": self.item_supplied,
            "date": f"{self.day}/{self.month}/{self.year}"
        }

class CartItem:
    def __init__(self, item_id, qty):
        self.item_id = item_id
        self.qty = qty

class Customer:
    def __init__(self, customer_id, name, house_no, city, society, phone):
        self.customer_id = customer_id
        self.name = name
        self.house_no = house_no
        self.city = city
        self.society = society
        self.phone = phone
        self.cart = []
        self.bill = 0
        self.order_status = 0
        self.points = 0
        self.order_day = 0
        self.order_month = 0
        self.order_year = 0

    def to_dict(self):
        return {
            "customer_id": self.customer_id,
            "name": self.name,
            "house_no": self.house_no,
            "city": self.city,
            "society": self.society,
            "phone": self.phone,
            "bill": self.bill,
            "order_status": self.order_status,
            "points": self.points,
            "cart": [{"item_id": c.item_id, "qty": c.qty} for c in self.cart],
            "order_date": f"{self.order_day}/{self.order_month}/{self.order_year}"
        }

# ─── SEED DUMMY DATA ──────────────────────────────────────────────────────────

def seed_data():
    global categories, items, suppliers, customers
    global category_counter, item_counter, supplier_counter, customer_counter

    categories = [
        Category(1, "Fruits"),
        Category(2, "Vegetables"),
        Category(3, "Dairy"),
        Category(4, "Bakery"),
        Category(5, "Beverages"),
    ]
    category_counter = 5

    items = [
        # Fruits (category 1)
        Item(1,  "Bananas",        50,  180, 1),
        Item(2,  "Oranges",        40,  250, 1),
        Item(3,  "Apples",         35,  300, 1),
        Item(4,  "Mangoes",        60,  350, 1),
        Item(5,  "Grapes",         25,  400, 1),
        Item(6,  "Watermelon",     20,  150, 1),
        Item(7,  "Strawberries",   30,  500, 1),
        Item(8,  "Pomegranate",    45,  280, 1),
        Item(9,  "Guava",          55,  120, 1),
        Item(10, "Pineapple",      18,  220, 1),
        Item(11, "Papaya",         22,  180, 1),
        Item(12, "Kiwi",           15,  450, 1),
        Item(13, "Lychee",         40,  320, 1),
        Item(14, "Peach",          28,  260, 1),
        Item(15, "Pears",          33,  210, 1),

        # Vegetables (category 2)
        Item(16, "Onions",         80,  120, 2),
        Item(17, "Tomatoes",       60,   90, 2),
        Item(18, "Potatoes",       90,   80, 2),
        Item(19, "Spinach",        40,   60, 2),
        Item(20, "Carrots",        55,  100, 2),
        Item(21, "Capsicum",       35,  150, 2),
        Item(22, "Garlic",         70,  200, 2),
        Item(23, "Ginger",         65,  180, 2),
        Item(24, "Broccoli",       25,  220, 2),
        Item(25, "Cauliflower",    30,  130, 2),
        Item(26, "Cucumber",       50,   70, 2),
        Item(27, "Peas",           45,  140, 2),
        Item(28, "Bitter Gourd",   38,  110, 2),
        Item(29, "Bottle Gourd",   42,   90, 2),
        Item(30, "Lady Finger",    60,  120, 2),

        # Dairy (category 3)
        Item(31, "Eggs (12pcs)",  100,  350, 3),
        Item(32, "Milk 1L",        80,  180, 3),
        Item(33, "Butter 200g",    60,  280, 3),
        Item(34, "Cheese 200g",    45,  420, 3),
        Item(35, "Yogurt 500g",    70,  160, 3),
        Item(36, "Cream 200ml",    35,  220, 3),
        Item(37, "Paneer 250g",    50,  380, 3),
        Item(38, "Condensed Milk", 40,  250, 3),
        Item(39, "Skimmed Milk",   55,  200, 3),
        Item(40, "Flavored Milk",  65,  150, 3),
        Item(41, "Sour Cream",     30,  300, 3),
        Item(42, "Mozzarella",     25,  550, 3),
        Item(43, "Cheddar Slice",  40,  480, 3),
        Item(44, "Ice Cream 1L",   35,  650, 3),
        Item(45, "Whipping Cream", 20,  400, 3),

        # Bakery (category 4)
        Item(46, "Bread Loaf",     25,  120, 4),
        Item(47, "Croissant",      15,  200, 4),
        Item(48, "Baguette",       20,  180, 4),
        Item(49, "Muffin",         30,  150, 4),
        Item(50, "Donut",          40,  100, 4),
        Item(51, "Cake Slice",     18,  350, 4),
        Item(52, "Cookies 12pcs",  25,  280, 4),
        Item(53, "Brownie",        22,  200, 4),
        Item(54, "Cinnamon Roll",  16,  220, 4),
        Item(55, "Pita Bread",     35,  130, 4),
        Item(56, "Naan",           50,   60, 4),
        Item(57, "Rusk",           45,  150, 4),
        Item(58, "Pancake Mix",    20,  320, 4),
        Item(59, "Waffle",         15,  250, 4),
        Item(60, "Pizza Base",     18,  280, 4),

        # Beverages (category 5)
        Item(61, "Mineral Water",  100,  50, 5),
        Item(62, "Orange Juice",    60, 180, 5),
        Item(63, "Apple Juice",     55, 200, 5),
        Item(64, "Mango Juice",     70, 180, 5),
        Item(65, "Green Tea",       40, 350, 5),
        Item(66, "Black Tea",       50, 280, 5),
        Item(67, "Coffee",          35, 450, 5),
        Item(68, "Lemonade",        45, 120, 5),
        Item(69, "Sparkling Water", 30, 150, 5),
        Item(70, "Energy Drink",    25, 250, 5),
        Item(71, "Lassi 500ml",     60, 130, 5),
        Item(72, "Sugarcane Juice", 80,  80, 5),
        Item(73, "Coconut Water",   40, 160, 5),
        Item(74, "Aloe Vera Drink", 20, 220, 5),
        Item(75, "Rooh Afza",       35, 300, 5),
    ]
    item_counter = 75

    suppliers = [
        Supplier(1,  "Ahmed Traders",     5,  "Lahore", "DHA",          "Fruits",     1,  5, 2025),
        Supplier(2,  "Raza Store",        12, "Lahore", "Gulberg",       "Vegetables", 3,  4, 2025),
        Supplier(3,  "Dairy Fresh",       3,  "Lahore", "Model Town",    "Dairy",      10, 3, 2025),
        Supplier(4,  "Bakers Hub",        7,  "Lahore", "Johar Town",    "Bakery",     5,  6, 2025),
        Supplier(5,  "Fresh Farms",       9,  "Lahore", "Bahria Town",   "Fruits",     12, 2, 2025),
        Supplier(6,  "Green Valley",      2,  "Lahore", "Garden Town",   "Vegetables", 8,  5, 2025),
        Supplier(7,  "Milk & More",       15, "Lahore", "Wapda Town",    "Dairy",      20, 1, 2025),
        Supplier(8,  "Sunrise Bakery",    4,  "Lahore", "Iqbal Town",    "Bakery",     15, 4, 2025),
        Supplier(9,  "Hydra Drinks",      6,  "Lahore", "Cantt",         "Beverages",  1,  3, 2025),
        Supplier(10, "Punjab Organics",   11, "Lahore", "Faisal Town",   "Fruits",     7,  6, 2025),
        Supplier(11, "Subzi Mandi Co.",   8,  "Lahore", "Ichra",         "Vegetables", 14, 2, 2025),
        Supplier(12, "Nestle Distributor",1,  "Lahore", "Gulshan Ravi",  "Dairy",      9,  5, 2025),
        Supplier(13, "Bake n Bite",       13, "Lahore", "Samanabad",     "Bakery",     22, 3, 2025),
        Supplier(14, "AquaFresh",         10, "Lahore", "Township",      "Beverages",  18, 4, 2025),
        Supplier(15, "Tropical Fruits",   16, "Lahore", "Shadman",       "Fruits",     3,  1, 2025),
        Supplier(16, "Organic Veggies",   14, "Lahore", "Gulberg III",   "Vegetables", 25, 5, 2025),
        Supplier(17, "Creamy Delights",   17, "Lahore", "Valencia",      "Dairy",      11, 6, 2025),
        Supplier(18, "Dough Masters",     19, "Lahore", "Paragon City",  "Bakery",     6,  2, 2025),
        Supplier(19, "Cool Sips",         20, "Lahore", "Raiwind Road",  "Beverages",  28, 3, 2025),
        Supplier(20, "Farm Direct",       18, "Lahore", "Thokar Niaz",   "Fruits",     17, 4, 2025),
    ]
    supplier_counter = 20

    customers = [
        Customer(1,  "Ali Hassan",    12, "Lahore", "DHA",          3001234567),
        Customer(2,  "Sara Khan",     45, "Lahore", "Gulberg",       3019876543),
        Customer(3,  "Usman Raza",     7, "Lahore", "Model Town",    3045678901),
        Customer(4,  "Fatima Malik",  23, "Lahore", "Johar Town",    3031122334),
        Customer(5,  "Hassan Ahmed",  56, "Lahore", "Bahria Town",   3055566778),
        Customer(6,  "Ayesha Siddiq", 34, "Lahore", "Garden Town",   3062233445),
        Customer(7,  "Bilal Chaudhry",18, "Lahore", "Wapda Town",    3079988776),
        Customer(8,  "Zara Imran",    91, "Lahore", "Iqbal Town",    3083344556),
        Customer(9,  "Omar Farooq",   67, "Lahore", "Cantt",         3094455667),
        Customer(10, "Hina Tariq",    29, "Lahore", "Faisal Town",   3001122334),
        Customer(11, "Kamran Ali",    14, "Lahore", "Ichra",         3015544332),
        Customer(12, "Sana Baig",     38, "Lahore", "Gulshan Ravi",  3026677889),
        Customer(13, "Tariq Mehmood", 72, "Lahore", "Samanabad",     3037788990),
        Customer(14, "Nadia Hussain", 5,  "Lahore", "Township",      3048899001),
        Customer(15, "Imran Sheikh",  44, "Lahore", "Shadman",       3059900112),
        Customer(16, "Rabia Noor",    61, "Lahore", "Gulberg III",   3060011223),
        Customer(17, "Faisal Qureshi",83, "Lahore", "Valencia",      3071122334),
        Customer(18, "Maryam Aziz",   26, "Lahore", "Paragon City",  3082233445),
        Customer(19, "Asad Mehmood",  49, "Lahore", "Raiwind Road",  3093344556),
        Customer(20, "Lubna Khalid",  37, "Lahore", "Thokar Niaz",   3004455667),
    ]

    # Confirmed orders
    customers[0].cart.append(CartItem(1, 2))
    customers[0].cart.append(CartItem(3, 1))
    customers[0].bill = 660
    customers[0].order_status = 1
    customers[0].points = 1
    customers[0].order_day = 1
    customers[0].order_month = 5
    customers[0].order_year = 2025
    items[0].sold_qty += 2
    items[2].sold_qty += 1

    customers[2].cart.append(CartItem(31, 2))
    customers[2].cart.append(CartItem(46, 1))
    customers[2].bill = 820
    customers[2].order_status = 1
    customers[2].points = 1
    customers[2].order_day = 10
    customers[2].order_month = 5
    customers[2].order_year = 2025
    items[30].sold_qty += 2
    items[45].sold_qty += 1

    customers[4].cart.append(CartItem(4, 3))
    customers[4].cart.append(CartItem(61, 2))
    customers[4].bill = 1150
    customers[4].order_status = 1
    customers[4].points = 1
    customers[4].order_day = 15
    customers[4].order_month = 5
    customers[4].order_year = 2025
    items[3].sold_qty += 3
    items[60].sold_qty += 2

    customers[6].cart.append(CartItem(32, 2))
    customers[6].cart.append(CartItem(47, 2))
    customers[6].bill = 760
    customers[6].order_status = 1
    customers[6].points = 1
    customers[6].order_day = 20
    customers[6].order_month = 5
    customers[6].order_year = 2025
    items[31].sold_qty += 2
    items[46].sold_qty += 2

    customers[8].cart.append(CartItem(7, 1))
    customers[8].cart.append(CartItem(67, 1))
    customers[8].bill = 950
    customers[8].order_status = 1
    customers[8].points = 1
    customers[8].order_day = 25
    customers[8].order_month = 5
    customers[8].order_year = 2025
    items[6].sold_qty += 1
    items[66].sold_qty += 1

    # Pending orders
    customers[1].cart.append(CartItem(5, 1))
    customers[1].bill = 400

    customers[3].cart.append(CartItem(16, 2))
    customers[3].cart.append(CartItem(18, 3))
    customers[3].bill = 480

    customers[5].cart.append(CartItem(34, 1))
    customers[5].bill = 420

    customers[7].cart.append(CartItem(62, 3))
    customers[7].bill = 540

    customers[9].cart.append(CartItem(50, 4))
    customers[9].bill = 400

    customer_counter = 20

seed_data()

# ─── ROUTES ───────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")

# --- CATEGORIES ---
@app.route("/api/categories", methods=["GET"])
def get_categories():
    return jsonify([c.to_dict() for c in categories])

@app.route("/api/categories", methods=["POST"])
def add_category():
    global category_counter
    data = request.json
    cid = data.get("category_id")
    if any(c.category_id == cid for c in categories):
        return jsonify({"error": "Category ID already exists"}), 400
    categories.append(Category(cid, data["name"]))
    category_counter += 1
    return jsonify({"message": "Category added successfully"})

@app.route("/api/categories/<int:cid>", methods=["PUT"])
def update_category(cid):
    for c in categories:
        if c.category_id == cid:
            c.name = request.json.get("name", c.name)
            return jsonify({"message": "Category updated"})
    return jsonify({"error": "Category not found"}), 404

@app.route("/api/categories/<int:cid>", methods=["DELETE"])
def delete_category(cid):
    global categories
    categories = [c for c in categories if c.category_id != cid]
    return jsonify({"message": "Category deleted"})

# --- ITEMS ---
@app.route("/api/items", methods=["GET"])
def get_items():
    return jsonify([i.to_dict() for i in items])

@app.route("/api/items", methods=["POST"])
def add_item():
    global item_counter
    data = request.json
    iid = data.get("item_id")
    if any(i.item_id == iid for i in items):
        return jsonify({"error": "Item ID already exists"}), 400
    if not any(c.category_id == data["category_id"] for c in categories):
        return jsonify({"error": "Category not found"}), 400
    items.append(Item(iid, data["name"], data["qty_in_stock"], data["unit_price"], data["category_id"]))
    item_counter += 1
    return jsonify({"message": "Item added successfully"})

@app.route("/api/items/<int:iid>", methods=["PUT"])
def update_item(iid):
    for i in items:
        if i.item_id == iid:
            i.name         = request.json.get("name",          i.name)
            i.qty_in_stock = request.json.get("qty_in_stock",  i.qty_in_stock)
            i.unit_price   = request.json.get("unit_price",    i.unit_price)
            return jsonify({"message": "Item updated"})
    return jsonify({"error": "Item not found"}), 404

@app.route("/api/items/<int:iid>", methods=["DELETE"])
def delete_item(iid):
    global items
    items = [i for i in items if i.item_id != iid]
    return jsonify({"message": "Item deleted"})

# --- SUPPLIERS ---
@app.route("/api/suppliers", methods=["GET"])
def get_suppliers():
    return jsonify([s.to_dict() for s in suppliers])

@app.route("/api/suppliers", methods=["POST"])
def add_supplier():
    global supplier_counter
    data = request.json
    sid = data.get("supplier_id")
    if any(s.supplier_id == sid for s in suppliers):
        return jsonify({"error": "Supplier ID already exists"}), 400
    suppliers.append(Supplier(
        sid, data["name"], data["shop_no"], data["city"],
        data["society"], data["item_supplied"],
        data["day"], data["month"], data["year"]
    ))
    supplier_counter += 1
    return jsonify({"message": "Supplier added successfully"})

@app.route("/api/suppliers/<int:sid>", methods=["PUT"])
def update_supplier(sid):
    for s in suppliers:
        if s.supplier_id == sid:
            s.name          = request.json.get("name",          s.name)
            s.shop_no       = request.json.get("shop_no",       s.shop_no)
            s.city          = request.json.get("city",          s.city)
            s.society       = request.json.get("society",       s.society)
            s.item_supplied = request.json.get("item_supplied", s.item_supplied)
            s.day           = request.json.get("day",           s.day)
            s.month         = request.json.get("month",         s.month)
            s.year          = request.json.get("year",          s.year)
            return jsonify({"message": "Supplier updated"})
    return jsonify({"error": "Supplier not found"}), 404

@app.route("/api/suppliers/<int:sid>", methods=["DELETE"])
def delete_supplier(sid):
    global suppliers
    suppliers = [s for s in suppliers if s.supplier_id != sid]
    return jsonify({"message": "Supplier deleted"})

# --- CUSTOMERS ---
@app.route("/api/customers", methods=["GET"])
def get_customers():
    return jsonify([c.to_dict() for c in customers])

@app.route("/api/customers", methods=["POST"])
def add_customer():
    global customer_counter
    data = request.json
    cid = data.get("customer_id")
    if any(c.customer_id == cid for c in customers):
        return jsonify({"error": "Customer ID already exists"}), 400
    customers.append(Customer(
        cid, data["name"], data["house_no"],
        data["city"], data["society"], data["phone"]
    ))
    customer_counter += 1
    return jsonify({"message": "Customer added successfully"})

@app.route("/api/customers/<int:cid>", methods=["PUT"])
def update_customer(cid):
    for c in customers:
        if c.customer_id == cid:
            c.name     = request.json.get("name",     c.name)
            c.house_no = request.json.get("house_no", c.house_no)
            c.city     = request.json.get("city",     c.city)
            c.society  = request.json.get("society",  c.society)
            c.phone    = request.json.get("phone",    c.phone)
            return jsonify({"message": "Customer updated"})
    return jsonify({"error": "Customer not found"}), 404

@app.route("/api/customers/<int:cid>", methods=["DELETE"])
def delete_customer(cid):
    global customers
    customers = [c for c in customers if c.customer_id != cid]
    return jsonify({"message": "Customer deleted"})

# --- CART ---
@app.route("/api/cart/<int:cid>", methods=["GET"])
def get_cart(cid):
    for c in customers:
        if c.customer_id == cid:
            cart_details = []
            for cart_item in c.cart:
                for i in items:
                    if i.item_id == cart_item.item_id:
                        cart_details.append({
                            "item_id": i.item_id,
                            "name": i.name,
                            "qty": cart_item.qty,
                            "unit_price": i.unit_price,
                            "subtotal": i.unit_price * cart_item.qty
                        })
            return jsonify({"customer": c.name, "cart": cart_details, "bill": c.bill})
    return jsonify({"error": "Customer not found"}), 404

@app.route("/api/cart/<int:cid>/add", methods=["POST"])
def add_to_cart(cid):
    data = request.json
    item_id = data["item_id"]
    qty = data["qty"]
    for c in customers:
        if c.customer_id == cid:
            for i in items:
                if i.item_id == item_id:
                    if i.qty_in_stock < qty:
                        return jsonify({"error": "Insufficient stock"}), 400
                    for cart_item in c.cart:
                        if cart_item.item_id == item_id:
                            c.bill -= i.unit_price * cart_item.qty
                            cart_item.qty = qty
                            c.bill += i.unit_price * qty
                            return jsonify({"message": "Cart updated"})
                    c.cart.append(CartItem(item_id, qty))
                    c.bill += i.unit_price * qty
                    return jsonify({"message": "Item added to cart"})
            return jsonify({"error": "Item not found"}), 404
    return jsonify({"error": "Customer not found"}), 404

@app.route("/api/cart/<int:cid>/remove/<int:iid>", methods=["DELETE"])
def remove_from_cart(cid, iid):
    for c in customers:
        if c.customer_id == cid:
            for cart_item in c.cart:
                if cart_item.item_id == iid:
                    for i in items:
                        if i.item_id == iid:
                            c.bill -= i.unit_price * cart_item.qty
                    c.cart = [x for x in c.cart if x.item_id != iid]
                    return jsonify({"message": "Item removed from cart"})
            return jsonify({"error": "Item not in cart"}), 404
    return jsonify({"error": "Customer not found"}), 404

@app.route("/api/cart/<int:cid>/confirm", methods=["POST"])
def confirm_order(cid):
    data = request.json
    for c in customers:
        if c.customer_id == cid:
            if not c.cart:
                return jsonify({"error": "Cart is empty"}), 400
            for cart_item in c.cart:
                for i in items:
                    if i.item_id == cart_item.item_id:
                        i.qty_in_stock -= cart_item.qty
                        i.sold_qty += cart_item.qty
            c.order_status = 1
            c.points += 1
            c.order_day   = data.get("day",   1)
            c.order_month = data.get("month", 1)
            c.order_year  = data.get("year",  2025)
            return jsonify({"message": "Order confirmed!", "bill": c.bill})
    return jsonify({"error": "Customer not found"}), 404

# --- REPORTS ---
@app.route("/api/reports", methods=["GET"])
def get_reports():
    total_orders    = sum(1 for c in customers if c.order_status == 1)
    pending_orders  = sum(1 for c in customers if c.order_status == 0 and c.cart)
    total_revenue   = sum(c.bill for c in customers if c.order_status == 1)
    most_demanded   = max(items, key=lambda i: i.sold_qty, default=None)
    return jsonify({
        "total_orders":   total_orders,
        "pending_orders": pending_orders,
        "total_revenue":  total_revenue,
        "most_demanded_item": most_demanded.name if most_demanded else "N/A",
        "most_demanded_qty":  most_demanded.sold_qty if most_demanded else 0,
        "total_customers": len(customers),
        "total_items":     len(items),
        "total_suppliers": len(suppliers),
    })

if __name__ == "__main__":
    app.run(debug=True)