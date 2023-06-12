from patsy import dmatrices
#import Flashes_function as fl
import pandas as pd
import statsmodels.api as sm
#GLM on StimSide(col 3), response(col 6) filter out the 2's,
import os
from csv import writer, reader
import pickle
directory = '../Urop Analysis/accumulation_parsed/9812_3_parsed/'
directory_seq = '../Urop Analysis/accumulation_parsed/9812_3_parsed_seq/'
data={}
win_stay=[]
lose_switch=[]
win_stay_lose_switch=[]
flashes_correct=[]
choice_bool=[]
persistance=[]


data['flashes_correct']=flashes_correct
data['choice_bool']=choice_bool #only 1 and 0
data['win_stay_lose_switch']=win_stay_lose_switch
data['win_stay']=win_stay
data['lose_switch']=lose_switch
data['persistance'] = persistance
cat=[]

for i in range(18):
    if i==2:
        cat.append('side')
    elif i==5:
        cat.append('correct')
    else:
        cat.append('')
for filename in os.listdir(directory):
    #print(filename)
    #if '67' not in filename and '69' not in filename: 
     #   continue
    #if '1200' not in filename:
     #   continue
    if filename=='.DS_Store':
        continue
    f=os.path.join(directory,filename) #commented portion below used for csv manipualtion
    #with open(f,'r') as f_object:
     #   rd=reader(f_object)
      #  lines = list(rd)
       # del lines[0:2]
       # updated = False
        #for row in rd:
         #   if row[2]=='side':
          #      updated=True
           # break
       # if updated is False:
        #    lines.insert(0,cat)
   #with open(f,'w',newline='') as writeFile:
    #    wt = writer(writeFile)
     #   wt.writerows(lines)
    #f_object.close()
    #writeFile.close()
    trials=pd.read_csv(f)
    s = os.path.join(directory_seq,filename[:-4]+'sequence'+'.csv')
    sequences = pd.read_csv(s)
    #print(trials)


#print(data)
#df=pd.DataFrame('7481_7_FULLTASK_48_850R_01262022.csv')
    correctness=trials['correct'].tolist() # 0-incorrect 1-correct 2-miss
    stim_side= trials['side'].tolist() # 0-left 1-right
    trial_list=[] # format: (correct or incorrect,left or right)
    sequence_list = [] # a list of the value of sequences for a given trail
    SIDE=1
    CORRECT=0
    sequence_index = 0
    for trial in zip(correctness,stim_side):
        if (trial[SIDE]!=1 and trial[SIDE]!=0) and (trial[CORRECT]!=0 and trial[CORRECT]!=1):
            continue
        elif trial[SIDE]==2:
            continue
        else:
            trial_list.append(trial)
            current_seq = sequences.iloc[sequence_index]
            seq_val = 0
            for val in current_seq:
                seq_val+=val
            sequence_list.append(seq_val)
        sequence_index+=1
    index=0
    OUTCOME=0
    DIRECTION=1
    #print(trial_list)
    right_correct=0
    right_total=0
    left_correct=0
    left_total=0
    maximum_difference_z=.4
    current_win_stay_lose_switch=[]
    current_win_stay=[]
    current_lose_switch=[]
    current_persistance=[]
    current_choice_bool=[]
    current_flashes_correct=[]


    for index,trial in enumerate(trial_list):# scans valid trials for stratgies
        if index==0:
            index+=1
            current_win_stay_lose_switch.append(0)
            current_win_stay.append(0)
            current_lose_switch.append(0)
            current_persistance.append(0)
            continue
        else:
            prev_trial=trial_list[index-1]
            if prev_trial[OUTCOME]==1:
                if prev_trial[DIRECTION]==1:
                    current_win_stay_lose_switch.append(1)
                    current_win_stay.append(1)
                    current_lose_switch.append(0)
                    current_persistance.append(1)
                    right_total+=1
                    right_correct+=1
                else:
                    current_win_stay_lose_switch.append(-1)
                    current_win_stay.append(-1)
                    current_lose_switch.append(0)
                    current_persistance.append(-1)
                    left_correct+=1
                    left_total+=1
            if prev_trial[OUTCOME]==0:
                if prev_trial[DIRECTION]==1:
                    current_win_stay_lose_switch.append(-1)
                    current_win_stay.append(0)
                    current_lose_switch.append(-1)
                    current_persistance.append(1)
                    right_total+=1
                else:
                    current_win_stay_lose_switch.append(1)
                    current_win_stay.append(0)
                    current_lose_switch.append(1)
                    current_persistance.append(-1)
                    left_total+=1
    print(len(trial_list))
    print(len(sequence_list))
    seq_index = 0
    for correct_or_not,side in trial_list:  #choice_bool is the final decision of the mice and flashes_correct is the correct_side
        if (side==1 and correct_or_not==1) or (side==0 and correct_or_not==0):
            current_choice_bool.append(1)
            if side==1:
                current_flashes_correct.append(sequence_list[seq_index])
            elif side==0:
                current_flashes_correct.append(sequence_list[seq_index])
        elif(side==1 and correct_or_not==0) or(side==0 and correct_or_not==1):
            current_choice_bool.append(0)
            if side==1:
                current_flashes_correct.append(sequence_list[seq_index])
            elif side==0:
                current_flashes_correct.append(sequence_list[seq_index])
        seq_index+=1
    try:
        p_right=float(right_correct/right_total)
        p_left=float(left_correct/left_total)
        diff1 = float(abs(p_right-p_left)/p_right)
        diff2 = float(abs(p_right-p_left)/p_left)
    except:
        continue
    #print(current_flashes_correct)
    if diff1<maximum_difference_z and diff2<maximum_difference_z:
        print(filename)
        win_stay_lose_switch.extend(current_win_stay_lose_switch)
        win_stay.extend(current_win_stay)
        lose_switch.extend(current_lose_switch)
        flashes_correct.extend(current_flashes_correct)
        choice_bool.extend(current_choice_bool)
        persistance.extend(current_persistance)
    

    




count=0
for i in range(len(flashes_correct)):
    if flashes_correct[i]!=choice_bool[i]:
        count+=1
#print(count)
#print(len(win_stay_lose_switch))
#print(len(flashes_correct))
#print(len(choice_bool))
#print(choice_bool)
df=pd.DataFrame(data)
#print(df)
Y1,X1 = dmatrices('choice_bool ~  flashes_correct+win_stay+lose_switch+persistance',df, return_type='dataframe')
#Y1,X1 = dmatrices('choice_bool ~  flashes_correct+win_stay + lose_switch',df, return_type='dataframe')

mod1=sm.GLM(Y1,X1,family=sm.families.Binomial())
res = mod1.fit()
summary=res.summary()
res.save('results.pickle')
x= (pd.read_pickle('results.pickle'))
print(x.summary())
#print(summary)









