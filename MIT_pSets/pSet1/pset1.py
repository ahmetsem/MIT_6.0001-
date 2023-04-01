

# PART-A******************************
annual_salary=int(input("The Starting Annual Salary: "))
portion_saved=float(input("Portion of Salary to save: "))
total_cost=int(input("The cost of your dream home: "))

current_savings=0
monthly_salary=annual_salary/12
number_of_months=0
portion_down_payment=0.25
total_cost=total_cost*portion_down_payment

while current_savings<total_cost:
    invest_return=((current_savings * 0.04) / 12)
    current_savings += (monthly_salary * portion_saved) + invest_return
    number_of_months+=1

print("Number of Months: ",number_of_months)


# PART-B***********************************************************
annual_salary=int(input("The Starting Annual Salary: "))
portion_saved=float(input("Portion of Salary to save: "))
total_cost=int(input("The cost of your dream home: "))
semi_annual_rase=float(input("Enter the semi-annual raise as a decimal"))

current_savings=0
monthly_salary=annual_salary/12
number_of_months=0
portion_down_payment=0.25
total_cost=total_cost*portion_down_payment

while current_savings<total_cost:
    invest_return=((current_savings * 0.04) / 12)
    current_savings += (monthly_salary * portion_saved) + invest_return
    if number_of_months%6==0 and number_of_months!=0:
        monthly_salary=monthly_salary + (monthly_salary*semi_annual_rase)

    number_of_months+=1

print("Number of Months: ",number_of_months)

# PART-C******************************************

starting_salary=int(input("Enter the starting salary: "))
cost_of_house=1000000
semi_annual_rase=0.07
down_payment=cost_of_house*0.25
current_saving=0
monthly_salary=starting_salary/12
invest_return=0
eps=100
low=0
high=1000
best_rating=(low+high)/2
numb_of_steps=0
check=True

while True:
    for i in range(1, 37):
        if i % 6 == 0:
            monthly_salary += monthly_salary * semi_annual_rase
        current_saving += (monthly_salary * (1)) + invest_return
        invest_return = (current_saving * 0.04) / 12

    if current_saving<(down_payment-eps):
        print("Its not possible to buy in 36 months")
        check=False
        break

    else:
        current_saving = 0
        monthly_salary = starting_salary / 12
        invest_return = 0

        for i in range(1,37):
            current_saving+=(monthly_salary*(best_rating/1000))+invest_return
            invest_return=(current_saving*0.04)/12
            if i%6==0 :
                monthly_salary+=monthly_salary*semi_annual_rase

        if abs(current_saving - down_payment) < eps:
            break

        elif current_saving > down_payment:
            high=best_rating

        elif current_saving < down_payment:
            low=best_rating

        numb_of_steps+=1
        best_rating=(low+high)/2

if check:
    print("Best Saving Rate: ",(best_rating/1000))
    print("Steps in Bisection search: ",numb_of_steps)


