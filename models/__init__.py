# -*- coding: utf-8 -*-

# BASIC MODELS
# ----------------------------------------------------------
from . import budget, budget_history, tag

# BASIC MODELS FROM FIRST BECAUSE WE ARE INHERITING
# TO THE BASIC MODELS IN THIS MODULE

# INHERITANCE MODELS
# ----------------------------------------------------------
from . import budget_inherit_operation, budget_inherit_project, \
              budget_history_inherit_project, budget_history_inherit_operation
