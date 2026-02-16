USE [KB_Project_Dev]
GO

/****** Object:  StoredProcedure [dbo].[usp_Report_Compliance_SQL_Version]    Script Date: 16-Feb-26 16:18:07 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

/****************************************************
-- Author:		UDR
-- Create date: 16.02.2026
-- Description:	Compliance report 
-- Example:     EXEC [dbo].[usp_Report_Compliance_SQL_Version]
-- REVISION:

Ver			      Date              Author              Description
----------		  ----------		----------          -------------------
1                 16.02.2026        UDR                 Initial version
*****************************************************/
CREATE PROCEDURE [dbo].[usp_Report_Compliance_SQL_Version]
AS

BEGIN
    SET NOCOUNT ON;

    EXEC msdb.dbo.sp_send_dbmail
        @profile_name = 'Test_Profile',
        @recipients = 'razvandenisudila@gmail.com',
        @subject = 'Server Compliance Report',
        @body = 'Attached is the latest compliance report.',
        @query = 'SELECT * FROM dbo.ServerCompliance',
        @execute_query_database = 'KB_Project_Dev',
        @attach_query_result_as_file = 1,
        @query_attachment_filename = 'ComplianceReport.csv',
        @query_result_separator = ',',
        @query_result_no_padding = 1,
        @query_result_header = 1;
END

GO


