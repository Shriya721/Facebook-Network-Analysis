###########################################################
    #  Computer Project #11
    #
    #  Algorithm
    #    user enters a user id to generate an EgoNet
    #    reprompts if user does not enter correct id
    #    diplays choices for EgoNet calculations
    #    user inputs their choice 
    #       if user enters choice 1 then user enters circle name to calculate similarity
    #       displays feature and feature similarity
    #       if user enters choice 2 then program calculates size of EgoNet
    #       if user enters choice 3 then user enters feature name and id
    #       displays the feature index for specific id
    #       if user enters choice 4 then program calculates the efficiency of the EgoNet
    #       if user enters a form of quit the program quits
    #       if the user enters anything but the choices mentioned above then program reprompts and asks for user to input correct number   
    #    user can quit the program anytime
    ###########################################################
#import modules from various classes
from EgoNet import EgoNet
from Node import Node
from Feature import Feature
from Circle import Circle
from operator import itemgetter

def get_ego_net_files():
    '''
    prompts user to enter a valid file
    opens the valid file the user entered
    if there is an invlaid file then prompts user to enter another file
    returns the opened files
    '''
    y1 = "_ego_features.txt"
    y2 = "_ego_net_features.txt"
    y3 = "_alters_features.txt"
    y4 = "_ego_net_connections.txt"
    y5 = "_circles.txt"
    x = input("Enter user id to generate EgoNet: ")
    while True:
        try:
            fp1 = open(x+y1)
            fp2 = open(x+y2)
            fp3 = open(x+y3)
            fp4 = open(x+y4)
            fp5 = open(x+y5)

            return (int(x),fp1,fp2,fp3,fp4,fp5)

        except FileNotFoundError:
            print("File not found for ego_id: ",x)
            x = input("Enter user id to generate EgoNet: ")

def get_ego_net_features(fp):
    '''
    fp: file that user enters
    splits all the information in the file
    gets the feature id and position
    gets feature name and joins the name together
    adds all these components to the dictionary
    returns the dictionary
    '''
    ego_net_dict = {} #initialize dictionary
    for line in fp: #goes through each line in the file
        pieces = line.split() #splits and creates list with information
        position = int(pieces[0]) #gets the feature position
        ids = str(pieces[3]) #gets the feature id
        feature_piece = pieces[1].split(";") #gets each feature name
        feature_name_list = []
        #goes through feature name list and gets the feature names
        for i in feature_piece:
            if i == 'id' or i == 'anonymized': #stops if feature name equals either one of these two names
                break #stops the loop
                
            else:
                feature_name_list.append(i) #appends feature name to a list
                
        feature_name = '_'.join(feature_name_list) #joins the feature names in the list with feature names
        ego_net_dict[position] = (feature_name,ids) #adds all components to the dictionary
    return  ego_net_dict #returns the dictionary
def add_ego_net_features_to_ego(ego, ego_feature_file, ego_net_features):
    '''Reads a one-line file of features for the ego node'''
    line_list = ego_feature_file.readline().split()    # read one line
    # i is the index, digit is the value
    for i,digit in enumerate(line_list):
        # in order to add a feature we must create a Feature instance
        ego.add_feature(i,Feature(ego_net_features[i][1], ego_net_features[i][0],int(digit))) 
    return ego

def add_alters_to_ego_net(ego_net,alter_features_file,ego_net_features):
    '''
    ego_net: object of EgoNet class
    alter_features_file: file the user inputs
    ego_net_features: used to access feature dictionary
    function splits information in file
    gets the feature name and value using the different classes
    calls add_feature function from Node class and adds that to a node
    uses add_alter_node function from EgoNet class using ego_net object
    returns the ego_net object
    '''
    for line in alter_features_file: #goes through each line in the file
        pieces = line.split() #splits and creates list with information
        node_id = int(pieces[0]) #gets the id
        new_node = Node(node_id, len(pieces[1:])) #calls Node class using id and other information
        
        for i ,j in enumerate(pieces[1:]): #uses enumerate to get index and value of the information
            feature_name = ego_net_features[i][1] #gets feature name
            feature_value = ego_net_features[i][0] #gets feature value
            feature_object = Feature(feature_name, feature_value,int(j)) #calls Feature class to get information
            new_node.add_feature(i,feature_object) #calls the add_feature funtion from the Node class and adds that to a node
        ego_net.add_alter_node(new_node) #uses add_alter_node function from EgoNet class using ego_net object 
    return ego_net #returns the ego_net object

def add_connections_to_ego_net(ego_net,connections_file):
    '''
    ego_net: object of EgoNet class
    connections_file: file the user inputs
    function splits information in file
    gets alters and ids of alters
    compares information in file
    uses add_connection_between_alters function from EgoNet class using ego_net object
    returns the ego_net object
    '''
    for line in connections_file: #goes through each line in the file
        pieces = line.split() #splits and creates list with information
        alters = ego_net.get_alters() #gets the alters
        for i in alters: #loops through all the alters
            ids = i.get_id() #gets the id of each alter
            if ids == int(pieces[0]): #compares id to information in the file
                first_node = i #if statement is true then sets the first node to that alter value
            elif ids == int(pieces[1]): #same thing as before but compares to different information in file
                second_node = i
        ego_net.add_connection_between_alters(first_node, second_node) #uses add_connection_between_alters function from EgoNet class using ego_net object
    return ego_net #returns the ego_net object

def add_circles_to_ego_net(ego_net,circles_file):
    '''
    ego_net: object of EgoNet class
    circles_file: file the user inputs
    function compares information in file to alter ids
    adds alter to node set if conditions are satisfied
    uses add_circle fucntion from EgoNet class using ego_net object
    return the ego_net object 
    '''
    for line in circles_file: #goes through each line in the file
        pieces = line.split() #splits and creates list with information
        circle_name = pieces [0] #gets circle name
        alters = ego_net.get_alters()  #gets the alters
        node_id_set = set() #creates a set with the node id
        for i in pieces[1:]: #loops through information in the file
            for j in alters: #loops through all the alters in the file
                if j.get_id() == int(i): #compares id to information in file
                    node_id_set.add(j) #if statement is true then adds alters to node set
        ego_net.add_circle(circle_name,node_id_set) #uses add_circle function from EgoNet class using the ego_net object
    return ego_net #returns the ego_net object

def calculate_circle_similarity(ego_net,circle_name):
    '''
    ego_net: object of EgoNet class
    circle_name: parameter to call circle function
    function iterates through features and alters
    calculates the circle similarity based on circle similarity
    returns the dictionary with circle similarity information
    '''
    circle = {} #initialize dictionary
    other_circle = ego_net.get_circle(circle_name) #gets circles using circle_name parameter and function from EgoNet class
    alters = other_circle.get_alters() #gets the alters
    for i in ego_net.get_ego_net_features(): #loops through all the ego_net features
        value = 0 #initializes value to 0
        for j in alters: #loops through all the alters
            count = j.get_feature_value(i) #count's value are the alters features
            value += count #adds the count value to the variable value
        circle[i] = value #creates the circle similarity dictionary
    return circle #returns the circle similarity dictionary
            
def calculate_ego_E_I_index(ego_net,feature_name,feature_id):
    '''
    ego_net: object of EgoNet class
    feature_name: parameter to call feature function
    feature_id: parameter to call feature function
    function gets feature position using the paramters
    iterates through alters and gets feature value at specific position
    calculates the ego index
    returns the result of the calculation
    '''
    feature_position = ego_net.get_feature_pos(feature_name,feature_id) #gets the feature position using the parameters
    num_alters = ego_net.get_alters() #get the alters
    count = 0 #initializes count to 0
    for i in num_alters: #loops through all the alters
        value = i.get_feature_value(feature_position) #gets the feature value for the alter at the specific position
        if value == 0: #checks if value is 0 or 1
            continue
        else:
            count +=1 #if value is 1 then increments the count variable by 1
    #performs the ego index calculation using the formula given in the project pdf
    calculation = ((len(num_alters )- count)-count)/((len(num_alters )- count) + count)
    return calculation #returns the result of the calculation

def calculate_ego_net_effective_size(ego_net):
    '''
    ego_net: object of EgoNet class
    function gets the alter node count
    iterates through the alters
    calculated the connection with the information found
    calculated the ego net effective size
    returns the result of the calculation
    '''
    alter_count = ego_net.get_alter_node_count() #gets alter node count
    count = 0 #initializes count to 0
    for i in ego_net.get_alters(): #loops through the alters
        connect = len(ego_net.get_alter_connections(i))-1 #calculates the connection
        count+=connect #adds the connection value to the count variable
    calculation = alter_count - (count/alter_count) #performs the ego net effective size calculation with the data found
    return calculation #returns the result of the calculation
def calculate_ego_net_efficiency(ego_net):
    '''
    ego_net: object of EgoNet class
    function calculates the ego net efficiency
    returns the result of the calculation
    '''
    #performs the ego net efficiency calculation
    calculation = calculate_ego_net_effective_size(ego_net)/ego_net.get_alter_node_count()
    return calculation #returns the result of the calculation 
def print_choices():
    '''
    function prints the choices the user selects
    returns nothing
    '''
    #function prints the choices the user selects
    print("Choices for Ego Net calculation: ")
    print("1 - Top 5 similar features in a circle")
    print("2 - Calculate effective size of Ego Net")
    print("3 - Calculate circle E/I index")
    print("4 - Calculate Ego Net efficiency")
    print("q/Q - Quit ")

def main():
    '''
    function provided but basically does what was mentioned in the function header
    '''
    ego_id,ego_feature_file,ego_net_features_file,alter_features_file,connections_file,circles_file=get_ego_net_files()
    ego_net_features = get_ego_net_features(ego_net_features_file)

    ego = Node(ego_id,len(ego_net_features))

    ego = add_ego_net_features_to_ego(ego,ego_feature_file,ego_net_features)

    FacebookNet = EgoNet(ego,ego_net_features)

    FacebookNet = add_alters_to_ego_net(FacebookNet,alter_features_file,ego_net_features)

    FacebookNet = add_connections_to_ego_net(FacebookNet,connections_file)

    FacebookNet = add_circles_to_ego_net(FacebookNet,circles_file)

    while True:
        print_choices()
        choice = input("Enter choice: ").strip()
        circle_names = FacebookNet.get_circle_names()
        if choice == "1":
            circle_name = input("Enter circle name to calculate similarity: ")
            circle_size = (FacebookNet.get_circle(circle_name).get_circle_size())
            if circle_name in circle_names:
                similarity_dict = calculate_circle_similarity(FacebookNet,circle_name)
            else:
                print("Circle name not in Ego Net's circles. Please try again!")
                continue
            similarity_dict = dict(sorted(similarity_dict.items(),key=itemgetter(1),reverse=True)[:5])
            for feature_pos in similarity_dict:
                feature_name_id = FacebookNet.get_ego_net_feature(feature_pos)
                feature_similarity = (similarity_dict[feature_pos])/(circle_size)
                print(f"Feature: {feature_name_id}")
                print(f"Feature Similarity in {circle_name}: {feature_similarity} \n")
            print()
        elif choice == '2':
            print(f"Effective size of the Ego Net is: {calculate_ego_net_effective_size(FacebookNet)}")
            print()
        elif choice == '3':
            feature_name = input("Enter feature name to calculate E/I index: ")
            feature_id = (input(f"Enter id for {feature_name} to calculate E/I index: "))
            e_i_index = calculate_ego_E_I_index(FacebookNet,feature_name,feature_id)
            if e_i_index < 0:
                print(f"Ego is more homophilic for {feature_name}_{feature_id} with an E/I index of {e_i_index}")
                print()
            else:
                print(f"Ego is more heterophilic for {feature_name}_{feature_id} with an E/I index of {e_i_index}")
                print()

        elif choice == '4':
            ego_net_efficiency = calculate_ego_net_efficiency(FacebookNet)
            print("The efficiency of the Ego Net is: {:.2f}%".format(100*ego_net_efficiency))
            print()

        elif choice in 'qQ':
            break
        else:
            print("Incorrect Choice. Please try again.")
            continue
    ego_feature_file.close()
    ego_net_features_file.close()
    alter_features_file.close()
    connections_file.close()

if __name__ == "__main__":
   main()