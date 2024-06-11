import sys
from file_reader import read_input_file
from model_manager import *

if __name__=="__main__":
    if (len(sys.argv) < 2):
        print("needs input file")
    data = read_input_file(sys.argv[1])
    facilities_data, points_to_attend_data, attend_costs_matrix = data

    facility_model = create_model(
        facilities_data, 
        points_to_attend_data, 
        attend_costs_matrix
    )

    out_path = sys.argv[1].split("/")
    out_path[-1] = out_path[-1].split(".")[0]
    out_path = "/".join(out_path) + ".lp"
    facility_model.write(out_path)

    facility_model.optimize()

    # for i in range(len(facilities_data["capacities"])):
    #     v = facility_model.getVarByName(get_var_open_facility_name(i))
    #     print(v.VarName, v.X)