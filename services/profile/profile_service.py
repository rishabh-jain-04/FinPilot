from db.profile_repo import (
    create_profile,
    get_profile,
    update_profile
)


def create_user_profile(
    user_id,
    monthly_income,
    monthly_expenses,
    dependants,
    employment_type,
    risk_profile,
    currency="INR"
):
    existing_profile = get_profile(user_id)

    if existing_profile:
        return {
            "success": False,
            "message": "Profile already exists."
        }

    create_profile(
        user_id,
        monthly_income,
        monthly_expenses,
        dependants,
        employment_type,
        risk_profile,
        currency
    )

    return {
        "success": True,
        "message": "Profile created successfully."
    }


def get_user_profile(user_id):

    profile = get_profile(user_id)

    if profile is None:
        return {
            "success": False,
            "message": "Profile not found."
        }

    return {
        "success": True,
        "profile": dict(profile)
    }


def update_user_profile(
    user_id,
    monthly_income,
    monthly_expenses,
    dependants,
    employment_type,
    risk_profile,
    currency="INR"
):

    profile = get_profile(user_id)

    if profile is None:
        return {
            "success": False,
            "message": "Profile not found."
        }

    update_profile(
        user_id,
        monthly_income,
        monthly_expenses,
        dependants,
        employment_type,
        risk_profile,
        currency
    )

    return {
        "success": True,
        "message": "Profile updated successfully."
    }