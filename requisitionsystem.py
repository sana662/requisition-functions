"""requisitionsystem.py

Requisition management system, built on top of the Part A functions
(staff_info, requisitions_total/requisitions_details, requisition_approval,
display_requisitons) by turning them into methods of a RequisitionSystem
class and adding the pieces Part B asks for: a manager-response method,
and statistics  tracking.

Approval rule (from Part A):
    - Total < $500  -> automatically Approved (Approval Reference Number
                       is generated: Staff ID + last 3 digits of the
                       Requisition ID).
    - Total >= $500 -> stays Pending until a manager calls
                       respond_requsition() to mark it Approved or
                       Not approved (or leave it Pending).
"""

# Global variable outside __init__, used to generate a unique requisition ID
# (counter + 10000), same idea as Part A's local 'counter' variable, but
# persistent across every requisition that gets created.
req_counter = 0


class RequisitionSystem:
    """Represents one staff requisition and the operations that can be
    performed on it (creation, pricing, approval, display, and reporting).
    """

    # Class-level counters shared by every requisition (used for statistics).
    total_submitted = 0
    total_approved = 0
    total_pending = 0
    total_not_approved = 0

    def __init__(self):
        global req_counter

        # Shared data identified from Part A
        self.date = None
        self.staff_id = None
        self.staff_name = None

        req_counter += 1
        self.requisition_id = req_counter + 10000

        self.items = []                 # list of (price, quantity) tuples
        self.total = 0                  # total cost of the requisition
        self.status = "Pending"         # Pending / Approved / Not approved
        self.approval_reference = None  # only set once Approved

        # A brand-new requisition always starts out Pending.
        RequisitionSystem.total_submitted += 1
        RequisitionSystem.total_pending += 1

    # ------------------------------------------------------------------
    # a. Staff submits their basic information (Part A, Task 1)
    # ------------------------------------------------------------------
    def staff_info(self):
        self.date = input("Enter Date: ")
        self.staff_id = input("Enter Staff ID: ")
        self.staff_name = input("Enter Staff Name: ")

        print("\nPrinting Staff Information:")
        print(f"\nDate: {self.date}")
        print(f"\nStaff ID: {self.staff_id}")
        print(f"\nStaff Name: {self.staff_name}")
        print(f"\nRequisition ID: {self.requisition_id}")

        return self.date, self.staff_id, self.staff_name, self.requisition_id

    # ------------------------------------------------------------------
    # b. Accept a list of (price, quantity) items and return the total
    #    (Part A, Task 2/3)
    # ------------------------------------------------------------------
    def requisitions_details(self, items):
        self.items = items
        self.total = sum(price * quantity for price, quantity in items)
        return self.total

    # ------------------------------------------------------------------
    # c. Decide Approved / Pending based on the total (Part A, Task 3)
    # ------------------------------------------------------------------
    def requisition_approval(self):
        if self.total < 500:
            self._set_status("Approved")
        else:
            self.status = "Pending"
        return self.status

    def _set_status(self, new_status):
        """Internal helper that changes status AND keeps the class-level
        statistics counters in sync."""
        if self.status == "Pending" and new_status != "Pending":
            RequisitionSystem.total_pending -= 1
            if new_status == "Approved":
                RequisitionSystem.total_approved += 1
                self.approval_reference = (
                    f"{self.staff_id}{str(self.requisition_id)[-3:]}"
                )
            elif new_status == "Not approved":
                RequisitionSystem.total_not_approved += 1
        self.status = new_status

    # ------------------------------------------------------------------
    # d. Manager responds to a pending requisition (>$499)
    # ------------------------------------------------------------------
    def respond_requsition(self, decision):
        if self.status != "Pending":
            print(
                f"Requisition {self.requisition_id} is already "
                f"'{self.status}'. No action taken."
            )
            return

        decision = decision.strip().lower()
        if decision == "approved":
            self._set_status("Approved")
        elif decision == "not approved":
            self._set_status("Not approved")
        else:
            # Manager chose to leave it pending -- nothing changes.
            print(f"Requisition {self.requisition_id} left as Pending.")

    # ------------------------------------------------------------------
    # e. Display a single requisition / all requisitions (Part A, Task 4)
    # ------------------------------------------------------------------
    def display_requisiton(self):
        print(f"Date: {self.date}")
        print(f"Requisition ID: {self.requisition_id}")
        print(f"Staff ID: {self.staff_id}")
        print(f"Staff Name: {self.staff_name}")
        print(f"Total: ${self.total:.0f}")
        print(f"Status: {self.status}")
        print(
            "Approval Reference Number: "
            f"{self.approval_reference if self.approval_reference else 'Not available'}"
        )
        print()

    @classmethod
    def display_requisitons(cls, requisitions):
        print("Printing Requisitions:\n")
        for requisition in requisitions:
            requisition.display_requisiton()

    # ------------------------------------------------------------------
    # f. Requisition statistics
    # ------------------------------------------------------------------
    @classmethod
    def requisition_statistic(cls):
        print("Statistics:")
        print("Displaying the Requisition Statistics")
        print()
        print(f"The total number of requisitions submitted: {cls.total_submitted}")
        print(f"The total number of approved requisitions: {cls.total_approved}")
        print(f"The total number of pending requisitions: {cls.total_pending}")
        print(
            "The total number of not approved requisitions: "
            f"{cls.total_not_approved}"
        )
        print()
        return {
            "submitted": cls.total_submitted,
            "approved": cls.total_approved,
            "pending": cls.total_pending,
            "not_approved": cls.total_not_approved,
        }


# ------------------------------------------------------------------------
# 5. Test the program
#
# NOTE: staff_info() uses input(), exactly as in Part A, so running this
# file will prompt you in the console for Date / Staff ID / Staff Name for
# each of the 5 requisitions below. Have your test data ready to type in,
# for example:
#
#   Requisition 1 (Approved automatically, total < $500):
#       Date: 03/04/2024, Staff ID: FN19, Staff Name: John Paul
#       items: [(50, 3), (100, 1)]   -> total = 250
#
#   Requisition 2 (Pending -> manager approves, total >= $500):
#       Date: 05/04/2024, Staff ID: FN20, Staff Name: Tracy Brown
#       items: [(350, 2)]            -> total = 700
#
#   Requisition 3 (Pending -> manager rejects, total >= $500):
#       Date: 07/05/2024, Staff ID: FN15, Staff Name: Emma Wellington
#       items: [(1750, 2)]           -> total = 3500
#
#   Requisition 4 (Approved automatically, total < $500):
#       Date: 03/05/2024, Staff ID: FN02, Staff Name: Catlin White
#       items: [(49, 10)]            -> total = 490
#
#   Requisition 5 (Pending -> manager leaves it Pending, total >= $500):
#       Date: 10/05/2024, Staff ID: FN08, Staff Name: Michael Chen
#       items: [(900, 1), (200, 1)]  -> total = 1100
# ------------------------------------------------------------------------
if __name__ == "__main__":
    requisitions = []
    item_sets = [
        [(50, 3), (100, 1)],   # -> 250  (Approved)
        [(350, 2)],            # -> 700  (Pending)
        [(1750, 2)],           # -> 3500 (Pending)
        [(49, 10)],            # -> 490  (Approved)
        [(900, 1), (200, 1)],  # -> 1100 (Pending)
    ]

    # --- a. Submit 5 requisitions covering different scenarios ---------
    for items in item_sets:
        r = RequisitionSystem()
        r.staff_info()
        r.requisitions_details(items)
        r.requisition_approval()
        requisitions.append(r)

    print("=== Requisitions after initial submission ===\n")
    RequisitionSystem.display_requisitons(requisitions)

    # --- b. Display the requisition statistics --------------------------
    RequisitionSystem.requisition_statistic()

    # --- c. Manager responds to requisitions greater than $499 ----------
    pending_over_499 = [r for r in requisitions if r.status == "Pending" and r.total > 499]

    if pending_over_499:
        print("=== Manager responds to pending requisitions (>$499) ===\n")
        # Example decisions: approve the first, reject the second, leave
        # any remaining ones pending.
        decisions = ["approved", "not approved"]
        for r, decision in zip(pending_over_499, decisions):
            r.respond_requsition(decision)

    print("\n=== Requisitions after manager response ===\n")
    RequisitionSystem.display_requisitons(requisitions)

    print("--- Updated requisition statistics ---\n")
    RequisitionSystem.requisition_statistic()