from db.db import get_connection


def create_profile(
    user_id,
    monthly_income,
    monthly_expenses,
    dependants,
    employment_type,
    risk_profile,
    currency="INR"
):
    connection = get_connection()
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
    connection.close()


def get_profile(user_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM financial_profiles
        WHERE user_id = ?
    """, (user_id,))

    profile = cursor.fetchone()

    connection.close()

    return profile


def update_profile(
    user_id,
    monthly_income,
    monthly_expenses,
    dependants,
    employment_type,
    risk_profile,
    currency
):
    connection = get_connection()
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
    connection.close()