# -- Imports ------------------------------------------------------------------
import numpy as np
import math


# -- Main class ---------------------------------------------------------------
class ConcreteSlab:
    def __init__(self, length, f_c, f_y, live_load, dead_load=0, concrete_wt=0.150, bar=6):
        """ Initializes the class named 'Slab' with the span length (ft),
        compressive strength of the conrete (psi), grade of steel reinforcement
        (psi), live load (psf), dead load (psf) aside from the self
        weight of the slab if there is any, the concrete weight (ksf) if it
        is not equal to 0.150 ksf, and the assumed bar type (#6 by default).
        Note that all calculations are done with a 12 in strip of slab as per
        ACI specifications.
        """
        self.length = length
        self.f_c = f_c
        self.f_y = f_y
        self.live_load = live_load
        self.dead_load = dead_load
        self.concrete_wt = concrete_wt
        self.bar = bar

        self.b = 12

        self.h = 0
        self.d = 0

    def __str__(self):
        """ String representation
        """
        return str('This program helps with the design of a concrete slab by performing many tedious calculations and guiding the user to the correct reference tables.')
        # Without the "unindentation", the string resulted in strange and
        # unwanted indentation

    def table_idx(self):
        """ Directs the user to the correct table to find values of rho based
        on the fc and fy inputted.
        """
        array = np.array(
            [
             [3000, 40000, 'Table A-7'],
             [3000, 60000, 'Table A-8'],
             [4000, 40000, 'Table A-9'],
             [4000, 60000, 'Table A-10'],
             [5000, 60000, 'Table A-11']
            ], dtype=object)

        row = array[(array[:,0] == self.f_c) & (array[:,1] == self.f_y)]

        if not row.size > 0:
            raise ValueError('There are no tables available for the combination of fy and fc inputted.')
        else:
            return row[0,2]

    def h_min(self):
        """ Returns the minimum depth of the slab in inches from the span
        length as per ACI requirements.
        """
        return math.ceil(self.length*12/20)
        # h_min is rounded up to the nearest inch to be conservative

    def self_weight(self, h):
        """ Returns the weight of the slab in psf from the depth and concrete
        weight.
        """
        return h*self.b/144 * self.concrete_wt*1000

    def factored_weight(self, sw):
        """ Returns the factored weight in kips per feet from the live load and
        dead load (including the self-weight of the slab).
        """
        return (1.2*(self.dead_load + sw) + 1.6*self.live_load) / 1000
        # LRFD: 1.2*D + 1.6*L

    def factored_moment(self, w_u):
        """ Returns the factored moment in kip-ft from the factored weight and
        span length.
        """
        return w_u * self.length**2 / 8

    def effective_depth(self, h):
        """ Returns the effective depth in inches from the depth and bar type.
        """
        return round(h - 3/4 - 1/2*(self.bar/8), 2)
        # d is rounded to 2 decimal points

    def k_required(self, h=None, phi=0.90):
        """ Prints the required k in ksi and the table that should be used to
        find rho.
        If there is no depth (inches) specified, calculations will be made
        based on the minimum depth as per ACI requirements.
        phi is assumed to be 0.90 unless specified otherwise.
        """

        if h == None:
            self.h = self.h_min()
        else:
            self.h = math.ceil(h)
        # Rounds the user inputted self.h to the higher integer as per ACI
        # specificationsin in case the user did not give an integer value.

        table = self.table_idx()
        sw = self.self_weight(self.h)
        w_u = self.factored_weight(sw)
        m_u = self.factored_moment(w_u)
        self.d = self.effective_depth(self.h)

        k = (m_u * 12) / (phi * self.b * (self.d**2))

        print('Depth h={} in'.format(self.h))
        print('Find rho using {} with k={} ksi'.format(table, round(k, 4)))
        print('Remember to check if the assumed phi of 0.90 can be used')
        # k is rounded to four decimal points

    def as_required(self, rho):
        """ Returns the required area of steel in in/ft^2.
        """
        return round(rho*self.b*self.d, 2)
        # A_s required is rounded to two decimal places

    def as_min(self):
        """ Returns the minimum area of steel in in/ft^2.
        """
        return round(0.0018*self.b*self.h, 2)
        # A_s minimum is rounded to two decimal places

    def main_steel(self, rho):
        """ Prints the area of main steel and the table that should be used.
        """
        a_s = max(self.as_required(rho), self.as_min())
        print('Find the main steel bar type and bar spacing needed using Table A-4 with A_s={} in^2'.format(round(a_s, 2)))

    def main_steel_spacing(self, oc):
        """ Checks whether the spacing of the main steel will be adequate,
        given the main steel's bar spacing in inches from Table A-4.
        """
        h3 = 3*self.h

        if h3 > oc:
            print('3h={} > {}: The bar spacing for the main steel is adequate.'.format(h3, oc))
        else:
            raise ValueError('3h={} < {}: The bar spacing for the main steel is inadequate.'.format(h3, oc))

    def new_effective_depth(self, bar_number):
        """ Prints the new effective depth, given the bar number.
        """
        d = self.h - 3/4 - 1/2*(bar_number/8)
        return print('Effective depth d={}'.format(round(d, 2)))
        # This is a separate function to reduce confusion for the user and to
        # ensure that the original assumptions are not accidentally changed

    def st_steel(self):
        """ Prints the area of shrinkage and temperature (longitudinal steel)
        and the table that should be used.
        """
        if self.f_y == 60000:
            a_s = self.as_min()
            print('Find the shrinkage and temperature steel bar type and bar spacing needed using Table A-4 with A_s={} in^2'.format(round(a_s, 2)))
        elif self.f_y == 40000 or self.f_y == 50000:
            a_s = 0.0020*self.b*self.h
            print('Find the shrinkage and temperature steel bar type and bar spacing needed using Table A-4 with A_s={} in^2'.format(round(a_s, 2)))
        else:
            raise ValueError('Steel grade used is not specified by the ACI code')

    def st_steel_spacing(self, oc):
        """ Checks whether the spacing of the shrinkage and temperature steel
        will be adequate, given the shrinkage and temperature steel's bar
        spacing in inches from Table A-4.
        """
        h5 = 5*self.h

        if h5 > oc:
            print('5h={} > {}: The bar spacing for the shrinkage and temperature steel is adequate.'.format(h5, oc))
        else:
            raise ValueError('5h={} < {}: The bar spacing for the shrinkage and temperature steel is inadequate.'.format(h5, oc))
