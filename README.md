Budget Core
===========
Specifically Designed for Etisalat-TBPC

Summary
---------------------
- Budget
- Budget History
- Budget Recurrence
- Project (Inherit to Budget)
- Project History (Inherit to Budget History)
- Project Recurrence (Inherit to Budget Recurrence)
- Cost Center - Account Code (Inherit to Budget)
- Cost Center History (Inherit to Budget History)
- Cost Center Recurrence (Inherit to Budget Recurrence)
- Access Users
    - Budget (View All)
        - Dependent - Can readonly
        - User - General Usage except delete power, can Edit recurrence but not create
        - Manager - All power to manipulate data
    - Project
        - Dependent - Can readonly
        - User - General Usage except delete power, can Edit recurrence but not create
        - Manager - All power to manipulate data
    - Cost Center
        - Dependent - Can readonly
        - User - General Usage except delete power, can Edit recurrence but not create
        - Manager - All power to manipulate data
- Validations
    - Project
        - Project Expenditure Amount Can't be More Than Commitment Amount
        - When Transferring Expenditure/Commitment Amount, the losing amount shouldn't be negative after the operation
        - When Adding/Subtracting Expenditure/Commitment Amount, the losing amount shouldn't be negative after the operation
        - Project No must be unique
        - Recurring Amounts should be Positive
    - Cost Center - Account Code
        - When Transferring Expenditure, the losing amount shouldn't be negative after the operation
        - When Adding/Subtracting Expenditure, the losing amount shouldn't be negative after the operation
        - Cost Center - Account Code must be unique
        - Recurring Amounts should be Positive
- Tagging Feature
- Utilities
