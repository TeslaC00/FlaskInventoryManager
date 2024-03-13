show databases;
use mock;
-- Create Suppliers Table
CREATE TABLE Suppliers (
    SupplierID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(255),
    GSTNumber VARCHAR(20),
    Address TEXT
);

-- Create Clients Table
CREATE TABLE Clients (
    ClientID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(255),
    GSTNumber VARCHAR(20),
    Address TEXT
);

-- Create RawMaterials Table
CREATE TABLE RawMaterials (
    MaterialID INT PRIMARY KEY AUTO_INCREMENT,
    PartNumber VARCHAR(50),
    Name VARCHAR(255),
    Description TEXT
);

-- Create FinishedGoods Table
CREATE TABLE FinishedGoods (
    ProductID INT PRIMARY KEY AUTO_INCREMENT,
    PartNumber VARCHAR(50),
    Name VARCHAR(255),
    Description TEXT
);

-- Create RawMaterialsUsage Table
CREATE TABLE RawMaterialsUsage (
    UsageID INT PRIMARY KEY AUTO_INCREMENT,
    ProductID INT,
    MaterialID INT,
    QuantityUsed INT,
    FOREIGN KEY (ProductID) REFERENCES FinishedGoods(ProductID),
    FOREIGN KEY (MaterialID) REFERENCES RawMaterials(MaterialID)
);

-- Create IncomingRawMaterials Table
CREATE TABLE IncomingRawMaterials (
    IncomingID INT PRIMARY KEY AUTO_INCREMENT,
    MaterialID INT,
    SupplierID INT,
    DateTime DATETIME,
    ChallanNumber VARCHAR(100),
    Quantity INT,
    Remarks TEXT,
    FOREIGN KEY (MaterialID) REFERENCES RawMaterials(MaterialID),
    FOREIGN KEY (SupplierID) REFERENCES Suppliers(SupplierID)
);

-- Create OutgoingFinishedGoods Table
CREATE TABLE OutgoingFinishedGoods (
    OutgoingID INT PRIMARY KEY AUTO_INCREMENT,
    ProductID INT,
    ClientID INT,
    DateTime DATETIME,
    InvoiceNumber VARCHAR(100),
    Quantity INT,
    PricePerUnit DECIMAL(10, 2),
    TotalCost DECIMAL(10, 2),
    CGST DECIMAL(10, 2),
    SGST DECIMAL(10, 2),
    IGST DECIMAL(10, 2),
    TotalAfterGST DECIMAL(10, 2),
    Remarks TEXT,
    FOREIGN KEY (ProductID) REFERENCES FinishedGoods(ProductID),
    FOREIGN KEY (ClientID) REFERENCES Clients(ClientID)
);

-- Create Returns Table
CREATE TABLE Returns (
    ReturnID INT PRIMARY KEY AUTO_INCREMENT,
    Type VARCHAR(255),
    PartNumber INT,
    DateTime DATETIME,
    ChallanNumber VARCHAR(100),
    Remarks TEXT
);

-- Create DailyStock Table
CREATE TABLE DailyStock (
    StockID INT PRIMARY KEY AUTO_INCREMENT,
    Date DATE,
    MaterialID INT NULL,
    ProductID INT NULL,
    Quantity INT,
    FOREIGN KEY (MaterialID) REFERENCES RawMaterials(MaterialID),
    FOREIGN KEY (ProductID) REFERENCES FinishedGoods(ProductID)
);

-- Inserting some dummy data
INSERT INTO Suppliers (Name, GSTNumber, Address) VALUES ('Supplier A', '27AAAAA0000A1Z5', '1234, Industrial Area, City A');
INSERT INTO Clients (Name, GSTNumber, Address) VALUES ('Client X', '29BBBBB0000B2Z6', '4321, Business Park, City B');
INSERT INTO RawMaterials (PartNumber, Name, Description) VALUES ('RM-001', 'Aluminium Sheet', 'High-quality aluminium sheet for manufacturing');
INSERT INTO FinishedGoods (PartNumber, Name, Description) VALUES ('FG-001', 'Aluminium Can', 'Premium aluminium can for packaging');
