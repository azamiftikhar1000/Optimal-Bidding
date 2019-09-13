import csv
from ortools.linear_solver import pywraplp

discom_price = 7
demand = []
solar = []
market_price = []

with open('Demand.csv', 'rb') as f:
		reader = csv.reader(f)
		demandd = list(reader)
		for row in demandd:
			for val in row:
				demand.append(float(val))


with open('Solar.csv', 'rb') as f:
		reader = csv.reader(f)
		solarr = list(reader)
		for row in solarr:
			for val in row:
				solar.append(float(val))


with open('Price.csv', 'rb') as f:
    reader = csv.reader(f)
    market_pricee = list(reader)
    for row in market_pricee:
			for val in row:
				market_price.append(float(val))

# demand = demand[:2400]
# solar = solar[:2400]
# market_price = market_price[:2400]
# print(market_price)
# print(demand)
# print(solar)
# print(market_price)
def main():

	# Instantiate a Glop solver, naming it SolveStigler.
	solver = pywraplp.Solver('SolveStigler',
											pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)
	# Declare an array to hold our nutritional data.
	bid_quantity_per_hour = [[]] * len(demand)
	discom_quantity_per_hour = [[]] * len(demand)
	battery_charge_quantity_per_hour = [[]] * len(demand)
	battery_discharge_quantity_per_hour = [[]] * len(demand)
	solar_quantity_per_hour = [[]] * len(demand)

	# Objective: minimize the sum of (price-normalized) foods.
	objective = solver.Objective()
	for i in range(0, len(demand)):
		bid_quantity_per_hour[i] = solver.NumVar(0.0, solver.infinity(), "Bid Day " + str((i+1)/24) + "Hour " + str(i%24+1) )
		discom_quantity_per_hour[i] = solver.NumVar(0.0, solver.infinity(), "Discom Day " + str((i+1)/24) + "Hour " + str(i%24+1) )
		battery_charge_quantity_per_hour[i] = solver.NumVar(0.0, 5.0, "Battery_charge Day " + str((i+1)/24) + "Hour " + str(i%24+1) )
		battery_discharge_quantity_per_hour[i] = solver.NumVar(0.0, 5.0, "Battery_discharge Day " + str((i+1)/24) + "Hour " + str(i%24+1) )
		solar_quantity_per_hour[i] = solver.NumVar(solar[i], solar[i], "Solar Day " + str((i+1)/24) + "Hour " + str(i%24+1) )
		
		objective.SetCoefficient(bid_quantity_per_hour[i], market_price[i])
		objective.SetCoefficient(discom_quantity_per_hour[i], discom_price)
		objective.SetCoefficient(battery_charge_quantity_per_hour[i], 0.0)
		objective.SetCoefficient(battery_discharge_quantity_per_hour[i], 0.0)
		objective.SetCoefficient(solar_quantity_per_hour[i], 0.0)

	objective.SetMinimization()
	# Create the constraints, one per nutrient.
	demand_constraints = [0] * len(demand)
	battery_constraints = [0] * len(demand)

	for i in range(0, len(demand)):
		demand_constraints[i] = solver.Constraint(demand[i], solver.infinity())

		demand_constraints[i].SetCoefficient(solar_quantity_per_hour[i], 1)								#solar
		demand_constraints[i].SetCoefficient(bid_quantity_per_hour[i],1)									#bid
		demand_constraints[i].SetCoefficient(discom_quantity_per_hour[i], 1)							#discom
		demand_constraints[i].SetCoefficient(battery_charge_quantity_per_hour[i], -1)			#battery charge
		demand_constraints[i].SetCoefficient(battery_discharge_quantity_per_hour[i], 0.8)			#battery discharge

		max_battery = (i + 1) * 5.0
		if max_battery > 25.0:
			max_battery = 25.0
		battery_constraints[i] = solver.Constraint(0.0, max_battery)

		for j in range(i+1):
			battery_constraints[i].SetCoefficient(battery_charge_quantity_per_hour[j], 1)
			battery_constraints[i].SetCoefficient(battery_discharge_quantity_per_hour[j], -1)


	# Solve!
	print("hello")
	status = solver.Solve()
	print("hello")

	if status == solver.OPTIMAL:
		# Display the amounts (in dollars) to purchase of each food.
		price = 0
		# num_nutrients = len(data[i]) - 3
		# values = [0] * len(demand)
		ci = 0
		co = 0
		cio = 0
		p2 = 0
		lst = []
		for i in range(0, len(demand)):
			print(i,  round(demand[i], 2), round(bid_quantity_per_hour[i].solution_value(), 2), round(market_price[i],2), round(solar_quantity_per_hour[i].solution_value(), 2),  round(battery_charge_quantity_per_hour[i].solution_value(), 2),  round(battery_discharge_quantity_per_hour[i].solution_value(), 2))
			price += bid_quantity_per_hour[i].solution_value()*market_price[i]
			p2 += discom_quantity_per_hour[i].solution_value()*discom_price
			lst.append([market_price[i], bid_quantity_per_hour[i].solution_value()])
			ci += battery_charge_quantity_per_hour[i].solution_value()
			co += battery_discharge_quantity_per_hour[i].solution_value()
			cio += (battery_charge_quantity_per_hour[i].solution_value() - battery_discharge_quantity_per_hour[i].solution_value())
			# print(cio)	
			if cio < -0.00000001 or cio > 25.00000001:
				print("breaaa")
		print(price)
		print(p2+price)
		print(ci)
		print(co)
		print(cio)

		write_file = "21.csv"
		with open(write_file, "w") as output:
		    for line in lst:
		    	output.write(str(line[0]) + "," + str(line[1]))
		        output.write('\n')
	# 		for nutrient in range(0, num_nutrients):
	# 			nutrients[nutrient] += data[i][nutrient+3] * food[i].solution_value()

	# 		if food[i].solution_value() > 0:
	# 			print "%s = %f" % (data[i][0], food[i].solution_value())

	# 	print 'Optimal annual price: $%.2f' % (365 * price)
	# else:  # No optimal solution was found.
	# 	if status == solver.FEASIBLE:
	# 		print 'A potentially suboptimal solution was found.'
	# 	else:
	# 		print 'The solver could not solve the problem.'

if __name__ == '__main__':
	main()