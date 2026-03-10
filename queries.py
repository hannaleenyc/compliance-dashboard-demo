# queries.py 

GET_COMPLIANCE = f'''
                    SELECT *
                    FROM StreetSolutions.dbo.SHS_Weekly_PMO_Compliance_vw

                    '''

GET_PMO_DATA = f'''--CREATE OR ALTER VIEW SHS_Weekly_PMO_Additional_Info_vw as

                    WITH weekly_pmo as (SELECT v1.ID,
                        v1.ResponderName, 
                        v1.Dateofsubmission, 
                        v1.FacilityType, 
                        v1.SiteName, 
                        v2.Facility_CD, 
                        v2.PA,
                        v1.SiteHasPMO, 
                        v1.ClientFirstName, 
                        v1.ClientLastName,
                        TRY_CAST(REPLACE(v1.CARESId, ' ', '') AS INT) AS CARESID_int,
                        v1.StreetSmartId,
                        v1.TargetMoveOutDate, 
                        v1.Exit_Reason, 
                        v1.MOProgress_Detail, 
                        v1.CaseProvider, 
                        v1.StartOfWeek, 
                        v1.EndOfWeek, 
                        v1.WeekPeriod, 
                        v1.DayofSubmission, 
                        v1.Late_Submission_FLG
                    FROM StreetSolutions.dbo.SHS_Weekly_PMO_Stg v1
                    LEFT JOIN StreetSolutions.dbo.SHS_ProjectedMoveOut_CodeTable v2 on v1.siteName = v2.List_of_Sites_SHS_Portfolio
                    ), 
                    table_v1 as (SELECT t1.*,
                        t2.Facility_Name, 
                        t2.Facility_CD as Facility_CD_LP, 
                        t2.Placement_Start_DTTM, 
                        t2.Exit_DTTM, 
                        t2.Exit_Reason as Exit_Reason_LP,
                        CASE WHEN (EXISTS (SELECT t2.Facility_CD
                                            FROM StreetSolutions.dbo.SHSFacility_Dec25 t3
                                            WHERE t2.Facility_CD = t3.Facility_CD
                                            ) OR (t2.Facility_CD IS NULL))
                                            THEN 'N/A'
                                            ELSE 'Y'
                                        END AS Latest_Exit_Elsewhere_FLG
                    FROM weekly_pmo t1
                    LEFT JOIN StreetSolutions.dbo.Latest_EDW_Placements_Fct t2 on t1.CARESID_int = t2.CARES_ID
                    ), 
                    table_v2 as (SELECT *, 
                    CASE WHEN Latest_Exit_Elsewhere_FLG = 'Y'
                    AND Placement_Start_DTTM > DateofSubmission 
                    THEN 'Y'
                    ELSE 'N'
                    END AS Reentered_system_FLG, 
                    CASE WHEN Latest_Exit_Elsewhere_FLG = 'Y'
                    AND FacilityType NOT IN ('Drop-in Center', 'Outreach Team')
                    THEN 'Y'
                    ELSE 'N'
                    END AS Error_FLG
                    FROM table_v1 
                    ), 
                    additional_info as (SELECT ID, 
                        Latest_Exit_Elsewhere_FLG, 
                        Reentered_system_FLG, 
                        Error_FLG
                    FROM table_v2
                    )
                    SELECT *
                    FROM table_v2
                    ORDER BY DateofSubmission DESC

                    '''
    
GET_REENTRY_DATA = '''WITH weekly_pmo as (SELECT v1.ID,
                        v1.ResponderName, 
                        v1.Dateofsubmission, 
                        v1.FacilityType, 
                        v1.SiteName, 
                        v2.Facility_CD, 
                        v2.PA,
                        v1.SiteHasPMO, 
                        v1.ClientFirstName, 
                        v1.ClientLastName,
                        TRY_CAST(REPLACE(v1.CARESId, ' ', '') AS INT) AS CARESID_int,
                        v1.StreetSmartId,
                        v1.TargetMoveOutDate, 
                        v1.Exit_Reason, 
                        v1.MOProgress_Detail, 
                        v1.CaseProvider, 
                        v1.StartOfWeek, 
                        v1.EndOfWeek, 
                        v1.WeekPeriod, 
                        v1.DayofSubmission, 
                        v1.Late_Submission_FLG
                    FROM StreetSolutions.dbo.SHS_Weekly_PMO_Stg v1
                    LEFT JOIN StreetSolutions.dbo.SHS_ProjectedMoveOut_CodeTable v2 on v1.siteName = v2.List_of_Sites_SHS_Portfolio
                    ), 
                    table_v1 as (SELECT t1.*,
                        t2.Facility_Name, 
                        t2.Facility_CD as Facility_CD_LP, 
                        t2.Placement_Start_DTTM, 
                        t2.Exit_DTTM, 
                        t2.Exit_Reason as Exit_Reason_LP,
                        CASE WHEN (EXISTS (SELECT t2.Facility_CD
                                            FROM StreetSolutions.dbo.SHSFacility_Dec25 t3
                                            WHERE t2.Facility_CD = t3.Facility_CD
                                            ) OR (t2.Facility_CD IS NULL))
                                            THEN 'N/A'
                                            ELSE 'Y'
                                        END AS Latest_Exit_Elsewhere_FLG
                    FROM weekly_pmo t1
                    LEFT JOIN StreetSolutions.dbo.Latest_EDW_Placements_Fct t2 on t1.CARESID_int = t2.CARES_ID
                    ), 
                    table_v2 as (SELECT *, 
                    CASE WHEN Latest_Exit_Elsewhere_FLG = 'Y'
                    AND Placement_Start_DTTM > DateofSubmission 
                    THEN 'Y'
                    ELSE 'N'
                    END AS Reentered_system_FLG, 
                    CASE WHEN Latest_Exit_Elsewhere_FLG = 'Y'
                    AND FacilityType NOT IN ('Drop-in Center', 'Outreach Team')
                    THEN 'Y'
                    ELSE 'N'
                    END AS Error_FLG
                    FROM table_v1 
                    ), 
                    additional_info as (SELECT ID, 
                        Latest_Exit_Elsewhere_FLG, 
                        Reentered_system_FLG, 
                        Error_FLG
                    FROM table_v2
                    )
                    SELECT *
                    FROM table_v2
                    WHERE Reentered_System_FLG = 'Y'
                    ORDER BY DateofSubmission DESC

                    '''

    
