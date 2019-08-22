import Circle #import circle class

class EgoNet:
    def __init__(self,ego,ego_net_features):
        '''
        ego: represents the Ego node for the EgoNet. type - Node object
        ego_net_features: represents the features for our Ego Net. type - dict where key = feature
        function initializes all the parameters
        returns nothing
        '''
        self.__ego = ego #Represents the Ego node for the EgoNet. type - Node object
        self.__social_network = {} #Represents the social network graph. type - dict where key = Node object 			        and value = list of Node objects key is connected to
        self.__social_network[ego] = set() #Represents the social network graph. type - dict where key = Node object 			        and value = list of Node objects key is connected to
        self.__alter_node_count = 0 #Represents the total number of alter nodes connected to our Ego
        self.__circles = {} #Represents the circles formed in our EgoNet. type - dict where key = circle name		      and value = list of Node objects in the circle
        self.__ego_net_features = ego_net_features #Represents the features for our Ego Net. type - dict where key = feature			           position in feature file (type - int) and value = tuple of feature name and			          feature id. This does not contain Feature objects but just strings. 


    def get_alter_node(self,node_id):
        '''
        node_id: parameter for node
        function gets the alter nodes by comparing node ids
        returns the nodes object or returns None depending on if statement is true or not
        '''
        for nodes in self.__social_network: #loops through nodes in social network dictionary
            if node_id == nodes.get_id(): #compares nodes id
                return nodes #returns node object
        return None #if statement is false returns None
    def get_ego(self):
        '''
        returns the ego of the EgoNet class
        '''
        return self.__ego #returns the ego of the EgoNet class
    
    def get_circle_names(self):
        '''
        function goes through the keys in the circles dictionary
        appends the keys to a circle name list
        returns the circle name list
        '''
        circle_name = [] #initializes the circle name list
        for key in self.__circles.keys(): #goes through the keys in the circles dictionary
            circle_name.append(key) #appends the keys to the cirlce name list
            
        return circle_name #returns the circle name list

    def get_circle(self, circle_name):
        '''
        circle_name: parameter for circle
        function gets the nodes from the circle dictionary
        returns the list of circle nodes
        '''
        #circle_node = []
        circle_node = self.__circles[circle_name] #gets the ndoes from the circle dictionary
        return circle_node #returns the list of circle nodes
    
    def get_alters(self):
        '''
        returns the set of Node objects the ego is connected to
        '''
        #print(self.__social_network[self.__ego])
        #get the keys from the social network dictionary
        return self.__social_network[self.__ego] #returns the set of Node objects the ego is connected to
    
    def get_alter_node_count(self):
        '''
        returns the alter node count connected to the Ego
        '''
        #print(self.__alter_node_count)
        return self.__alter_node_count #returns the alter node count connected to the Ego

    def get_ego_net_features(self):
        '''
        returns the dictionary of ego net features
        '''
        #print(self.__ego_net_features)
        return self.__ego_net_features #returns the dictionary of ego net features

    def get_ego_net_feature(self, feature):
        '''
        features: parameter for feature
        returns a tuple of feature name and feature id
        '''
        #print(self.__ego_net_features[feature] )
        return self.__ego_net_features[feature] #returns a tuple of feature name and feature id from using the feature parameter

    def get_feature_pos(self, feature_name, feature_id):
        '''
        feature_name: parameter for feature
        feature_id: parameter for feature
        function compares feature name and feature id to other information
        returns the feature position or returns None if statement is false
        '''
        for keys in self.__ego_net_features: #gets keys in features
            value = self.__ego_net_features[keys] #gets value at the specific key
            if value[0] == feature_name and value[1] == feature_id: #compares values to feature name and feature id
                #print(keys)
                return keys #returns the feature position
        return None #returns None if statement is false
    
    def get_alter_connections(self, alter):
        '''
        alter: paramter for node
        returns alter node object is connected to
        '''
        return set(self.__social_network[alter]) #returns alter node object is connected to using the alter parameter
    
    def add_circle(self, circle_name, alters):
        '''
        circle_name: used to call Circle class, name of circle
        alters: list of alters
        function add the circle to the ego's circle
        returns nothing
        '''
#        if not(circle_name in self.__circles.keys()):
#            self.__circles[circle_name] = set(alters)
#        else:
#            for node in alters:
#                self.__circles[circle_name].add(node)
#        if circle_name in self.__circles:
#            self.__circles[circle_name].add(Circle.Circle(circle_name,alters))
#        else:
        self.__circles[circle_name] = Circle.Circle(circle_name,alters) #add the circle to the ego's circle
    
    def add_connection_between_alters(self,alter1,alter2):
        '''
        alter1: parameter for node
        alter2: parameter for node
        function checks whether alter1 is in social network
        if not then creates set
        if already in set the adds value only
        does same thing for alter2
        returns nothing
        '''
        if not(alter1 in self.__social_network): #checks whether alter1 is in social network
            self.__social_network[alter2] = set(alter1) #if not then creates set
        else:
            self.__social_network[alter2].add(alter1) #if already in set the adds value only
        #does same thing for alter2
        if not(alter2 in self.__social_network):
            self.__social_network[alter1] = set(alter2)
        else:
            self.__social_network[alter1].add(alter2)
        


    def add_alter_node(self, alter):
        '''
        alter: parameter for node
        function checks whether alter is in social network
        if not then adds alter to social network and increments alter node count by 1
        returns nothing
        '''
        if not(alter in self.__social_network): #checks whether alter is in social network
            self.__social_network[self.__ego].add(alter) #if not in social network then adds alter to social network
            self.__social_network[alter] = {self.__ego}
            self.__alter_node_count +=1 #increments node count by 1
        
   

    def __eq__(self,other):
        '''True if all attributes are equal.'''
        return (self.__ego == other.__ego)\
            and (self.__social_network == other.__social_network) \
            and (self.__alter_node_count == other.__alter_node_count) \
            and (self.__circles == other.__circles) \
            and (self.__ego_net_features == other.__ego_net_features)
            
    def __str__(self):
        '''Returns a string representation for printing.'''
        st = f"Ego: {self.__ego}\n"
        st+= f"Social Network: {self.__social_network}\n"
        st+= f"Circles: {self.__circles}"
        return st

    __repr__ = __str__