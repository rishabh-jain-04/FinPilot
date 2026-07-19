from db.db import db_connection


def create_profile(
    user_id,
    monthly_income,
    monthly_expenses,
    dependants,
    employment_type,
    risk_profile,
    currency="INR"
):
    with db_connection() as connection:
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO financial_profiles (
                user_id,
                monthly_income,
                monthly_expenses,
                dependants,
                employment_type,
                risk_profile,
                currency
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            user_id,
            monthly_income,
            monthly_expenses,
            dependants,
            employment_type,
            risk_profile,
            currency
        ))

        connection.commit()


def get_profile(user_id):
    with db_connection() as connection:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT *
            FROM financial_profiles
            WHERE user_id = ?
        """, (user_id,))

        return cursor.fetchone()


def update_profile(
    user_id,
    monthly_income,
    monthly_expenses,
    dependants,
    employment_type,
    risk_profile,
    currency
):
    with db_connection() as connection:
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE financial_profiles
            SET
                monthly_income = ?,
                monthly_expenses = ?,
                dependants = ?,
                employment_type = ?,
                risk_profile = ?,
                currency = ?
            WHERE user_id = ?
        """, (
            monthly_income,
            monthly_expenses,
            dependants,
            employment_type,
            risk_profile,
            currency,
            user_id
        ))

        connection.commit()