-- Craete Customer test table
USE [KB_Project_Dev]
CREATE TABLE Test_Customer(
customer_id int NOT NULL Primary Key,
customer_name nvarchar(50) NOT NULL,
customer_details nvarchar (200)
)

-- Create Status Catalog (3 for the moment, 0 - > removed, 1 - > active, 2 -> transffered)
USE [KB_Project_Dev]
CREATE TABLE tbl_Status_Catalog(
tbl_status_id INT NOT NULL PRIMARY KEY,
tbl_status_name NVARCHAR (30)
)


-- Version catalog
USE [KB_Project_Dev]
CREATE TABLE tbl_Version_Catalog(
ID INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
KB_STRING [nvarchar](50) NOT NULL,
Major_Version INT NOT NULL,
Minor_Version INT NOT NULL,
Build_Number INT NOT NULL,
Release_Date DATE)


-- Add revision number for granular comparisoon
ALTER TABLE tbl_Version_Catalog
ADD Revision_Number INT NOT NULL


-- Environment Catalog table
USE [KB_Project_Dev]
CREATE TABLE tbl_Environment_Catalog(
tbl_environment_id INT NOT NULL PRIMARY KEY,
tlb_environment_detail NVARCHAR (50))


-- Backup Catalog table
USE [KB_Project_Dev]
CREATE TABLE tbl_Backup_Catalog (
tbl_backup_id INT NOT NULL PRIMARY KEY,
tlb_backup_type_description NVARCHAR(100))


-- Create test serverlist based on the already customer
USE[KB_Project_Dev]

CREATE TABLE tbl_serverlist(
tbl_serverlist_id INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
tbl_serverlist_customer_id INT NOT NULL  FOREIGN KEY REFERENCES Test_Customer(customer_id), 
tbl_serverlist_instance_name NVARCHAR(50) NOT NULL,
tbl_serverlist_instance_ip NVARCHAR (50),
tbl_serverlist_status_id INT NOT NULL FOREIGN KEY REFERENCES tbl_Status_Catalog(tbl_status_id),
tbl_serverlist_sql_version INT NULL FOREIGN KEY REFERENCES tbl_Version_Catalog(ID),
tbl_serverlist_sql_edition NVARCHAR(50) NOT NULL,
tbl_serverlist_environment_id INT NOT NULL FOREIGN KEY REFERENCES tbl_Environment_Catalog(tbl_environment_id),
tbl_serverlist_backup_id INT NOT NULL FOREIGN KEY REFERENCES tbl_Backup_Catalog (tbl_backup_id)
)
GO
