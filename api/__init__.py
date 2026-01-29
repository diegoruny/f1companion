"""F1 Race Companion API Module

Provides data access for F1 racing information.
Supports both online (API) and offline (CSV) modes.
"""

from .csv_handler import CSVDataHandler, ErgastAPI

__all__ = ['CSVDataHandler', 'ErgastAPI']
