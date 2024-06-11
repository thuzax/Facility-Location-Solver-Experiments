from gurobipy import *

def get_var_percentage_attended_name(k, j):
    return "percentage_" + str(k) + "_" + str(j)

def get_var_open_facility_name(j):
    return "open_facility_" + str(j)


def create_variables(model, n_facilties, n_points):
    percentage_attended = [
        [
            model.addVar(
                name=get_var_percentage_attended_name(k, j),
                lb=0,
                ub=1,
                vtype=GRB.CONTINUOUS
            )
            for k in range(n_points)
        ] 
        for j in range(n_facilties)
    ]

    open_facility = [
        model.addVar(
            name=get_var_open_facility_name(j),
            vtype=GRB.BINARY
        )
        for j in range(n_facilties)
    ]

    return (percentage_attended, open_facility)


def create_full_attendance_constraint(
    model, 
    n_facilities, 
    n_points
):
    return [
        model.addConstr(
            quicksum(
                [
                    model.getVarByName(
                        name=get_var_percentage_attended_name(k, j)
                    )
                    for j in range(n_facilities)
                ]
            ) 
            ==
            1,
            name="full_attendance_" + str(k)

        )
        for k in range(n_points)
    ]


def open_facility_and_capacity(
    model,
    n_facilities,
    n_points,
    capacities,
    demands
):
    return [
        model.addConstr(
            quicksum(
                [
                    demands[k]
                    *
                    model.getVarByName(get_var_percentage_attended_name(k, j))
                    for k in range(n_points)
                ]
            ) 
            <=
            capacities[j]
            *
            model.getVarByName(name=get_var_open_facility_name(j)),
            name="open_facility_and_capacity_" + str(j) 
        )
        for j in range(n_facilities)
    ]
    

def aggregated_capacities(
    model,
    n_facilities,
    n_points,
    capacities,
    demands,
): 
    return [model.addConstr(
        quicksum(
            [
                capacities[j]
                *
                model.getVarByName(name=get_var_open_facility_name(j))
                for j in range(n_facilities)
            ]
        ) 
        >=
        quicksum(demands),
        name="aggregated_capacities"
    )]  

    

def implied_percentage_buond(
    model, 
    n_facilities,
    n_points
):
    return [
        [
            model.addConstr(
                model.getVarByName(name=get_var_percentage_attended_name(k, j))
                - 
                model.getVarByName(name=get_var_open_facility_name(j))
                <= 
                0,
                name="implied_bound_" + str(k) + "_" + str(j) 
            )
            for k in range(n_points)
        ]
        for j in range(n_facilities)
    ]


def create_constraints(
    model, 
    n_facilities, 
    facilities_data, 
    n_points, 
    points_data, 
):
    full_attendance_constr = create_full_attendance_constraint(
        model, 
        n_facilities, 
        n_points,
    )

    open_and_capacity_constr = open_facility_and_capacity(
        model, 
        n_facilities,
        n_points,
        facilities_data["capacities"],
        points_data["demands"]
    )

    aggregated_capacities_constr = aggregated_capacities(
        model, 
        n_facilities,
        n_points,
        facilities_data["capacities"],
        points_data["demands"]
    )

    implied_bounds_constr = implied_percentage_buond(
        model, 
        n_facilities,
        n_points,
    )

    return (
        full_attendance_constr,
        open_and_capacity_constr,
        aggregated_capacities_constr,      
        implied_bounds_constr
    )

def construct_objective_function(
    model,
    n_facilities,
    n_points,
    fixed_costs,
    costs_matrix
):
    model.setObjective(
        quicksum([
            quicksum([
                costs_matrix[j][k]
                *
                model.getVarByName(get_var_percentage_attended_name(k, j))
                for k in range(n_points)
            ])
            for j in range(n_facilities)
        ])
        +
        quicksum([
            fixed_costs[j]
            *
            model.getVarByName(get_var_open_facility_name(j))
            for j in range(n_facilities)
        ]),
        sense=GRB.MINIMIZE
    )


def create_model(
        facilities_data, 
        points_to_attend_data, 
        attend_costs_matrix
):

    model = Model("Capacited Facility Location")
    # model.setParam('MIPGap', 0.000001)


    number_of_facilties = len(facilities_data["names"])
    number_of_points_to_attend = len(points_to_attend_data["names"])
    variables = create_variables(
        model,
        number_of_facilties,
        number_of_points_to_attend
    )
    model.update()

    constraints = create_constraints(
        model,
        number_of_facilties,
        facilities_data,
        number_of_points_to_attend,
        points_to_attend_data,
    )
    model.update()

    construct_objective_function(
        model,
        number_of_facilties,
        number_of_points_to_attend,
        facilities_data["fixed_costs"],
        attend_costs_matrix
    )
    model.update()

    a, b = variables
    print(b)
    for i in range(len(b)):
        b[i].Start = 0
    
    b[2-1].Start = 1
    b[4-1].Start = 1
    b[10-1].Start = 1
    b[17-1].Start = 1
    b[19-1].Start = 1
    b[21-1].Start = 1
    b[25-1].Start = 1
    b[35-1].Start = 1
    b[47-1].Start = 1
    b[52-1].Start = 1
    b[57-1].Start = 1
    b[59-1].Start = 1
    b[65-1].Start = 1
    b[73-1].Start = 1
    b[75-1].Start = 1
    b[82-1].Start = 1
    b[84-1].Start = 1
    b[86-1].Start = 1
    b[88-1].Start = 1
    b[97-1].Start = 1

    model.update

    return model