
class BABSM:
    def __init__(self):
        self.battery = 100
        self.charging = False
        self.tasks = []

    def add_task(self):
        app = input("Enter app/service name: ")
        name = input("Enter task name: ")

        while True:
            priority = input("Priority (HIGH/MEDIUM/LOW): ").upper()
            if priority in ["HIGH", "MEDIUM", "LOW"]:
                break
            print("Enter HIGH, MEDIUM, or LOW.")

        self.tasks.append({
            "app": app,
            "name": name,
            "priority": priority
        })
        print("Task added successfully!")

    def show_tasks(self):
        if not self.tasks:
            print("No tasks added yet.")
            return

        print("\n--- TASK LIST ---")
        for i, task in enumerate(self.tasks, 1):
            print(
                i, task["app"], "|",
                task["name"], "|",
                task["priority"]
            )

    def evaluate_policy(self):
        if self.battery <= 0 and not self.charging:
            return "SYSTEM_OFF"
        if self.charging:
            return "CHARGING"
        if self.battery > 70:
            return "UNRESTRICTED"
        if self.battery > 30:
            return "BALANCED"
        if self.battery > 15:
            return "SAVER"
        return "CRITICAL"

    def run(self):
        mode = self.evaluate_policy()

        print("\n========== BABSM REPORT ==========")
        print("Battery:", str(self.battery) + "%")
        print("Charging:", self.charging)
        print("Policy:", mode)
        print("----------------------------------")

        for task in self.tasks:
            priority = task["priority"]
            name = task["name"]

            if mode == "SYSTEM_OFF":
                action = "HALTED"
            elif mode in ["CHARGING", "UNRESTRICTED"]:
                action = "EXECUTED NOW"
            elif priority == "HIGH" and mode in ["BALANCED", "SAVER"]:
                action = "EXECUTED NOW"
            elif mode == "BALANCED" and priority == "MEDIUM":
                action = "BATCHED"
            elif (
                mode == "CRITICAL"
                and priority == "HIGH"
                and "alert" in name.lower()
            ):
                action = "EXECUTED NOW"
            else:
                action = "DEFERRED"

            print(
                task["app"], "|", name,
                "|", priority, "->", action
            )

        print("==================================")

    def menu(self):
        while True:
            print("\n===== BABSM CONTROL MENU =====")
            print("1. Add task")
            print("2. View tasks")
            print("3. Change battery level")
            print("4. Change charging status")
            print("5. Run BABSM policy")
            print("6. Exit")

            choice = input("Choose an option: ")

            if choice == "1":
                self.add_task()

            elif choice == "2":
                self.show_tasks()

            elif choice == "3":
                try:
                    value = int(input("Enter battery (0-100): "))
                    if 0 <= value <= 100:
                        self.battery = value
                    else:
                        print("Battery must be between 0 and 100.")
                except ValueError:
                    print("Enter a valid whole number.")

            elif choice == "4":
                answer = input("Is device charging? (y/n): ")
                self.charging = answer.strip().lower() == "y"

            elif choice == "5":
                self.run()

            elif choice == "6":
                print("BABSM demo ended.")
                break

            else:
                print("Invalid choice. Try again.")


system = BABSM()
system.menu()
