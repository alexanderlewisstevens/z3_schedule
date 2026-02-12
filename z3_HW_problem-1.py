from z3 import *

# Presentations
PRESENTATIONS = ["Q", "A", "B", "C", "N", "M", "CC", "DS", "IoT"]  # 9 presentations

# Time slots: 9:00, 10:00, 11:00
TIMES = [9, 10, 11]

# Rooms: Alpha, Beta, Gamma
ROOMS = ["Alpha", "Beta", "Gamma"]

# Create Z3 variables for each presentation's time and room
time_vars = {p: Int(f"time_{p}") for p in PRESENTATIONS}
room_vars = {p: Int(f"room_{p}") for p in PRESENTATIONS}

# Create Z3 solver
solver = Solver()

# Conflict Constraints: Certain presentations cannot happen at the same time
solver.add(time_vars["Q"] != time_vars["B"])  # Q and B cannot happen at the same time
solver.add(time_vars["A"] != time_vars["DS"])  # A and DS cannot happen at the same time
solver.add(time_vars["C"] != time_vars["M"])  # C and M cannot happen at the same time

# Time Priority: Some presentations must happen earlier in the day
solver.add(time_vars["Q"] < time_vars["B"])  # Q must happen earlier than B
solver.add(time_vars["A"] < time_vars["IoT"])  # A must happen earlier than IoT

# Location Constraints: Some presentations must be in specific rooms
solver.add(room_vars["C"] == 1)  # Cybersecurity must be in Room Beta
solver.add(room_vars["B"] == 2)  # Blockchain must be in Room Gamma
solver.add(room_vars["CC"] == 0)  # Cloud Computing must be in Room Alpha

# Order Constraints: Some presentations must happen before others
solver.add(time_vars["DS"] < time_vars["M"])  # DS must happen before M
solver.add(time_vars["N"] < time_vars["CC"])  # N must happen before CC

# ADDITINOAL EMERGENCY CONSTRAINTS 

# Quantum Computing fixed at 9:00 AM
# Quantum Computing must be in Room Alpha
# AI fixed at 10:00 AM
# AI in Room Beta
# Blockchain fixed at 11:00 AM
# Blockchain in Room Gamma


# Each presentation must be scheduled exactly once in time and room
for p in PRESENTATIONS:
    solver.add(time_vars[p] >= 9, time_vars[p] <= 11)
    solver.add(room_vars[p] >= 0, room_vars[p] <= 2)

# Create combined variables for time and room
combined_vars = [time_vars[p] * 10 + room_vars[p] for p in PRESENTATIONS]

# Ensure every time slot and room combination is unique
solver.add(Distinct(combined_vars))
# Solve the problem
if solver.check() == sat:
    model = solver.model()
    for p in PRESENTATIONS:
        time_assigned = model[time_vars[p]]
        room_assigned = model[room_vars[p]]
        room_str = ROOMS[room_assigned.as_long()]
        print(f"Presentation {p} is scheduled at {time_assigned} in Room {room_str}")
else:
    print("No solution found")