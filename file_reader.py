import os
import sys
import numpy

def read_facility(line, caps, fixcos, pos_x, pos_y, names):
    """
    Read the information of one facility from a line and insert in the parameters arrays
    line: input file line with the information
    caps: array with the capacities of all the facilities
    fixcos: array with the fixed costs of the facilities
    pos_x: array with the x coordenate of the facilities
    pos_y: array with the y coordenate of the facilities
    names: array with the names of the facilities
    """
    line_splitted = line.split()
    caps.append(int(line_splitted[0]))
    fixcos.append(int(line_splitted[1]))
    pos_x.append(int(line_splitted[3]))
    pos_y.append(int(line_splitted[4]))
    names.append(line_splitted[5])

def read_attending_point(line, demands, pos_x, pos_y, names):
    """
    Read the information of one point to be attended from a line and insert in the arrays
    line: input file line with the information
    demands: array with the fixed costs of the facilities
    pos_x: array with the x coordenate of the facilities
    pos_y: array with the y coordenate of the facilities
    names: array with the names of the facilities
    """
    line_splitted = line.split()
    demands.append(int(line_splitted[0]))
    pos_x.append(int(line_splitted[1]))
    pos_y.append(int(line_splitted[2]))
    names.append(line_splitted[3])



def read_input_file(file_name):
    with open(file_name, "r") as input_file:
        line_index = 0
        line = input_file.readline()
        continue_reading = True

        facilities_capacities = []
        facilities_fixed_costs = []
        facilities_x_coords = []
        facilities_y_coords = []
        facilities_names = []

        attend_demands = []
        attend_x_coord = []
        attend_y_coord = []
        attend_names = []

        attend_costs_matrix =[]

        while (line and continue_reading):
            line_index += 1
            if (line[:10] == "#customers"):
                line_splitted = line.split(";")
                number_to_attend = int(line_splitted[0].split()[-1])
                number_possible_facilities = int(line_splitted[1].split()[-1])
            
            elif ("[DEPOTS]" in line):
                line = input_file.readline()
                line_index += 1
                end_facilities_lines = line_index + number_possible_facilities
                for i in range(line_index, end_facilities_lines):
                    line = input_file.readline()
                    read_facility(
                        line,
                        facilities_capacities,
                        facilities_fixed_costs,
                        facilities_x_coords,
                        facilities_y_coords,
                        facilities_names
                    )
                line_index = end_facilities_lines

            elif ("[CUSTOMERS]" in line):
                line = input_file.readline()
                line_index += 1
                end_attend_lines = line_index + number_to_attend
                for i in range(line_index, end_attend_lines):
                    line = input_file.readline()
                    read_attending_point(
                        line,
                        attend_demands,
                        attend_x_coord,
                        attend_y_coord,
                        attend_names
                    )
                line_index = end_attend_lines

            elif ("[COSTMATRIX]" in line):
                line = input_file.readline()
                line = input_file.readline()
                line = input_file.readline()
                line_index += 3
                end_cost_matrix_lines = line_index + number_possible_facilities
                for i in range(number_possible_facilities):
                    attend_costs_matrix.append([])
                    line = input_file.readline()
                    line_splitted = line.split()
                    for j in range(number_to_attend):
                        attend_costs_matrix[i].append(float(line_splitted[j]))

                line_index += number_possible_facilities
            line = input_file.readline()


        facility_data = {
            "capacities": facilities_capacities,
            "fixed_costs": facilities_fixed_costs,
            "x_coords": facilities_x_coords,
            "y_coords": facilities_y_coords,
            "names": facilities_names
        }

        points_to_attend_data = {
            "demands": attend_demands,
            "x_coord": attend_x_coord,
            "y_coord": attend_y_coord,
            "names": attend_names
        }

        return (facility_data, points_to_attend_data, attend_costs_matrix)
            
