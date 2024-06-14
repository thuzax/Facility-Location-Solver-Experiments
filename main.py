import os
import sys
from file_manager import *
from model_manager import *

def run(args):
    if (len(args) < 4):
        print("Needs:")
        print(" 1. Input File")
        print(" 2. Configuration File (JSON)")
        print(" 3. Solution Output Path")
        print(" 4. Model Output Path")
        exit(0)
    
    config_dict = read_config_file(args[1])
    solution_output_path = args[2]
    model_output_path = args[3]

    params = get_gurobi_params(config_file=config_dict)

    data = read_input_file(args[0])

    facilities_data, points_to_attend_data, attend_costs_matrix = data

    facility_model = create_model(
        facilities_data, 
        points_to_attend_data, 
        attend_costs_matrix,
        params
    )

    if (model_output_path is not None):
        facility_model.write(model_output_path)
    
    facility_model.optimize()

    if (solution_output_path is not None):
        solution_dict = {
            "input_file": args[0],
            "output_file": args[3],
            "model_location": args[2],
            "gurobi_config": params,
            "solution_data": get_solution_dict(facility_model)
        }
        write_json(solution_output_path, solution_dict)

if __name__=="__main__":
    run(sys.argv[1:])
    