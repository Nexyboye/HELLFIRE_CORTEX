import numpy as np

def generate_nodes(                         # Generate a 2d array of empty inputs, outputs, and neurons:
    #                                       # - gaps will be filled with zeros
    #                                       # - first values represents size
    #                                       # - the first and last arrays are the input and output layers
    number_of_inputs,                            
    number_of_neurons_array,                
    number_of_outputs                       
):
    #                      csubakkkaaa waaaaa                                   
    nodes_array = [np.zeros(number_of_inputs)]                                  # Initialize with input array
    nodes_array += [np.zeros(neurons) for neurons in number_of_neurons_array]   # Add neuron arrays
    nodes_array.append(np.zeros(number_of_outputs))                             # Add output array
    
    #                              ~<[L]>~ óóóóóóóóó fassssssszzzzzzzz
    max_length = max(len(arr) for arr in nodes_array)
    nodes_array = np.array([np.pad(arr, (0, max_length - len(arr) + 1)) for arr in nodes_array])

    nodes_array[0][0] = number_of_inputs                                        # Add number of inputs
    for nx in range(len(nodes_array)-2):                                        # Add number of neurons per layer
        nodes_array[nx+1][0] = number_of_neurons_array[nx]                      #
    nodes_array[len(nodes_array)-1][0] = number_of_outputs                      # Add number of outputs
    
    print(f"{number_of_inputs} inputs created.")
    number_of_neurons = 0
    for nx in range(len(nodes_array)-2):
        number_of_neurons += nodes_array[nx+1][0]
    print(f"{int(number_of_neurons)} neurons created.")
    print(f"{number_of_outputs} outputs created.")
    
    
    return nodes_array
    
    
def generate_weights(
    nodes_array,
    weight_value_min=0,                     # the weights will have random float values ranging from this value -
    weight_value_max=1                      #       - to this value
):
    weights_array = []
    
    for nx in range(len(nodes_array)-1):                                # generate random values for weights and insert the sizes of layers into 0. index
        layer_length = int(nodes_array[nx][0]*nodes_array[nx+1][0])
        random_array = np.random.uniform(weight_value_min, weight_value_max, layer_length)
        length_array = np.array([layer_length])
        weights_array.append(np.concatenate((length_array, random_array)))
        
    max_length = max(len(arr) for arr in weights_array)
    weights_array = np.array([np.pad(arr, (0, max_length - len(arr) + 1)) for arr in weights_array])
    
    n = 0
    for nx in range(len(weights_array)):
        n += weights_array[nx][0]
    print(f"{int(n)} weights generated in a [{max_length},{len(weights_array)}] matrix")
    
    return weights_array
    
def calculate_network(node_array, weights_array):
    for nx in range(len(weights_array)):
        