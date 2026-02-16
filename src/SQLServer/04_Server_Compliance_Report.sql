USE [KB_Project_Dev]
GO

/****** Object:  View [dbo].[ServerCompliance]    Script Date: 16-Feb-26 16:16:27 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO


-- Create a View for the regular repport
-- It must contain ServerName/instance name, current version of sql, Customer name, status, server compliance

CREATE VIEW [dbo].[ServerCompliance] as 
WITH Latest_Version AS
(
    SELECT
        Major_Version,
        Minor_Version,
        Build_Number,
        Revision_Number,
        kb_string
    FROM
    (
        SELECT *,
               ROW_NUMBER() OVER
               (
                   PARTITION BY Major_Version
                   ORDER BY
                       Major_Version DESC,
                       Minor_Version DESC,
                       Build_Number DESC,
                       Revision_Number DESC
               ) AS rn
        FROM tbl_Version_Catalog
    ) V
    WHERE rn = 1
)

SELECT  CST.customer_name,
        SRV.tbl_serverlist_instance_name AS [Instance Name],
        SRV.tbl_serverlist_instance_ip AS [Instance IP], 
        VRS.KB_String AS [Current Version], 
        LST.KB_String AS [Target KB],
CASE 
    WHEN 
        VRS.Major_Version < LST.Major_Version
        OR (VRS.Major_Version = LST.Major_Version AND VRS.Minor_Version < LST.Minor_Version)
        OR (VRS.Major_Version = LST.Major_Version AND VRS.Minor_Version = LST.Minor_Version AND VRS.Build_Number < LST.Build_Number)
        OR (VRS.Major_Version = LST.Major_Version AND VRS.Minor_Version = LST.Minor_Version 
            AND VRS.Build_Number = LST.Build_Number AND VRS.Revision_Number < LST.Revision_Number)
        THEN 'Not Compliant'
    ELSE 'Compliant'
END AS [Server Compliance]
FROM tbl_serverlist SRV
INNER JOIN Test_Customer CST on SRV.tbl_serverlist_customer_id = CST.customer_id
INNER JOIN tbl_Version_Catalog VRS
ON SRV.tbl_serverlist_sql_version = VRS.ID
INNER JOIN Latest_Version LST ON VRS.Major_Version = LST.Major_Version
WHERE SRV.tbl_serverlist_status_id IN (2, 4) -- Active and New instance
GO


