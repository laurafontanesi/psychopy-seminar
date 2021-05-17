from __future__ import division
from psychopy.visual import ImageStim, TextStim, Window
from psychopy import core, event, gui, data, logging
import numpy as np
import pandas as pd
import os

from routines import Routine

#general settings
expName = 'wpa_6'
screen_size = [800, 600]
frames_per_second = 60
full_screen = False
background_color = '#eeeeee'

# trial settings
choice_keys = ['q', 'p']
escape_key = 'escape'
choice_time_limit = 5
feedback_duration = 2
fixation_duration = 1.5

#stimuli settings
text_color = 'black'
text_height = 50
options_x_offset = 200
image_size = 100

#store info about the experiment session
dlg = gui.Dlg(title=expName)
dlg.addField('Participant:', 1)
dlg.addField('Age:', 25)
dlg.addField('Gender:', choices=['female', 'male', 'prefer not to disclose'])
dlg.addField('Handedness:', choices=['right', 'left', 'both'])
dlg.show()

expInfo = dict(zip(['participant', 'age', 'gender', 'hand'], dlg.data))
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName # add the experiment name
if dlg.OK:  # then the user pressed OK
    print(expInfo)
else:
    print(expInfo)
    core.quit()

#check if data folder exists
directory=os.path.join(os.getcwd(), 'data')
if not os.path.exists(directory):
    os.makedirs(directory)

#create file name for storing data
fileName = os.path.join('data', '%s_%s_%s' % (expName, expInfo['participant'], expInfo['date']))

#save a log file
logFile = logging.LogFile(fileName + '.log', level=logging.DEBUG)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

#create a window
mywin = Window(screen_size, units='pix', color=background_color, fullscr=full_screen)

#create some stimuli
n_trials = 30

A_feedback = TextStim(win=mywin, color=text_color, pos=(-options_x_offset, 0), height=text_height)
B_feedback = TextStim(win=mywin, color=text_color, pos=(options_x_offset, 0), height=text_height)

A_feedback_trials = np.random.binomial(n=1, p=.4, size=n_trials)
B_feedback_trials = np.random.binomial(n=1, p=.6, size=n_trials)

A_picture = ImageStim(win=mywin, 
                      pos=(-options_x_offset, 0), 
                      size=image_size, 
                      image=os.path.join(os.getcwd(), 'stimuli', 'A.png'))

B_picture = ImageStim(win=mywin, 
                      pos=(options_x_offset, 0), 
                      size=image_size, 
                      image=os.path.join(os.getcwd(), 'stimuli', 'B.png'))

fixation_cross = TextStim(win=mywin, text='+', color=text_color)

#create the dataframe
data = pd.DataFrame([])

#draw the stimuli
trial_routine = Routine(window=mywin, frames_per_second=frames_per_second, escape_key=escape_key)

for t in range(n_trials):
    # put here things that change every trial
    A_feedback.text = '%s' % A_feedback_trials[t]
    B_feedback.text = '%s' % B_feedback_trials[t]

    # first event
    trial_routine.wait_for_time_limit(
        components=[fixation_cross], 
        time_seconds=fixation_duration, 
        label='fixation_cross')

    # second event
    key, rt = trial_routine.wait_for_keys_or_time_limit(
        components=[A_picture, B_picture], 
        valid_keys=choice_keys, 
        time_seconds=choice_time_limit, 
        label='choice')
    data = data.append({'rt':rt, 'choice': key, 'trial': t, 'f_A': A_feedback_trials[t],  'f_B': B_feedback_trials[t]}, ignore_index=True) # record the responses
    
    # third event
    trial_routine.wait_for_time_limit(
        components=[A_feedback, B_feedback], 
        time_seconds=feedback_duration, 
        label='feedback')

    #save data to file
    for label in expInfo.keys():
        data[label] = expInfo[label]
    data.to_csv(fileName + '.csv')
    
#cleanup
mywin.close()
core.quit()