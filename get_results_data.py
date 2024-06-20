import os
import sys
import json
import pandas

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
    results_files_data = {}
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

        results_files_data[os.path.basename(result).split(".")[0]] = {
            "time": total_time,
            "node_count": total_nodes,
            "objective": obj_value,
            "feasible": has_feasible,
            "is_optimal": is_opt,
            "dual_bound": dual_bound,
            "gap": gap
        }

    with open(output_file_name, "w") as output:
        json.dump(results_files_data, output, indent=4)
    
    print(output_file_name)
    for name, data in results_files_data.items():
        header = results_files_data[name].keys()
        config_name = "_".join(name.split(".")[0].split("_")[-3:-1])
        header = list(header)
        
    
    header.insert(0, config_name)
    
    output_csv_name = os.path.basename(output_file_name).split(".")[0] + ".csv"
    output_csv_name = os.path.join(
        os.path.dirname(output_file_name), 
        output_csv_name
    )
    
    print(header)
    print(results_files_data)
    
    with open(output_csv_name, "w") as output:
        csv_data = []
        for name, data in results_files_data.items():
            csv_data.append([])
            csv_data[-1].append(name)
            for key, value in data.items():
                if (value is None):
                    value = "-"
                csv_data[-1].append(value)
        
        data_frame = pandas.DataFrame(csv_data, columns=header)
        data_frame.to_csv(output_csv_name, header=True, index=False)
        print(data_frame)

if __name__=="__main__":
    get_results_data(sys.argv[1:])
    

    

