query_test_insert_with_static_values = """
INSERT INTO dbo.Test (Nume, Varsta, Sex)
VALUES ('Denis', 25, 'M')
"""


query_test_insert_with_params = ["""
INSERT INTO dbo.Test (Nume, Varsta, Sex)
VALUES (?, ?, ?)
""", ('Denisa', '45', 'F')]
