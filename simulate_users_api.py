from src.users.users import get_user_assignments

if __name__ == "__main__":
    # test getting assignments for doctor with user_id 42530
    print(get_user_assignments(42530))

    # test getting assignments for patient with user_id 20544
    print(get_user_assignments(20544))

    # test getting assignments for doctor with user_id 123
    print(get_user_assignments(123))

    # test getting assignments for patient with user_id 321
    print(get_user_assignments(321))
