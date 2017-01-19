# -*- coding: utf-8 -*-

# INHERITANCE MODELS FROM OTHER MODULE
# ----------------------------------------------------------
from . import contract_inherit

# BASIC MODELS
# ----------------------------------------------------------
from . import budget, budget_history, budget_plan, \
    cost_center, account_code # budget_investment_area

# BASIC MODELS FROM FIRST BECAUSE WE ARE INHERITING
# TO THE BASIC MODELS IN THIS MODULE

# INHERITANCE MODELS
# ----------------------------------------------------------
from . import budget_inherit_operation, budget_inherit_project, \
    budget_history_inherit_operation, budget_history_inherit_project, \
    budget_plan_inherit_operation, budget_plan_inherit_project
