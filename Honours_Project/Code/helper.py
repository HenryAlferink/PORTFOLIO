import numpy as np

class data:
    def __init__(self, x_lo, x_hi, num_data_points, design, t, m_true, m_prior, data_std, C_prior, domain=(0,300), additional_x=None):
        # MEASURING LOCATIONS (x-values)
        self.X_initial = np.linspace(            
            x_lo, x_hi, num_data_points)         # initial set of measurement locations 
        if additional_x is not None:
            self.X_initial = np.append(self.X_initial, additional_x) # for plotting purposes
        self.X_plot = np.linspace(*domain, 300)  # fuller set for plotting purposes (could also be called the "domain")
        self.X_unsorted = self.X_initial.copy()           # full set of locations (sorted) that actually gets processed
        self.m = len(self.X_initial)   
        self.n = len(t)

        # CONCENTRATION DATA FOR CURRENT X (these will change as data points are added)
        self.d_true = design(self.X_initial, t) @ m_true 
        self.d_unsorted = self.d_true + np.random.normal(0, data_std, self.m)
        # sort:
        idxxx = np.argsort(self.X_unsorted)
        self.X = self.X_unsorted[idxxx]
        self.d = self.d_unsorted[idxxx]

        # CONCENTRATION DATA FOR X_initial (constant)
        self.d_initial_true = self.d_true.copy()        
        self.d_initial = self.d.copy()
        # for plotting true data:
        self.d_plot = design(self.X_plot, t) @ m_true 

        # COVARIANCE MATRICES
        self.C_prior = C_prior
        self.C_data = data_std**2 * np.eye(self.m)

        # FORWARD OPERATOR
        self.design = design                    # function to create forward operator
        self.G = self.design(self.X, t)         # forward operator corresponding to current X

        # POSTERIOR
        if C_prior is not None: # this if statement (and one below are just so the first notebook can keep running...)
            self.m_map, self.C_map = self.__evaluate_posterior_initial(self.G, self.d, self.C_data, C_prior, m_prior)

        # POTENTIAL NEW MEASUREMENT LOCATIONS
        self.additional = []                    # x-values         
        self.additional_d_true = []             # corresponding true concentration data
        self.additional_d = []                  # corresponding noisy concentration data
        curr_idx = None                         # current index of set added to full location data X

        # UNCERTAINTY OBJECTIVE VALUES 
        # (corresponding to new measurement locations)
        self.A_optimality = []
        self.D_optimality = []
        self.A_optimality_nocost = []
        self.D_optimality_nocost = []
        # objective values for initial measurement locations:
        if C_prior is not None:
            self.A_optimality_initial = self.__A_optimality(self.C_map)
            self.D_optimality_initial = self.__D_optimality(self.C_map)
        
        # COST FOR EACH OF THE ADDITIOINAL DATAPOINTS (this will be a vector)
        self.c = None

        # TOTAL OBJECTIVE VALUE FOR CURRENT MEASUREMENT SET 
        self.c_total_A = None # for A-optimality
        self.c_total_D = None # for D-optimality
        
        # OTHER PROBLEM SETTINGS/PARAMETERS
        self.domain = domain
        self.t = t
        self.m_true = m_true
        self.m_prior = m_prior
        self.data_std = data_std    
        
        
    def add_points(self, x):
        """ Add point or set of points to self.additional lists.
            Note: x must either be an array of values, or a list containing a value(s).
        """
        assert type(x)!=float and type(x)!=int, " x must either be an array of values, or a list containing a value(s)."

        x = np.array(x)
        self.additional.append(x)
        # evaluate corresponding noisy concentration data:
        self.additional_d_true.append(
            self.design(x, self.t) @ self.m_true
        )
        self.additional_d.append(
            self.additional_d_true[-1] + np.random.normal(0, self.data_std, len(x))
        )
        

    def clear_additional(self):
        self.additional = []
        self.additional_d = []
        self.A_optimality = []
        self.D_optimality = []
    

    def choose_points(self, idx):
        """ Add points in self.additional at specified index to full data. This method useful for plotting."""
        
        if idx is None:
            return

        self.X = np.append(self.X_initial, self.additional[idx])
        self.d_true = np.append(self.d_initial_true, self.additional_d_true[idx])
        self.d = np.append(self.d_initial, self.additional_d[idx])
        
        idxx = np.argsort(self.X)
        self.X = self.X[idxx]
        self.d_true = self.d_true[idxx]
        self.d = self.d[idxx]
        
        self.m = len(self.X)
        self.curr_idx = idx
        self.G = self.design(self.X, self.t)


    def evaluate_cost(self, P, infeasible):
        """ This function evaluates the cost for each measurement location and stores it in the vector self.c
            P is the cost function. 
        """
        self.__check_for_error()

        new_x = np.array(self.additional).flatten()
        self.c = P(new_x, infeasible)

    
    def __evaluate_posterior_initial(self, G, d, C_data, C_prior, m_prior):
        A = np.concatenate(
            [np.linalg.inv(np.linalg.cholesky(C_data)) @ G,
            np.linalg.inv(np.linalg.cholesky(C_prior))])

        b = np.concatenate(
            [np.linalg.inv(np.linalg.cholesky(C_data)) @ d,
            np.linalg.inv(np.linalg.cholesky(C_prior)) @ m_prior])

        m_map = np.linalg.inv(A.T @ A) @ A.T @ b
        C_map = np.linalg.inv(G.T @ np.linalg.inv(C_data) @ G + np.linalg.inv(C_prior))
        
        return m_map, C_map

    
    def evaluate_objective(self):
        """ Evaluate uncertainty objective for current set of measurements. """
        self.__check_for_error()
        for i in range(len(self.additional)):
            C_map_new = self.__update_posterior(self.additional[i])
            self.A_optimality_nocost.append(self.__A_optimality(C_map_new))
            self.D_optimality_nocost.append(self.__D_optimality(C_map_new))
            self.A_optimality.append(self.__A_optimality(C_map_new) + self.c[i])
            self.D_optimality.append(self.__D_optimality(C_map_new) + self.c[i])
            

    def __update_posterior(self, x):
        """ Update posterior (m_map, C_map) after adding one datapoint, x."""
        g = self.design(x, self.t)
        return self.C_map - (self.C_map @ g.T @ g @ self.C_map) / (self.data_std**2 + g @ self.C_map @ g.T)


    def __A_optimality(self, C):
        return np.trace(C) / self.n


    def __D_optimality(self, C):
        # return np.linalg.det(C)
        # return -np.sum(np.log(np.linalg.eigvalsh(C)))
        return np.sum(np.log(np.linalg.eigvalsh(C))) + 800


    def __check_for_error(self):
        for item in self.additional:
            if item.size > 1:
                raise TypeError("If wanting to evaluate cost, new measurements must come in singles only.")
 
        
    def __len__(self): 
        """ Return number of locations in full set."""
        return len(self.X)