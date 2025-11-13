def get_admin_dashboard_service(current_admin):
    # Any DB queries or aggregation logic can go here
    return {
        "message": f"Welcome {current_admin.name}, this is your admin dashboard.",
        "email": current_admin.email,
        "role": current_admin.role,
    }
