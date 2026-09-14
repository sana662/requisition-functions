def staff_info(counter):
    """
    Collects staff requisition details via user input and generates
    a unique requisition ID.

    Design Principle: Single Responsibility Principle (SRP)
    This function has one job — gather staff input and produce a
    requisition record. It does not handle printing, storage, or
    validation logic elsewhere in the program, keeping it focused
    and easy to modify independently.

    Parameters:
        counter (int): A running count of requisitions submitted so far,
                        used to generate a unique ID.

    Returns:
        tuple: (date, staff_id, staff_name, requisition_id)
    """
    # DRY Principle: each input() call is simple and used once —
    # no duplicated input-gathering logic anywhere else in the program
    date = input("Enter Date (DD/MM/YYYY): ")
    staff_id = input("Enter Staff ID: ")
    staff_name = input("Enter Staff Name: ")

    # Requisition ID generation: counter + 10000 ensures a unique,
    # sequential ID without needing external storage or a database
    requisition_id = counter + 10000

    return date, staff_id, staff_name, requisition_id


def print_staff_info(date, staff_id, staff_name, requisition_id):
    """
    Displays staff requisition details in a formatted way.

    Design Principle: Separation of Concerns
    Printing/display logic is kept separate from data collection
    (staff_info). This means if the output format needs to change
    (e.g., to JSON, or a file), only this function needs editing —
    staff_info remains untouched. This also supports the
    Open/Closed Principle: new output formats can be added without
    modifying existing input-gathering code.
    """
    print("Printing Staff Information:")
    print(f"Date: {date}")
    print(f"Staff ID: {staff_id}")
    print(f"Staff Name: {staff_name}")
    print(f"Requisition ID: {requisition_id}")


# Example usage
if __name__ == "__main__":
    # Design Improvement Note: Currently this counter resets every run
    # since it's not persisted — a real system should store this
    # externally (file/database) to maintain uniqueness across sessions.
    requisition_counter = 1

    date, staff_id, staff_name, requisition_id = staff_info(requisition_counter)
    print_staff_info(date, staff_id, staff_name, requisition_id)
