import gurobipy

def get_gurobi_params(config_file=None):
    
    # VarBranch (branching strategy)
    ## -1. Default (automatically)
    ##  0. Pseudo Reduced Cost Branching
    ##  1. Pseudo Shadow Price Branching
    ##  2. Maximum Infeasibility Branching
    ##  3. Strong Branching

    # BranchDir (node selection strategy)
    ##  0. Default (automatically)
    ## -1. will always explore the rounded down branch first
    ##  1 will always explore the rounded up branch first

    # Cuts (cuts intensisty)
    ## -1 value chooses automatically
    ##  0. to shut off cuts
    ##  1. for moderate cut generation
    ##  2. for aggressive cut generation
    ##  3. for very aggressive cut generation

    # TimeLimit
    ## Limit time to execute

    # MIPGap
    ## Acceptable optimallity gap

    # print(gurobipy.Model().getParamInfo("VarBranch"))
    params = {
        "VarBranch": -1, 
        "BranchDir": 0,
        "Cuts": -1,
        "TimeLimit": gurobipy.GRB.INFINITY,
        "MIPGap": 0.0001,
        "Presolve": 0,
        "Heuristics": 0.05
    }
    
    if (config_file is not None):            
        params["VarBranch"] = config_file["branching"]
        params["BranchDir"] = config_file["node_selecion"]
        params["Cuts"] = config_file["cuts"]
        params["Presolve"] = config_file["presolve"]
        params["Heuristics"] = config_file["heuristics"]
        params["TimeLimit"] = config_file["time"]
        params["MIPGap"] = config_file["gap"]

    return params


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
                vtype=gurobipy.GRB.CONTINUOUS
            )
            for k in range(n_points)
        ] 
        for j in range(n_facilties)
    ]

    open_facility = [
        model.addVar(
            name=get_var_open_facility_name(j),
            vtype=gurobipy.GRB.BINARY
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
            gurobipy.quicksum(
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
            gurobipy.quicksum(
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
        gurobipy.quicksum(
            [
                capacities[j]
                *
                model.getVarByName(name=get_var_open_facility_name(j))
                for j in range(n_facilities)
            ]
        ) 
        >=
        gurobipy.quicksum(demands),
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
        gurobipy.quicksum([
            gurobipy.quicksum([
                costs_matrix[j][k]
                *
                model.getVarByName(get_var_percentage_attended_name(k, j))
                for k in range(n_points)
            ])
            for j in range(n_facilities)
        ])
        +
        gurobipy.quicksum([
            fixed_costs[j]
            *
            model.getVarByName(get_var_open_facility_name(j))
            for j in range(n_facilities)
        ]),
        sense=gurobipy.GRB.MINIMIZE
    )


def create_model(
        facilities_data, 
        points_to_attend_data, 
        attend_costs_matrix,
        gurobi_params=None
):

    model = gurobipy.Model("Capacited Facility Location")
    # model.setParam('MIPGap', 0.000001)
    if (gurobi_params is not None):
        for param_name, param_value in gurobi_params.items():
            model.setParam(param_name, param_value)


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

    model.update

    return model


def get_solution_dict(model):
    data = {
        "variables": None,
        "objective": None,
        "is_optimal": False,
        "inf_or_unb": False,
        "feasible_found": False,
        "gap": None,
        "node_count": None,
        "total_time": None
    }
    data["total_time"] = model.Runtime

    if (model.status == gurobipy.GRB.INFEASIBLE):
        data["inf_or_unb"] = True
        return data
    
    if (model.status == gurobipy.GRB.UNBOUNDED):
        data["inf_or_unb"] = True
        return data

    data["node_count"] = model.NodeCount

    if (model.SolCount == 0):
        return data
    

    data["variables"] = {}
    for v in model.getVars():
        data["variables"][v.VarName] = v.X

    if (model.status == gurobipy.GRB.OPTIMAL):
        data["feasible_found"] = True
        data["is_optimal"] = True
        data["gap"] = model.MIPGap

    data["feasible_found"] = True
    data["objective"] = model.getObjective().getValue()
    data["gap"] = model.MIPGap

    return data