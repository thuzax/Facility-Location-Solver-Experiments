import os
import sys
import json

def get_results_data(args):
    if (len(args) < 2):
        print("Needs:")
        print(" 1. Inputs Directory")
        print(" 2. Output File Name (JSON)")
        exit(0)

    results_dir = args[0]
    output_file_name = args[1]
    # Get results files names
    results_files = []
    for item in os.listdir(results_dir):
        item_path = os.path.join(results_dir, item)
        if (os.path.isfile(item_path)):
            results_files.append(item_path)
    
    results_files = sorted(results_files)
    files_data = {}
    for result in results_files:
        print(result)
        if (not os.path.isfile(result)):
            continue
        with open(result) as result_file:
            data = json.load(result_file)
            total_time = data["solution_data"]["total_time"]
            total_nodes = data["solution_data"]["node_count"]
            has_feasible = data["solution_data"]["feasible_found"]
            is_opt = data["solution_data"]["is_optimal"]
            obj_value = data["solution_data"]["objective"]
            dual_bound = data["solution_data"]["dual_bound"]
            gap = data["solution_data"]["gap"]

        files_data[os.path.basename(result).split(".")[0]] = {
            "time": total_time,
            "node_count": total_nodes,
            "objective": obj_value,
            "feasible": has_feasible,
            "is_optimal": is_opt,
            "dual_bound": dual_bound,
            "gap": gap
        }

    with open(output_file_name, "w") as output:
        json.dump(files_data, output, indent=4)


if __name__=="__main__":
    get_results_data(sys.argv[1:])
    

    

