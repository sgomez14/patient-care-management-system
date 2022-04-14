from src.users.users import get_user_assignments, get_patient_summary

if __name__ == "__main__":
    # test getting assignments for doctor with user_id 42530
    print(get_user_assignments(42530))

    # test getting assignments for patient with user_id 20544
    print(get_user_assignments(20544))

    # test getting assignments for doctor with user_id 123
    print(get_user_assignments(123))

    # test getting assignments for patient with user_id 321
    print(get_user_assignments(321))

    # test getting assignments for invalid user
    print(get_user_assignments(12))

    # test getting summary for patient with user_id 321
    print(get_patient_summary(321))

    # test getting summary for user that is not a patient
    print(get_patient_summary(123))

    # test getting summary for invalid user
    print(get_patient_summary(12))
