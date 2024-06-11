\ Model Capacited Facility Location
\ LP format - for model browsing. Use MPS format to capture full model detail.
Minimize
  195.4861 percentage_0_0 + 149.826 percentage_1_0 + 46.1261 percentage_2_0
   + 239.4284 percentage_3_0 + 181.8186 percentage_4_0
   + 169.5767 percentage_0_1 + 124.543 percentage_1_1
   + 97.0611 percentage_2_1 + 69.0986 percentage_3_1
   + 223.3077 percentage_4_1 + 946 open_facility_0 + 670 open_facility_1
Subject To
 full_attendance_0: percentage_0_0 + percentage_0_1 = 1
 full_attendance_1: percentage_1_0 + percentage_1_1 = 1
 full_attendance_2: percentage_2_0 + percentage_2_1 = 1
 full_attendance_3: percentage_3_0 + percentage_3_1 = 1
 full_attendance_4: percentage_4_0 + percentage_4_1 = 1
 open_facility_and_capacity_0: 30 percentage_0_0 + 16 percentage_1_0
   + 17 percentage_2_0 + 33 percentage_3_0 + 25 percentage_4_0
   - 76 open_facility_0 <= 0
 open_facility_and_capacity_1: 30 percentage_0_1 + 16 percentage_1_1
   + 17 percentage_2_1 + 33 percentage_3_1 + 25 percentage_4_1
   - 45 open_facility_1 <= 0
 aggregated_capacities: 76 open_facility_0 + 45 open_facility_1 >= 121
 implied_bound_0_0: percentage_0_0 - open_facility_0 <= 0
 implied_bound_1_0: percentage_1_0 - open_facility_0 <= 0
 implied_bound_2_0: percentage_2_0 - open_facility_0 <= 0
 implied_bound_3_0: percentage_3_0 - open_facility_0 <= 0
 implied_bound_4_0: percentage_4_0 - open_facility_0 <= 0
 implied_bound_0_1: percentage_0_1 - open_facility_1 <= 0
 implied_bound_1_1: percentage_1_1 - open_facility_1 <= 0
 implied_bound_2_1: percentage_2_1 - open_facility_1 <= 0
 implied_bound_3_1: percentage_3_1 - open_facility_1 <= 0
 implied_bound_4_1: percentage_4_1 - open_facility_1 <= 0
Bounds
 percentage_0_0 <= 1
 percentage_1_0 <= 1
 percentage_2_0 <= 1
 percentage_3_0 <= 1
 percentage_4_0 <= 1
 percentage_0_1 <= 1
 percentage_1_1 <= 1
 percentage_2_1 <= 1
 percentage_3_1 <= 1
 percentage_4_1 <= 1
Binaries
 open_facility_0 open_facility_1
End
