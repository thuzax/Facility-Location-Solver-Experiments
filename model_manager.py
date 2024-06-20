import gurobipy

def get_gurobi_params(config_dict=None):
    ''' 
    The following keys are extracted considered in config_dict (if they exist):

    - branching (branching strategy - Gurobi VarBranch Param)
        (-1) Default (automatically)
        (0) Pseudo Reduced Cost Branching
        (1) Pseudo Shadow Price Branching
        (2) Maximum Infeasibility Branching
        (3) Strong Branching

    - branching_direction (branching direction - Gurobi BranchDir Param)
        (0) Default (automatically)
        (-1) will always explore the rounded down branch first
        (1) will always explore the rounded up branch first

    - cuts (cuts intensisty - Gurobi Cuts Param)
        (-1) value chooses automatically
        (0) to shut off cuts
        (1) for moderate cut generation
        (2) for aggressive cut generation
        (3) for very aggressive cut generation

    - <cut_name>_cut (specific cut intensity - <cut_name> is the of the cut):
        The default value for all cuts is -1
        List of <cut_name> for each Gurobi Cut:
            - bqp_cut => BQPCuts
            - clique_cut => CliqueCuts
            - cover_cut => CoverCuts
            - flow_cover_cut => FlowCoverCuts
            - flow_path_cut => FlowPathCuts
            - gub_cover_cut => GUBCoverCuts
            - implied_cut => ImpliedCuts
            - inf_proof_cut => InfProofCuts
            - lift_project_cut => LiftProjectCuts
            - mip_sep_cut => MIPSepCuts
            - mir_cut => MIRCuts
            - mixing_cut => MixingCuts
            - mod_k_cut => ModKCuts
            - network_cut => NetworkCuts
            - proj_implied_cut => ProjImpliedCuts
            - psd_cut => PSDCuts
            - relax_lift_cut => RelaxLiftCuts
            - rlt_cut => RLTCuts
            - strong_cg_cut => StrongCGCuts
            - sub_mip_cut => SubMIPCuts
            - zero_half_cut => ZeroHalfCuts
        

    - node_selecion (node selection strategy - Gurobi MIPFocus Param)
         (0) default: balance between primal and dual
         (1) focus on improving primal solution
         (2) focus on improving dual solution
         (3) focus on improving best bound

    - time (Gurobi TimeLimit Param)
        Limit time to execute

    - gap (Gurobi MIPGap Param)
        Acceptable optimallity gap

    - heuristics (Gurobi Heuristics Param)
        Percentage of time spent with heuristics

    - presolve (Gurobi Presolve Param)
        (-1) defaulf: automatic setting. 
        (0) turn off presolve 
        (1) conservative 
        (2) aggressive

    - log_file (Gurobi LogFile Param)
        Name of the log file
    
    - log_console (Gurobi LogToConsole Param)
        (0) deactivate log in console
        (1) activate log in console

    Default Values:
        VarBranch: -1 
        BranchDir: 0
        Cuts: -1
        TimeLimit: gurobipy.GRB.INFINITY
        MIPGap: 0.0001
        Presolve: 0
        Heuristics: 0.05
        LogFile: ""
        LogToConsole: 1
        MIPFocus: 0
    '''
    # print(gurobipy.Model().getParamInfo("VarBranch"))
    params = {
        "VarBranch": -1, 
        "BranchDir": 0,
        "Cuts": -1,
        "TimeLimit": gurobipy.GRB.INFINITY,
        "MIPGap": 0.0001,
        "Presolve": -1,
        "Heuristics": 0.05,
        "LogFile": "",
        "MIPFocus": 0,
        "LogToConsole": 1,
        "BQPCuts": -1,
        "CliqueCuts": -1,
        "CoverCuts": -1,
        "FlowCoverCuts": -1,
        "FlowPathCuts": -1,
        "GUBCoverCuts": -1,
        "ImpliedCuts": -1,
        "InfProofCuts": -1,
        "LiftProjectCuts": -1,
        "MIPSepCuts": -1,
        "MIRCuts": -1,
        "MixingCuts": -1,
        "ModKCuts": -1,
        "NetworkCuts": -1,
        "ProjImpliedCuts": -1,
        "PSDCuts": -1,
        "RelaxLiftCuts": -1,
        "RLTCuts": -1,
        "StrongCGCuts": -1,
        "SubMIPCuts": -1,
        "ZeroHalfCuts": -1
    }
    
    if (config_dict is not None):
        if ("branching" in config_dict.keys()):
            params["VarBranch"] = config_dict["branching"]
        if ("node_selecion" in config_dict.keys()):
            params["BranchDir"] = config_dict["node_selecion"]
        if ("cuts" in config_dict.keys()):
            params["Cuts"] = config_dict["cuts"]
        if ("presolve" in config_dict.keys()):
            params["Presolve"] = config_dict["presolve"]
        if ("heuristics" in config_dict.keys()):
            params["Heuristics"] = config_dict["heuristics"]
        if ("time" in config_dict.keys()):
            params["TimeLimit"] = config_dict["time"]
        if ("gap" in config_dict.keys()):
            params["MIPGap"] = config_dict["gap"]
        if ("log_file" in config_dict.keys()):
            params["LogFile"] = config_dict["log_file"]
        if ("focus" in config_dict.keys()):
            params["MIPFocus"] = config_dict["focus"]
        if ("log_console" in config_dict.keys()):
            params["LogToConsole"] = config_dict["log_console"]
        if ("bqp_cut" in config_dict.keys()):
            params["BQPCuts"] = config_dict["bqp_cut"]
        if ("clique_cut" in config_dict.keys()):
            params["CliqueCuts"] = config_dict["clique_cut"]
        if ("cover_cut" in config_dict.keys()):
            params["CoverCuts"] = config_dict["cover_cut"]
        if ("flow_cover_cut" in config_dict.keys()):
            params["FlowCoverCuts"] = config_dict["flow_cover_cut"]
        if ("flow_path_cut" in config_dict.keys()):
            params["FlowPathCuts"] = config_dict["flow_path_cut"]
        if ("gub_cover_cut" in config_dict.keys()):
            params["GUBCoverCuts"] = config_dict["gub_cover_cut"]
        if ("implied_cut" in config_dict.keys()):
            params["ImpliedCuts"] = config_dict["implied_cut"]
        if ("inf_proof_cut" in config_dict.keys()):
            params["InfProofCuts"] = config_dict["inf_proof_cut"]
        if ("lift_project_cut" in config_dict.keys()):
            params["LiftProjectCuts"] = config_dict["lift_project_cut"]
        if ("mip_sep_cut" in config_dict.keys()):
            params["MIPSepCuts"] = config_dict["mip_sep_cut"]
        if ("mir_cut" in config_dict.keys()):
            params["MIRCuts"] = config_dict["mir_cut"]
        if ("mixing_cut" in config_dict.keys()):
            params["MixingCuts"] = config_dict["mixing_cut"]
        if ("mod_k_cut" in config_dict.keys()):
            params["ModKCuts"] = config_dict["mod_k_cut"]
        if ("network_cut" in config_dict.keys()):
            params["NetworkCuts"] = config_dict["network_cut"]
        if ("proj_implied_cut" in config_dict.keys()):
            params["ProjImpliedCuts"] = config_dict["proj_implied_cut"]
        if ("psd_cut" in config_dict.keys()):
            params["PSDCuts"] = config_dict["psd_cut"]
        if ("relax_lift_cut" in config_dict.keys()):
            params["RelaxLiftCuts"] = config_dict["relax_lift_cut"]
        if ("rlt_cut" in config_dict.keys()):
            params["RLTCuts"] = config_dict["rlt_cut"]
        if ("strong_cg_cut" in config_dict.keys()):
            params["StrongCGCuts"] = config_dict["strong_cg_cut"]
        if ("sub_mip_cut" in config_dict.keys()):
            params["SubMIPCuts"] = config_dict["sub_mip_cut"]
        if ("zero_half_cut" in config_dict.keys()):
            params["ZeroHalfCuts"] = config_dict["zero_half_cut"]

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

    return model


def get_solution_dict(model):
    data = {
        "variables": None,
        "objective": None,
        "is_optimal": False,
        "inf_or_unb": False,
        "feasible_found": False,
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
        data["is_optimal"] = True

    data["feasible_found"] = True
    data["objective"] = model.getObjective().getValue()
    data["dual_bound"] = model.ObjBound

    return data


def get_linear_relaxation(model):
    linear_model = model.relax()
    linear_model.update()
    return linear_model

def get_solution_dict_linear(model):
    data = get_solution_dict(model)
    data["gap"] = None
    return data

def get_solution_dict_MIP(model):
    data = get_solution_dict(model)
    data["gap"] = None
    if (data["is_optimal"] or "feasible_found"):
        data["gap"] = model.MIPGap
    return data