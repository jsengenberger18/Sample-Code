import sys

try:
    import MySQLdb
    hasSQL = True
    print("import mysql-python")
except:
    hasSQL = False
    print("MySQL missing")

class Family:

    # Instantiate a Family
    def __init__ (self, inID):
        self.familyID = inID
        self.drivers = []
        self.cars = []
        self.trucks = []
    
    # Add an Instantiated Driver
    def addDriver (self, newDriver):
        self.drivers.append(newDriver)

    # Add an Instantiated Car
    def addCar (self, newCar):
        self.cars.append(newCar)
    
    # Add an Instantiated Truck
    def addTruck (self, newTruck):
        self.trucks.append(newTruck)
    
    # Print Attributes and Objects
    def printInfo (self):

        print("---------------------")
        print("Family ID: " + self.familyID)
        print("---------------------")

        if self.drivers:
            for driver in self.drivers:
                driver.printInfo()
                print("---------------------")
        else:
            print("Empty")
            print("---------------------")

        if self.cars:
            for car in self.cars:
                car.printInfo()
                print("---------------------")
        else:
            print("Empty")
            print("---------------------")

        if self.trucks:
            for truck in self.trucks:
                truck.printInfo()
                print("---------------------")
        else:
            print("Empty")
            print("---------------------")

class Driver:
    
    # Instantiate a Driver
    def __init__(self, driverID, firstName, lastName):
        self.driverID = driverID
        self.firstName = firstName
        self.lastName = lastName
    
    # Print Attributes
    def printInfo(self):
        
        print("Driver ID: " + self.driverID)
        print("First Name: " + self.firstName)
        print("Last Name: " + self.lastName)

class Car:

    # Instantiate a Car
    def __init__(self, vehicleID, make, model, year, manual, hatchback):
        self.vehicleID = vehicleID
        self.make = make
        self.model = model
        self.year = year
        self.manual = manual
        self.hatchback = hatchback
    
    # Print Attributes
    def printInfo(self):
        
        print("Vehicle ID: " + self.vehicleID)
        print("Make: " + self.make)
        print("Model: " + self.model)
        print("Year: " + str(self.year))
        print("Manual: " + str(self.manual))
        print("Hatchback: " + str(self.hatchback))

class Truck:

    # Instantiate a Truck
    def __init__(self, vehicleID, make, model, year, towingCapacity, fourDrive):
        self.vehicleID = vehicleID
        self.make = make
        self.model = model
        self.year = year
        self.towingCapacity = towingCapacity
        self.fourDrive = fourDrive
    
    # Print Attributes
    def printInfo(self):

        print("Vehicle ID: " + self.vehicleID)
        print("Make: " + self.make)
        print("Model: " + self.model)
        print("Year: " + str(self.year))
        print("Towing Capacity: " + str(self.towingCapacity))
        print("Four Drive: " + str(self.fourDrive))

def main ():

    # Cars and Trucks
    vehicle1 = Car('VEHICLE1', 'FORD', 'FOCUS', 2013, False, False)
    vehicle2 = Car('VEHICLE2', 'SUBARU', 'OUTBACK', 2008, True, True)
    vehicle3 = Truck('VEHICLE3', 'CHEVROLET', 'COLORADO', 2019, 5000, True)
    vehicle4 = Truck('VEHICLE4', 'TOYOTA', 'TACOMA', 2012, 2000, False)

    # Drivers
    driver1 = Driver ('DRIVER1', 'Justin', 'Sengenberger')
    driver2 = Driver ('DRIVER2', 'Rebekah', 'Sengenberger')
    driver3 = Driver ('DRIVER3', 'Jaydan', 'Uetz')

    # Family #1
    family1 = Family ("FAMILY1")
    family1.addDriver (driver1)
    family1.addDriver (driver2)
    family1.addCar (vehicle1)
    family1.addTruck (vehicle3)
    family1.addTruck (vehicle4)

    # Family #2
    family2 = Family ("FAMILY2")
    family2.addDriver (driver3)
    family2.addCar (vehicle2)
    
    # Print Object-Oriented Family Information
    family1.printInfo()
    print()
    family2.printInfo()

    # # # # # # # # # # # # # # # # # # # # # # # # # #
    # Create Mock DB Connection
    # # # # # # # # # # # # # # # # # # # # # # # # # #

    if not hasSQL:
        print("MySQLdb Library Required")
    else:
        try:
            myDB = MySQLdb.connect("""host, user, password, database""")
            cursor = myDB.cursor()
        except:
            print("Invalid DB Info... Exiting Program")
            sys.exit(1)

        # # # # # # # # # # # # # # # # # # # # # # # # # #
        # Add SQL 'CREATE' commands into a Python string
        # # # # # # # # # # # # # # # # # # # # # # # # # #

        # Create Family_Table
        sql = """CREATE TABLE 'Family_Table' (
            'FamilyID' varchar(255) NOT NULL,
            'FirstName' varchar(255) NOT NULL,
            'LastName' varchar(255) NOT NULL

        PRIMARY KEY ('FamilyID')
        ) DEFAULT CHARSET=utf8mb4
        """

        # Create Driver_Table
        sql += """CREATE TABLE 'Driver_Table' (
            'DriverID' varchar(255) NOT NULL,
            'FamilyID' varchar(255) NOT NULL

        PRIMARY KEY ('DriverID')
        FOREIGN KEY ('FamilyID')
        ) DEFAULT CHARSET=utf8mb4
        """

        # Create Car_Table
        sql += """CREATE TABLE 'Car_Table' (
            'VehicleID' varchar(255) NOT NULL,
            'FamilyID' varchar(255) NOT NULL,
            'Make' varchar(255) NOT NULL,
            'Model' varchar(255) NOT NULL,
            'Year' int(4) NOT NULL,
            'Manual' bool NOT NULL,
            'Hatchback' bool NOT NULL

        PRIMARY KEY ('VehicleID')
        FOREIGN KEY ('FamilyID')
        ) DEFAULT CHARSET=utf8mb4
        """

        # Create Truck_Table
        sql += """CREATE TABLE 'Truck_Table' (
            'VehicleID' varchar(255) NOT NULL,
            'FamilyID' varchar(255) NOT NULL,
            'Make' varchar(255) NOT NULL,
            'Model' varchar(255) NOT NULL,
            'Year' int(4) NOT NULL,
            'TowingCapacity' int(5) NOT NULL,
            'FourDrive' bool NOT NULL

        PRIMARY KEY ('VehicleID')
        FOREIGN KEY ('FamilyID')
        ) DEFAULT CHARSET=utf8mb4
        """

        # Execute Commands & Commit Changes
        cursor.execute(sql)
        myDB.commit()

        # # # # # # # # # # # # # # # # # # # # # # # # # #
        # Insert Data into Mock Tables
        # Add SQL 'INSERT' commands into a Python string
        # # # # # # # # # # # # # # # # # # # # # # # # # #

        # Insert Each Family into DB
        families = list (family1, family2)
        for family in families:

            # Insert FamilyID
            sql = "INSERT INTO FamilyTable (FamilyID) VALUES ("
            sql += family.familyID + ");"
            
            # Insert Drivers
            for driver in family.drivers:
                sql += "INSERT INTO DriverTable (DriverID, FamilyID, FirstName, LastName) VALUES ("
                sql += driver.driverID + ', ' + family.familyID + ', ' + driver.firstName + ', ' + driver.lastName + ');'
            
            # Insert Cars
            for car in family.cars:
                sql += "INSERT INTO DriverTable (VehicleID, FamilyID, Make, Model, Year, Manual, Hatchback) VALUES ("
                sql += car.vehicleID + ', ' + family.familyID + ', ' + car.make + ', ' + car.model + car.year + ', ' + car.manual + car.hatchback + ');'
            
            # Insert Trucks
            for truck in family.trucks:
                sql += "INSERT INTO DriverTable (VehicleID, FamilyID, Make, Model, Year, TowingCapacity, FourDrive) VALUES ("
                sql += truck.vehicleID + ', ' + family.familyID + ', ' + truck.make + ', ' + truck.model + truck.year + ', ' + truck.towingCapacity + truck.fourDrive + ');'
        
        print("SQL to Commit: ")
        print(sql)

        # Execute Commands & Commit Changes
        cursor.execute(sql)
        myDB.commit()

        # Close DB Connections
        cursor.close()
        myDB.close()

if __name__ == "__main__":
    main()