import fuzzy

# yapf: disable
## Test case fuzzy subset for trimf
# f_ssets = [[ # error
#             [-10,-10,-5],   # -ve medium   
#             [-10,-5 , 0],    # -ve small
#             [-5 , 0 , 5],   # zero
#             [ 0 , 5 , 10],   # +ve small
#             [ 5 ,10 , 10], # +ve medium
#            ],        
#             # delta_error
#            [          
#             [-10,-10,-5],   # -ve medium   
#             [-10,-5 , 0],    # -ve small
#             [-5 , 0 , 5],   # zero
#             [ 0 , 5 , 10],   # +ve small
#             [ 5 ,10 , 10], # +ve medium
#            ],              
#             # u
#            [                 
#             [-10,-10,-5],  # -ve medium
#             [-10,-5 , 0],  # -ve small
#             [-5 , 0 , 5],  # zero
#             [ 0 , 5 , 10], # +ve small
#             [ 5 ,10 , 10], # +ve medium
#            ] 
#           ]
# # yapf: enable

# io_ranges = [  # range of e
#               [-10,10],
#                # range of d_e
#               [-10,10],
#                # range of u
#               [-10,10]
#             ]

# mf_types = ['trimf','trimf','trimf']

## fuzzy subset test case for gaussmf
f_ssets = [[ # error
            [-180,70], # -ve medium   
            [-50,20], # -ve small
            [ 0 ,20], # zero
            [50 ,20], # +ve small
            [180 ,70], # +ve medium
           ],        
            # delta_error
           [          
            [-180,70], # -ve medium   
            [-50,20], # -ve small
            [ 0 ,20], # zero
            [50 ,20], # +ve small
            [180 ,70], # +ve medium
           ],              
            # u
           [                 
            [-3,2], # -ve medium   
            [-1,2], # -ve small
            [ 0,1], # zero
            [ 1,2], # +ve small
            [ 3,2], # +ve medium           
           ] 
          ]
# yapf: enable

io_ranges = [  # range of e
              [-180,180],
               # range of d_e
              [-180,180],
               # range of u
              [-10,10]
            ]

mf_types = ['gaussmf','gaussmf','gaussmf']

def main():
  x = fuzzy.Fuzzy(mf_types, f_ssets)
  x.error = -20
  x.delta_e = -20
  x.io_ranges = io_ranges
  print x.run() 

if __name__ == '__main__':
  main()
