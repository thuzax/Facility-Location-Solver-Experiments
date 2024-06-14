import os
import sys
import json

if __name__=="__main__":
    if (len(sys.argv) < 1):
        print("Needs:")
        print(" 1. Inputs Directory")
        print(" 2. Configurations Directory")
        print(" 3. Outputs Directory")
        exit(0)

    results_dir = sys.argv[1]
    # configs_dir = sys.argv[2]
    # output_dir = sys.argv[3]
    
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
            obj_value = data["solution_data"]["objective"]
            has_feasible = data["solution_data"]["feasible_found"]
            is_opt = data["solution_data"]["is_optimal"]
            gap = data["solution_data"]["gap"]
        files_data[os.path.basename(result).split(".")[0]] = {
            "time": total_time,
            "node_count": total_nodes,
            "objective": obj_value,
            "feasible": has_feasible,
            "is_optimal": is_opt,
            "gap": gap
        }
    
    results_main_data = "./results_main_data.json"
    with open(results_main_data, "w") as output:
        json.dump(files_data, output, indent=4)

    

