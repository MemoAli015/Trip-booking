import tkinter as tk
from tkinter import messagebox, ttk


def load_data(file_name):
    try:
        with open(file_name, 'r') as file:
            return [line.strip().split(',') for line in file.readlines()]
    except FileNotFoundError:
        return []

def save_data(file_name, data):
    with open(file_name, 'w') as file:
        for entry in data:
            file.write(','.join(entry) + '\n')


hotels = load_data('hotels.txt')
flights = load_data('flights.txt')
users = load_data('users.txt')  
cart = []

class User:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.cart = []

class Admin(User):
    def __init__(self, email, password):
        super().__init__(email, password)
    
    
    def add_hotel(self, hotel):
        hotels.append(hotel)
        save_data('hotels.txt', hotels)

    def add_flight(self, flight):
        flights.append(flight)
        save_data('flights.txt', flights)

    def edit_hotel(self, index, new_data):
        hotels[index] = new_data
        save_data('hotels.txt', hotels)

    def edit_flight(self, index, new_data):
        flights[index] = new_data
        save_data('flights.txt', flights)

    def delete_hotel(self, index):
        del hotels[index]
        save_data('hotels.txt', hotels)

    def delete_flight(self, index):
        del flights[index]
        save_data('flights.txt', flights)

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tour Booking System")
        self.geometry("500x500")
        self.current_user = None
        
        self.login_screen()
    
    
    def login_screen(self):
        self.clear_frame()
        
        tk.Label(self, text="Email:").pack()
        email_entry = tk.Entry(self)
        email_entry.pack()

        tk.Label(self, text="Password:").pack()
        password_entry = tk.Entry(self, show="*")
        password_entry.pack()

        def login():
            email = email_entry.get()
            password = password_entry.get()
            for user in users:
                if user[0] == email and user[1] == password:
                    if email == 'admin':
                        self.current_user = Admin(email, password)
                    else:
                        self.current_user = User(email, password)
                    self.main_screen()
                    return
            messagebox.showerror("Error", "Invalid email or password")

        tk.Button(self, text="Login", command=login).pack()
        tk.Button(self, text="Register", command=self.register_screen).pack()

    
    def register_screen(self):
        self.clear_frame()

        tk.Label(self, text="New email:").pack()
        email_entry = tk.Entry(self)
        email_entry.pack()

        tk.Label(self, text="New password:").pack()
        password_entry = tk.Entry(self, show="*")
        password_entry.pack()

        def register():
            email = email_entry.get()
            password = password_entry.get()
            for user in users:
                if user[0] == email:
                    messagebox.showerror("Error", "This email is already registered")
                    return
            users.append([email, password])
            save_data('users.txt', users)
            messagebox.showinfo("Registration", "Registration successful!")
            self.login_screen()

        tk.Button(self, text="Register", command=register).pack()
        tk.Button(self, text="Back", command=self.login_screen).pack()

   
    def main_screen(self):
        self.clear_frame()

        if isinstance(self.current_user, Admin):
            tk.Label(self, text="Admin Panel").pack()
        else:
            tk.Label(self, text="User Panel").pack()

        tk.Button(self, text="Hotels", command=self.hotel_screen).pack()
        tk.Button(self, text="Flights", command=self.flight_screen).pack()
        tk.Button(self, text="Cart", command=self.cart_screen).pack()

    
    def hotel_screen(self):
        self.clear_frame()
        tk.Label(self, text="Available Hotels").pack()

        tk.Label(self, text="Sort By:").pack()
        tk.Button(self, text="Name", command=lambda: self.sort_hotels("name")).pack()
        tk.Button(self, text="Price", command=lambda: self.sort_hotels("price")).pack()

        tk.Label(self, text="Search:").pack()
        search_entry = tk.Entry(self)
        search_entry.pack()
        tk.Button(self, text="Search", command=lambda: self.search_hotels(search_entry.get())).pack()

        for index, hotel in enumerate(hotels):
            hotel_info = f"Name: {hotel[0]}, Price: {hotel[1]}, Location: {hotel[2]}"
            tk.Label(self, text=hotel_info).pack()

            if isinstance(self.current_user, Admin):
                tk.Button(self, text="Edit", command=lambda i=index: self.edit_hotel(i)).pack()
                tk.Button(self, text="Delete", command=lambda i=index: self.delete_hotel(i)).pack()
            else:
                tk.Button(self, text="Add to Cart", command=lambda h=hotel: self.add_to_cart(h)).pack()

        if isinstance(self.current_user, Admin):
            tk.Button(self, text="Add New Hotel", command=self.add_hotel).pack()
        tk.Button(self, text="Back", command=self.main_screen).pack()

    def flight_screen(self):
        self.clear_frame()
        tk.Label(self, text="Available Flights").pack()

        tk.Label(self, text="Sort By:").pack()
        tk.Button(self, text="From", command=lambda: self.sort_flights("from")).pack()
        tk.Button(self, text="Price", command=lambda: self.sort_flights("price")).pack()

        tk.Label(self, text="Search:").pack()
        search_entry = tk.Entry(self)
        search_entry.pack()
        tk.Button(self, text="Search", command=lambda: self.search_flights(search_entry.get())).pack()

        for index, flight in enumerate(flights):
            flight_info = f"From: {flight[0]}, To: {flight[1]}, Date: {flight[2]}, Price: {flight[3]}"
            tk.Label(self, text=flight_info).pack()

            if isinstance(self.current_user, Admin):
                tk.Button(self, text="Edit", command=lambda i=index: self.edit_flight(i)).pack()
                tk.Button(self, text="Delete", command=lambda i=index: self.delete_flight(i)).pack()
            else:
                tk.Button(self, text="Add to Cart", command=lambda f=flight: self.add_to_cart(f)).pack()

        if isinstance(self.current_user, Admin):
            tk.Button(self, text="Add New Flight", command=self.add_flight).pack()
        tk.Button(self, text="Back", command=self.main_screen).pack()

    
    def cart_screen(self):
        self.clear_frame()
        tk.Label(self, text="Your Cart").pack()
        for item in cart:
            tk.Label(self, text=f"Item: {item[0]}, Price: {item[1]}").pack()
        tk.Button(self, text="Buy", command=self.buy_items).pack()
        tk.Button(self, text="Back", command=self.main_screen).pack()

    
    def edit_hotel(self, index):
        self.clear_frame()
        tk.Label(self, text="Edit Hotel").pack()

        def save_changes():
            new_name = name_entry.get()
            new_price = price_entry.get()
            new_location = location_entry.get()
            new_data = [new_name, new_price, new_location]
            self.current_user.edit_hotel(index, new_data)
            self.hotel_screen()

        hotel = hotels[index]
        tk.Label(self, text="Name:").pack()
        name_entry = tk.Entry(self)
        name_entry.insert(0, hotel[0])
        name_entry.pack()

        tk.Label(self, text="Price:").pack()
        price_entry = tk.Entry(self)
        price_entry.insert(0, hotel[1])
        price_entry.pack()

        tk.Label(self, text="Location:").pack()
        location_entry = tk.Entry(self)
        location_entry.insert(0, hotel[2])
        location_entry.pack()

        tk.Button(self, text="Save Changes", command=save_changes).pack()
        tk.Button(self, text="Back", command=self.hotel_screen).pack()

        

    def delete_hotel(self, index):
        hotels.pop(index)
        save_data('hotels.txt', hotels)
        self.hotel_screen()

    def add_hotel(self):
        self.clear_frame()
        tk.Label(self, text="Add New Hotel").pack()

        def save_hotel():
            name = name_entry.get()
            price = price_entry.get()
            location = location_entry.get()
            hotel = [name, price, location]
            self.current_user.add_hotel(hotel)
            self.hotel_screen()

        tk.Label(self, text="Name:").pack()
        name_entry = tk.Entry(self)
        name_entry.pack()

        tk.Label(self, text="Price:").pack()
        price_entry = tk.Entry(self)
        price_entry.pack()

        tk.Label(self, text="Location:").pack()
        location_entry = tk.Entry(self)
        location_entry.pack()

        tk.Button(self, text="Add Hotel", command=save_hotel).pack()
        tk.Button(self, text="Back", command=self.hotel_screen).pack()


    def edit_flight(self, index):
        self.clear_frame()
        tk.Label(self, text="Edit Flight").pack()

        def save_changes():
            new_from = from_entry.get()
            new_to = to_entry.get()
            new_date = date_entry.get()
            new_price = price_entry.get()
            new_data = [new_from, new_to, new_date, new_price]
            self.current_user.edit_flight(index, new_data)
            self.flight_screen()

        flight = flights[index]
        tk.Label(self, text="From:").pack()
        from_entry = tk.Entry(self)
        from_entry.insert(0, flight[0])
        from_entry.pack()

        tk.Label(self, text="To:").pack()
        to_entry = tk.Entry(self)
        to_entry.insert(0, flight[1])
        to_entry.pack()

        tk.Label(self, text="Date:").pack()
        date_entry = tk.Entry(self)
        date_entry.insert(0, flight[2])
        date_entry.pack()

        tk.Label(self, text="Price:").pack()
        price_entry = tk.Entry(self)
        price_entry.insert(0, flight[3])
        price_entry.pack()

        tk.Button(self, text="Save Changes", command=save_changes).pack()
        tk.Button(self, text="Back", command=self.flight_screen).pack()


    def delete_flight(self, index):
        flights.pop(index)
        save_data('flights.txt', flights)
        self.flight_screen()

    def add_flight(self):
        self.clear_frame()
        tk.Label(self, text="Add New Flight").pack()

        def save_flight():
            from_city = from_entry.get()
            to_city = to_entry.get()
            date = date_entry.get()
            price = price_entry.get()
            flight = [from_city, to_city, date, price]
            self.current_user.add_flight(flight)
            self.flight_screen()

        tk.Label(self, text="From:").pack()
        from_entry = tk.Entry(self)
        from_entry.pack()

        tk.Label(self, text="To:").pack()
        to_entry = tk.Entry(self)
        to_entry.pack()

        tk.Label(self, text="Date:").pack()
        date_entry = tk.Entry(self)
        date_entry.pack()

        tk.Label(self, text="Price:").pack()
        price_entry = tk.Entry(self)
        price_entry.pack()

        tk.Button(self, text="Add Flight", command=save_flight).pack()
        tk.Button(self, text="Back", command=self.flight_screen).pack()


    def add_to_cart(self, item):
        cart.append(item)

    def buy_items(self):
        messagebox.showinfo("Purchase", "Items purchased successfully!")
        cart.clear()

    
    def clear_frame(self):
        for widget in self.winfo_children():
            widget.destroy()

    def sort_hotels(self, criteria):
        if criteria == "name":
            hotels.sort(key=lambda x: x[0])
        elif criteria == "price":
            hotels.sort(key=lambda x: float(x[1]))
        save_data('hotels.txt', hotels)
        self.hotel_screen()

    def sort_flights(self, criteria):
        if criteria == "from":
            flights.sort(key=lambda x: x[0])
        elif criteria == "price":
            flights.sort(key=lambda x: float(x[3]))
        save_data('flights.txt', flights)
        self.flight_screen()

    def search_hotels(self, query):
        filtered_hotels = [hotel for hotel in hotels if query.lower() in hotel[0].lower()]
        self.display_search_results(filtered_hotels, "Hotels")

    def search_flights(self, query):
        filtered_flights = [flight for flight in flights if query.lower() in flight[0].lower() or query.lower() in flight[1].lower()]
        self.display_search_results(filtered_flights, "Flights")

    def display_search_results(self, results, type_):
        self.clear_frame()
        tk.Label(self, text=f"Search Results for {type_}").pack()
        for entry in results:
            if type_ == "Hotels":
                info = f"Name: {entry[0]}, Price: {entry[1]}, Location: {entry[2]}"
            else:
                info = f"From: {entry[0]}, To: {entry[1]}, Date: {entry[2]}, Price: {entry[3]}"
            tk.Label(self, text=info).pack()
        tk.Button(self, text="Back", command=self.main_screen).pack()


app = App()
app.mainloop()
