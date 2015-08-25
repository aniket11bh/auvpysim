import fuzzy

# yapf: disable
f_ssets = [[ # error
            [-45,-45,-10], # -ve medium   
            [-45,-10 , 0], # -ve small
            [-10, 0  ,10], # zero
            [ 0 , 10 ,45], # +ve small
            [ 10, 45 ,45], # +ve medium
           ],        
            # delta_error
           [          
            [-45,-45,-10], # -ve medium   
            [-45,-10 , 0], # -ve small
            [-10, 0  ,10], # zero
            [ 0 , 10 ,45], # +ve small
            [ 10, 45 ,45], # +ve medium
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
  x.error = -10
  x.delta_e = -10
  x.io_ranges = io_ranges
  print x.run() 

if __name__ == '__main__':
  main()
