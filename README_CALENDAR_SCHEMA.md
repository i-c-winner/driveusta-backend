# Calendar Schema Documentation

This document describes the database schema for the calendar functionality in the DriveUsta project.

## Overview

The calendar system consists of three main tables that are associated with WorkShop entities:
1. `appointments` - Client appointment records
2. `holidays` - Holiday records for each WorkShop
3. `working_hours` - Working hours schedule for each WorkShop

All calendar entries are linked to a specific WorkShop through the `work_shop_id` foreign key.

## Schema Details

### Appointments Table (`participants.appointments`)

Stores client appointment information.

**Columns:**
- `id` (Integer, Primary Key) - Unique identifier
- `work_shop_id` (Integer, Foreign Key) - References `work_shop.work_shop.id`
- `client_name` (String(100)) - Client's name
- `client_phone` (String(20)) - Client's phone number
- `car_license_plate` (String(10)) - Vehicle license plate
- `appointment_date` (Date) - Date of appointment
- `appointment_time` (Time) - Time of appointment
- `duration_minutes` (Integer) - Duration of service in minutes
- `time` (DateTime) - Timestamp of record creation
- `description` (String(200)) - Description of service

**Relationships:**
- Many-to-many with `cars` through `participants.appointments_cars`
- Many-to-many with `work_shop` through `participants.appointments_work_shop`
- Many-to-many with `type_work_children` through `participants.appointments_work_type_children`

### Holidays Table (`work_shop.holidays`)

Stores holiday information for each WorkShop.

**Columns:**
- `id` (Integer, Primary Key) - Unique identifier
- `work_shop_id` (Integer, Foreign Key) - References `work_shop.work_shop.id`
- `description` (String(200)) - Holiday description

**Relationships:**
- Many-to-many with `work_shop` through `work_shop.holidays_work_shops`

### Working Hours Table (`work_shop.working_hours`)

Stores working hours schedule for each WorkShop.

**Columns:**
- `id` (Integer, Primary Key) - Unique identifier
- `work_shop_id` (Integer, Foreign Key) - References `work_shop.work_shop.id`
- `day_of_week` (Integer) - Day of week (0-6, where 0 is Monday)
- `is_working` (Boolean) - Whether the WorkShop is open on this day
- `opening_time` (Time) - Opening time
- `closing_time` (Time) - Closing time

**Relationships:**
- Direct relationship with `work_shop` through foreign key

## Migration Information

The calendar schema is defined in the migration file:
- `alembic/versions/0b7597ab50ca_start.py` - Initial schema creation

All calendar tables were created in the initial migration and are properly linked to WorkShop entities.

## API Endpoints

The calendar functionality is exposed through the following API endpoints:
- `/v1/calendar/appointments/` - Appointment management
- `/v1/calendar/holidays/` - Holiday management
- `/v1/calendar/working-hours/` - Working hours management

All endpoints require the `work_shop_id` parameter to ensure data isolation between different WorkShops.

## Usage Notes

1. All calendar entries must be associated with a valid WorkShop through the `work_shop_id` foreign key.
2. The `closing_time` field in the `working_hours` table uses the Time data type (not String).
3. Data is isolated by WorkShop - queries should always filter by `work_shop_id`.
4. All relationships are properly defined with appropriate foreign key constraints.