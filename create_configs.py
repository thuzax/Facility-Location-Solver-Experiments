
import os
import sys
import itertools
import json

def get_cuts(cuts_level=0):
    ''' 
    Returns a dict blocking every Gurobi cut parameter value

        If cuts_level is 0, no personalized configuration will be done
        Otherwise, only MIRCuts and ImpliedCut is currently activated
    
        If cut level is 2, then the active cuts will have an aggressive approach
        Otherwise it will have an moderated approach
    '''
    if (cuts_level == 0):
        return {}

    elif (cuts_level != 2):
        cuts = {
            "bqp_cut": 0,
            "clique_cut": 0,
            "cover_cut": 0,
            "flow_cover_cut": 0,
            "flow_path_cut": 0,
            "gub_cover_cut": 0,
            "implied_cut": 1,
            "inf_proof_cut": 0,
            "lift_project_cut": 0,
            "mip_sep_cut": 0,
            "mir_cut": 1,
            "mixing_cut": 0,
            "mod_k_cut": 0,
            "network_cut": 0,
            "proj_implied_cut": 0,
            "psd_cut": 0,
            "relax_lift_cut": 0,
            "rlt_cut": 0,
            "strong_cg_cut": 0,
            "sub_mip_cut": 0,
            "zero_half_cut": 0
        }
    elif(cuts_level == 2):
        cuts = {
            "bqp_cut": 0,
            "clique_cut": 0,
            "cover_cut": 0,
            "flow_cover_cut": 0,
            "flow_path_cut": 0,
            "gub_cover_cut": 0,
            "implied_cut": 2,
            "inf_proof_cut": 0,
            "lift_project_cut": 0,
            "mip_sep_cut": 0,
            "mir_cut": 2,
            "mixing_cut": 0,
            "mod_k_cut": 0,
            "network_cut": 0,
            "proj_implied_cut": 0,
            "psd_cut": 0,
            "relax_lift_cut": 0,
            "rlt_cut": 0,
            "strong_cg_cut": 0,
            "sub_mip_cut": 0,
            "zero_half_cut": 0
        }

    return cuts

if __name__=="__main__":
    if (len(sys.argv) < 2):
        print("Needs:")
        print(" 1. Output Directory")
        exit(0)

    output_dir = sys.argv[1]

    time = 180
    presolve = 0
    branching = [0, 1, 2, 3]
    cuts_level = [1, 2] # 1. moderated, 2. aggressive
    node_selection = [1, 2, 3]
    
    
    configurations = []
    configuration_std_no_presolve = {
        "time": time,
        "presolve": presolve
    }
    configurations.append(configuration_std_no_presolve)
    
    combinations = list(itertools.product(*
        [branching, cuts_level, node_selection, [time], [presolve]]
    ))
    
    for combination in combinations:
        configuration = {
            "branching": combination[0],
            "node_selection": combination[2],
            "time": combination[3],
            "presolve": combination[4]
        }
        cuts = get_cuts(combination[1])
        for key, value in cuts.items():
            configuration[key] = value
        configurations.append(configuration)
    
    configurations_names = []
    for i in range(len(configurations)):
        configurations_names.append("configuration_" + str(i) + ".json")
    
    configurations_names[0] = "configuration_std_no_pre.json"

    if (not os.path.exists(output_dir)):
        os.makedirs(output_dir)
    
    configurations_path = [
        os.path.join(output_dir, configuration_name)
        for configuration_name in configurations_names
    ]

    for i in range(len(configurations_path)):
        with open(configurations_path[i], "w") as config_file:
            json.dump(configurations[i], config_file, indent=4)