import os
import sys
from main import run

if __name__=="__main__":
    if (len(sys.argv) < 4):
        print("Needs:")
        print(" 1. Inputs Directory")
        print(" 2. Configurations Directory")
        print(" 3. Outputs Directory")
        exit(0)

    input_dir = sys.argv[1]
    configs_dir = sys.argv[2]
    output_dir = sys.argv[3]
    
    # Get input files names
    input_files = []
    for item in os.listdir(input_dir):
        item_path = os.path.join(input_dir, item)
        if (os.path.isfile(item_path)):
            input_files.append(item_path)
    
    input_files = sorted(input_files)

    # Get configurations files names
    configurations = []
    for item in os.listdir(configs_dir):
        item_path = os.path.join(configs_dir, item)
        if (os.path.isfile(item_path)):
            configurations.append(item_path)
    
    configurations = sorted(configurations)

    output_model_dir = os.path.join(output_dir, "model")
    output_results_dir = os.path.join(output_dir, "results")

    if (not os.path.exists(output_model_dir)):
        os.makedirs(output_model_dir)
    if (not os.path.exists(output_results_dir)):
        os.makedirs(output_results_dir)
    output_models_files = []
    output_results_files = []

    for input_file in input_files:
        output_name = os.path.basename(input_file).split(".")[0]
        output_models_files.append([])
        output_results_files.append([])

        for j in range(len(configurations)):
            config_name = os.path.basename(configurations[j]).split(".")[0]

            output_model_file_path = os.path.join(
                output_model_dir, 
                output_name + "_" + config_name + ".lp"
            )
            output_result_file_path = os.path.join(
                output_results_dir, 
                output_name + "_" + config_name + "_out.json"
            )

            output_models_files[-1].append(output_model_file_path)
            output_results_files[-1].append(output_result_file_path)

    for j in range(len(configurations)):
        args = [
            input_files[0], 
            configurations[j],
            output_results_files[0][j],
            output_models_files[0][j]
        ]
        print("ARGUMENTS: ")
        print("\tINPUT FILE", input_files[0]) 
        print("\tCONFIGURATION FILE", configurations[j])
        print("\tOUTPUT RESULT PATH", output_results_files[0][j])
        print("\tOUTPUT MODEL PATH", output_models_files[0][j])
        
        run(args)
        # for i in range(len(input_files)):
            # run([
            #     input_files[i], 
            #     configurations[j],
            #     output_results_files[i],
            #     output_models_files[i]
            # ])

    
    
    