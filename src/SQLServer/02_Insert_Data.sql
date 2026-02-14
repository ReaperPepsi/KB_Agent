-- Insert test values for customer
USE [KB_Project_Dev]
INSERT INTO Test_Customer VALUES
(1, 'GymBeam', 'Gym suppliments'),
(2, 'GymOne', 'Sport industry (Gym)'),
(3, 'Emag', 'E-Commerce')


-- Insert the corresponding values for status catalog
USE KB_Project_Dev
INSERT INTO tbl_Status_Catalog VALUES
(1, 'Removed'),
(2, 'Active'),
(3, 'Transffered'),
(4, 'New')


-- Define environment catalog: 1 - > Production, 2 - > Test, 3 - > Development
USE [KB_Project_Dev]
INSERT INTO tbl_Environment_Catalog VALUES
(1, 'Production'),
(2, 'Test'),
(3, 'Development')

-- Define backup tools: 1 - > Networker, 2 - > Avamar, 3 - > SnapCenter, 4 - > SQL Server Native Backup
USE [KB_Project_Dev]
INSERT INTO tbl_Backup_Catalog VALUES
(1, 'Networker'),
(2, 'Avamar'),
(3, 'SnapCenter'),
(4, 'SQL Server Native Backup')


-- Version catalog insert based on the Python extracted Data (KB_Test)
INSERT INTO [dbo].[tbl_Version_Catalog] (KB_String,Major_Version, Minor_Version, Build_Number, Revision_Number,Release_Date)
SELECT 
    KB AS KBString,
    PARSENAME(KB,4) AS MajorVersion,
    PARSENAME(KB,3) AS MinorVersion,
    PARSENAME(KB,2) AS BuildNumber,
    PARSENAME(KB,1) AS RevisionNumber,
    Release_Date
FROM KB_Test


-- Insert test values for a single customer
INSERT INTO [dbo].[tbl_serverlist]
(
    tbl_serverlist_customer_id,
    tbl_serverlist_instance_name,
    tbl_serverlist_instance_ip,
    tbl_serverlist_status_id,
    tbl_serverlist_sql_version,
    tbl_serverlist_sql_edition,
    tbl_serverlist_environment_id,
    tbl_serverlist_backup_id
)
SELECT
    1,                                      -- customer ID static
    'GMB001\SuppTest',                    -- instance name static
    '10.0.0.5',                             -- IP static
    2,                                      -- status ID static (ex: Active)
    vc.ID,                                   -- FK towards VersionCatalog
    CASE 
        WHEN vc.KB_String LIKE '17.%' THEN 'SQL Server 2025'
        WHEN vc.KB_String LIKE '16.%' THEN 'SQL Server 2022'
        WHEN vc.KB_String LIKE '15.%' THEN 'SQL Server 2019'
        WHEN vc.KB_String LIKE '14.%' THEN 'SQL Server 2017'
        WHEN vc.KB_String LIKE '13.%' THEN 'SQL Server 2016'
        WHEN vc.KB_String LIKE '12.%' THEN 'SQL Server 2014'
        ELSE 'SQL Server Older'
    END,
    1,                                      -- environment ID static
    1                                       -- backup type ID static
FROM [dbo].[tbl_Version_Catalog] vc
WHERE vc.KB_String = '17.0.1000.7';         -- test version