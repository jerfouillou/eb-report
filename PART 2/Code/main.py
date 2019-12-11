# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 13:36:53 2019

@author: jeremy.fouillou
"""
#IMPORT LIBRARIES
from extract_envelope import main_envelope as envelope

server_name = 'http://hkg1902w0057/project/api/'
proposed_id = 3953
baseline_id = 3953

#PART 2
#SECTION 5: 5.1	Input Parameters Summary Table
#Building Envelope
building_envelope_data = envelope(proposed_id, server_name)

#Lighting System Input

#Shower Hot Water System Input

#Equipment Loads Impact

#Indoor Set Points

#Occupancy Density