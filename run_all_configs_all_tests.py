import os
import sys
from main import run
from get_results_data import get_results_data, join_resumes_csv
from solve_relaxation import solve_relaxation


def get_input_files(input_dir):
    input_files = []
    for item in os.listdir(input_dir):
        item_path = os.path.join(input_dir, item)
        if (os.path.isfile(item_path)):
            input_files.append(item_path)
    
    input_files = sorted(input_files)
    return input_files

def get_configurations(configs_dir):
    configurations = []
    for item in os.listdir(configs_dir):
        item_path = os.path.join(configs_dir, item)
        if (os.path.isfile(item_path)):
            configurations.append(item_path)
    configurations = sorted(configurations)
    return configurations


def get_outputs_paths(
    output_models_dir, 
    output_results_dir, 
    output_logs_dir,
    solve_relaxation_only
):
    output_model_files = []
    output_result_files = []
    output_log_files = []

    for input_file in input_files:
        output_name = os.path.basename(input_file).split(".")[0]
        output_model_files.append([])
        output_result_files.append([])
        output_log_files.append([])

        for j in range(len(configurations)):
            config_name = os.path.basename(configurations[j]).split(".")[0]
            if (solve_relaxation_only):
                config_name = "linear"

            output_model_file_path = os.path.join(
                output_models_dir, 
                config_name,
                output_name + "_" + config_name + ".lp"
            )
            output_result_file_path = os.path.join(
                output_results_dir, 
                config_name, 
                output_name + "_" + config_name + "_out.json"
            )

            output_log_file_path = os.path.join(
                output_logs_dir, 
                config_name, 
                output_name + "_" + config_name + ".log"
            )

            output_model_files[-1].append(output_model_file_path)
            output_result_files[-1].append(output_result_file_path)
            output_log_files[-1].append(output_log_file_path)

    return (output_model_files, output_result_files, output_log_files)


def print_arguments(args):
    print("ARGUMENTS: ")
    print("\tINPUT FILE:\t", args[0]) 
    print("\tCONFIGURATION FILE:\t", args[1])
    print("\tOUTPUT RESULT PATH:\t", args[2])
    print("\tOUTPUT MODEL PATH:\t", args[3])
    print("\tLOG FILE PATH:\t", args[4])
            

if __name__=="__main__":
    if (len(sys.argv) < 4):
        print("Needs:")
        print(" 1. Inputs Directory")
        print(" 2. Configurations Directory")
        print(" 3. Outputs Directory")
        print(" 4. Value 1 to solve Relaxation only [optional]")
        exit(0)

    input_dir = sys.argv[1]
    configs_dir = sys.argv[2]
    output_dir = sys.argv[3]
    solve_relaxation_only = False
    if (len(sys.argv) == 5):
        if (sys.argv[4] == "1"):
            solve_relaxation_only = True
    
    # Get input files names
    input_files = get_input_files(input_dir)

    # Get configurations files names
    configurations = get_configurations(configs_dir)

    output_models_dir = os.path.join(output_dir, "model")
    output_results_dir = os.path.join(output_dir, "results")
    output_logs_dir = os.path.join(output_dir, "logs")

    if (not os.path.exists(output_models_dir)):
        os.makedirs(output_models_dir)
    if (not os.path.exists(output_results_dir)):
        os.makedirs(output_results_dir)
    if (not os.path.exists(output_logs_dir)):
        os.makedirs(output_logs_dir)
    
    outputs = get_outputs_paths(
        output_models_dir,
        output_results_dir,
        output_logs_dir,
        solve_relaxation_only
    )

    output_model_files = outputs[0]
    output_result_files = outputs[1]
    output_log_files = outputs[2]
    
    out_res_dir = None
    out_models_dir = None
    out_logs_dir = None
    for i in range(len(input_files)):
        if (solve_relaxation_only):
            out_res_dir = os.path.join(output_results_dir, "linear")
            out_models_dir = os.path.join(output_models_dir, "linear")
            out_logs_dir = os.path.join(output_logs_dir, "linear")

            if (not os.path.exists(out_res_dir)):
                os.makedirs(out_res_dir)
            if (not os.path.exists(out_models_dir)):
                os.makedirs(out_models_dir)
            if (not os.path.exists(out_logs_dir)):
                os.makedirs(out_logs_dir)
            
            output_name = os.path.basename(input_files[i]).split(".")[0]

            args = [
                input_files[i],
                "0",
                os.path.join(out_res_dir, output_name + "_out_linear.json"),
                os.path.join(out_models_dir, output_name + "_linear.lp"),
                os.path.join(out_logs_dir, output_name + "_linear.log")
            ]

            print_arguments(args)
            solve_relaxation(args)
            continue

        for j in range(len(configurations)):
            config_name = os.path.basename(configurations[j]).split(".")[0]
            out_res_dir = os.path.join(output_results_dir, config_name)
            out_models_dir = os.path.join(output_models_dir, config_name)
            out_logs_dir = os.path.join(output_logs_dir, config_name)

            if (not os.path.exists(out_res_dir)):
                os.makedirs(out_res_dir)
            if (not os.path.exists(out_models_dir)):
                os.makedirs(out_models_dir)
            if (not os.path.exists(out_logs_dir)):
                os.makedirs(out_logs_dir)
            
            args = [
                input_files[i], 
                configurations[j],
                output_result_files[i][j],
                output_model_files[i][j],
                output_log_files[i][j]
            ]

            print_arguments(args)
            run(args)
    
    resumes_dir = os.path.join(output_results_dir, "resumes")
    for j in range(len(configurations)):
        
        if (solve_relaxation_only):
            config_name = "linear"
      
        config_name = os.path.basename(configurations[j]).split(".")[0]  
        resume_name = "resume_ " + config_name + "_data_out.json"
        
        if (not os.path.exists(resumes_dir)):
            os.makedirs(resumes_dir)

        get_results_data([
            os.path.join(out_res_dir),
            os.path.join(resumes_dir, resume_name)
        ])

    join_resumes_csv([resumes_dir, output_results_dir])