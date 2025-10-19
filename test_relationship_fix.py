#!/usr/bin/env python3
"""
Test script to verify the fix for the AmbiguousForeignKeysError
"""
import sys
import os

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(__file__))

try:
    # Import the models to test if the relationships are properly defined
    from app.models.type_work_children import TypeWorkChildren
    from app.models.calendar.appointments import Appointments
    from app.db.base import appointments_work_type_children
    
    print("SUCCESS: Models imported without AmbiguousForeignKeysError")
    print(f"Association table: {appointments_work_type_children}")
    print(f"TypeWorkChildren relationship: {TypeWorkChildren.appointments}")
    print(f"Appointments relationship: {Appointments.work_type}")
    
except Exception as e:
    print(f"ERROR: {type(e).__name__}: {e}")
    sys.exit(1)