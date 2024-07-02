import json
import sys
import os
import random
import matplotlib
import csv
import matplotlib.pyplot as plt
import numpy
import perfprof

def get_parameter_text(parameter):
    if (parameter == "node_selection"):
        return "seleção de nó"
    if (parameter == "branching"):
        return "branching"
    if (parameter == "cut_level"):
        return "agressividade do corte"

def get_metric_name(metric):
    if (metric == "primal"):
        return "função objetivo"
    if (metric == "dual"):
        return "limitante dual"
    if (metric == "gap"):
        return "gap"

def get_branching_strategy_name(code):
    if (code == -1):
        return "Padrão"
    if (code == 0):
        return "PRCB"
    if (code == 1):
        return "PSPB"
    if (code  == 2):
        return "MIB"
    if (code == 3):
        return "SB"
    return None

def get_cuts_aggressiveness_name(code):
    if (code == -1):
        return "Padrão"
    if (code == 0):
        return "Desligado"
    if (code == 1):
        return "Moderado"
    if (code == 2):
        return "Agressivo"
    return None

def get_node_selection_strategy_name(code):
    if (code == 0):
        return "Padrão"
    if (code == 1):
        return "Primal"
    if (code == 2):
        return "Dual"
    if (code == 3):
        return "Bound"
    return None

def get_legend_name(parameter):

    if (parameter == "node_selection"):
        return get_node_selection_strategy_name(key)
    if (parameter == "branching"):
        return get_branching_strategy_name(key)
    if (parameter == "cut_level"):
        return get_cuts_aggressiveness_name(key)

def get_parameter_key_value(parameter, config_data):
    if (parameter == "branching"):
        if (parameter in config_data.keys()):
            return config_data[parameter]
        else:
            if ("linear" in config_path or "no_pre" in config_path):
                return None
            return -1
    if (parameter == "node_selection"):
        if (parameter in config_data.keys()):
            return config_data[parameter]
        else:
            if ("linear" in config_path or "no_pre" in config_path):
                return None
            return 0
    if (parameter == "cut_level"):
        if ("mir_cut" in config_data.keys()):
            return config_data["mir_cut"]
        else:
            if ("linear" in config_path or "no_pre" in config_path):
                return None
            return -1

            

if __name__=="__main__":
    if (len(sys.argv) < 3):
        print("Needs:")
        print(" 1. Data Resumes Directory")
        print(" 2. Input Configurations Directory")
        exit(0)

    resumes_dirs = sys.argv[1]
    configs_dirs = sys.argv[2]
    cont = 0

    primal_values = {}
    dual_values = {}
    gap_values = {}


    for parameter in ["branching", "node_selection", "cut_level"]:
        primal_values[parameter] = {}
        dual_values[parameter] = {}
        gap_values[parameter] = {}

        header = []

        for resume_file in os.listdir(resumes_dirs):
            # if (cont == 2):
            #     continue
            if (resume_file[-4:] == "json"):
                cont += 1

                config = "_".join(resume_file.split("_")[1:-2]).strip() + ".json"

                config_path = os.path.join(configs_dirs, config)
                
                dict_primal = primal_values[parameter]
                dict_dual = dual_values[parameter]
                dict_gap = gap_values[parameter]

                with open(config_path, "r") as config_file:
                    config_data = json.load(config_file)
                    key_value = get_parameter_key_value(parameter, config_data)
                    
                    if (key_value is None):
                        continue

                    if (not key_value in dict_primal.keys()):
                        dict_primal[key_value] = []
                    if (not key_value in dict_dual.keys()):
                        dict_dual[key_value] = []
                    if (not key_value in dict_gap.keys()):
                        dict_gap[key_value] = []

                
                dict_primal[key_value].append([])
                dict_dual[key_value].append([])
                dict_gap[key_value].append([])
                resume_file_path = os.path.join(resumes_dirs, resume_file)


                with open(resume_file_path, "r") as json_file:
                    file_data = json.load(json_file)

                for instance_name in sorted(file_data.keys()):
                    sol_data = file_data[instance_name]

                    dict_primal[key_value][-1].append(sol_data["objective"])
                    dict_dual[key_value][-1].append(sol_data["dual_bound"])
                    dict_gap[key_value][-1].append(sol_data["gap"])

                    instance_name = "_".join(instance_name.split("_")[:3])
                    if (instance_name not in header):
                        header.append(instance_name)

                primal_values[parameter] = dict_primal
                dual_values[parameter] = dict_dual
                gap_values[parameter] = dict_gap


        header.insert(0, "gurobi_code")

        for metric in ["primal", "dual", "gap"]:
            if (metric == "primal"):
                used_dict = primal_values
            if(metric == "dual"):
                used_dict = dual_values
            if (metric == "gap"):
                used_dict = gap_values
            
            best = []
            mean = []
            deviation = []
            n_rep = 0
            order = []
            for key in sorted(used_dict[parameter].keys()):
                order.append(key)
                value = used_dict[parameter][key]
                
                if (metric == "dual"):
                    best.append(numpy.max(value, axis=0).tolist())
                else:    
                    best.append(numpy.min(value, axis=0).tolist())
                
                mean.append(numpy.mean(value, axis=0).tolist())
                deviation.append(numpy.std(value, axis=0).tolist())
                
                if (key != -1):
                    n_rep = len(value)
            
            for analisys_type in ["best", "mean"]:
                if (analisys_type == "best"):
                    data = best
                else:
                    data = mean

                figure_title = "Estratégia de " + get_parameter_text(parameter) 
                figure_title += " (" + get_metric_name(metric) + "): "
                figure_title += "melhor solução" if analisys_type == "best" else "média"
                
                data = numpy.array(data)
                data_copy = numpy.copy(data)
                if (metric == "dual"):
                    data = 10**8/data

                data = numpy.transpose(data)
                numpy.random.seed(0)
                palette = []
                for i in range(numpy.size(data, axis=1)):
                    palette.append("")
                
                plt.title(figure_title)
                perfprof.perfprof(data, linestyle=palette, markersize=4, markevery=[0])
                legend = []
                for key in sorted(used_dict[parameter]):
                    legend.append(get_legend_name(parameter))
                plt.legend(legend)
                plt.xlabel("Razão")
                plt.ylabel("Número de Instâncias")
                fig_path = os.path.join(
                    "./figs/", 
                    parameter + "_" + metric + "_" + analisys_type + ".png"
                )
                plt.savefig(fig_path)
                plt.clf()
                csv_path = os.path.join(
                    "./csvs/", 
                    parameter + "_" + metric + "_" + analisys_type + ".csv"
                )

                data_copy = numpy.transpose(data_copy)
                data_copy = numpy.insert(arr=data_copy, obj=[0], values=order, axis=0)
                data_copy = numpy.transpose(data_copy)
                
                with open(csv_path, 'w') as csvfile:

                    writer = csv.writer(csvfile)
                    writer.writerow(header)
                    writer.writerows(data_copy)

