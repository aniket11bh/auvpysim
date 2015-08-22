import fuzzy
# yapf: disable
f_ssets = [[ # error
            [-180,-180,30],   # -ve medium   
            [-60,-30 , 0],    # -ve small
            [-30 , 0 , 30],   # zero
            [ 0 , 30 , 60],   # +ve small
            [ 30 ,180 , 180], # +ve medium
           ],        
            # delta_error
           [          
            [-180,-180,30],   # -ve medium
            [-60,-30 , 0],    # -ve small
            [-30 , 0 , 30],   # zero
            [ 0 , 30 , 60],   # +ve small
            [ 30 ,180 , 180], # +ve medium
           ],              
            # u
           [                 
            [-10,-10,-5],  # -ve medium
            [-10,-5 , 0],  # -ve small
            [-5 , 0 , 5],  # zero
            [ 0 , 5 , 10], # +ve small
            [ 5 ,10 , 10], # +ve medium
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

mf_types = ['trimf','trimf','trimf']

def main():
  x = fuzzy.Fuzzy(mf_types, f_ssets)
  x.error = 2.5
  x.delta_e = 0 
  x.io_ranges = io_ranges
  print x.run() 

if __name__ == '__main__':
  main()
