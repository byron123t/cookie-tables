import squarify
import plotly
import plotly.express as px
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.sankey import Sankey


fig = plt.figure(figsize=(8, 12))
ax = fig.add_subplot(1, 1, 1, xticks=[], yticks=[],
                     title="Detected Sites with Cookie Consent Violations")
learners = [54323, 4755, 4450, 4281]
labels = ["Successfully visited", "Detected cookie settings",
         "Consent violation", "Personal information"]
colors = ["#FF8000", "#FFBF00", "#FFFF00", "#FFFFF0"]

sankey = Sankey(ax=ax, scale=1.0 / 4000, offset=0.3, head_angle=150)
for input_learner, output_learner, label, prior, color in zip(learners[:-1], learners[1:], 
                                                              labels, [None, 0, 1, 2, 3],
                                                             colors):
    if label == "Successfully Visited":
        quit_label = 'No cookie settings detected'
    elif label == "Detected cookie settings":
        quit_label = 'No violation'
    elif label == "Consent violation":
        quit_label = 'No personal information'
    else:
        quit_label = 'No cookie settings detected'
        
    if prior != 3:
        sankey.add(flows=[input_learner, -output_learner, output_learner - input_learner],
               orientations=[0, 0, 1],
               patchlabel=label,
               labels=['', None, quit_label],
              prior=prior,
              connect=(1, 0),
               pathlengths=[0, 0, 2],
              trunklength=10.,
              rotation=-90,
                  facecolor=color)
    else:
        sankey.add(flows=[input_learner, -output_learner, output_learner - input_learner],
               orientations=[0, 0, 1],
               patchlabel=label,
               labels=['', labels[-1], quit_label],
              prior=prior,
              connect=(1, 0),
               pathlengths=[0, 0, 10],
              trunklength=10.,
              rotation=-90,
                  facecolor=color)
diagrams = sankey.finish()
for diagram in diagrams:
    diagram.text.set_fontweight('bold')
    diagram.text.set_fontsize('10')
    for text in diagram.texts:
        text.set_fontsize('10')
ylim = plt.ylim()
plt.ylim(ylim[0]*1.05, ylim[1])


ax.set_title('Simple Sankey diagram')
plt.savefig('plots/sankey.pdf')


df = {'Website Count':[3936, 4213, 3971, 4016, 4406, 4097, 195, 213, 194, 474, 323, 462],
      'Region': ['Germany', 'California', 'United Kingdom', 'Germany', 'California', 'United Kingdom', 'Germany', 'California', 'United Kingdom', 'Germany', 'California', 'United Kingdom'],
      'Violation Type': ['Rejected Cookie Usage', 'Rejected Cookie Usage', 'Rejected Cookie Usage', 'Cookie Consent Omission', 'Cookie Consent Omission', 'Cookie Consent Omission', 'Ambiguous Consent', 'Ambiguous Consent', 'Ambiguous Consent', 'Complies', 'Complies', 'Complies'],
      'Severity': [0.9, 0.8, 0.9, 1.0, 0.9, 1.0, 0.7, 0.6, 0.7, 0, 0, 0]}

colors = px.colors.diverging.RdYlGn_r
colors.pop()
colors.pop(len(colors) - 1)
# colors = px.colors.diverging.Temps

fig = px.treemap(pd.DataFrame(df), path=[px.Constant('All'), 'Region', 'Violation Type'], values='Website Count', color='Severity', color_continuous_scale=colors, color_continuous_midpoint=0.5, hover_data=['Region', 'Violation Type'])
fig.update_traces(root_color="lightgrey", textinfo="label+value+percent root")
fig.update_layout(margin = dict(t=50, l=25, r=25, b=25), font=dict(size=20))

plotly.offline.plot(fig, filename='plots/treemap.html')

exit()



perc = [0.6604073838319542, 0.6644803041031566, 0.6603978817804494, 0.5805778340603162, 0.611650380724347, 0.5769768027662644, 0.7, 0.6950904392764858, 0.7024128686327078, 0.6525508921839658, 0.643968199101279, 0.6506782945736435]

info_perc = {'California': {'IP Address': 0.03933506044905009, 'Location': 0.026489637305699483, 'Tracker': 0.9090997409326425, 'Demographic': 0.025075561312607946}, 'Germany': {'IP Address': 0.04037468375603739, 'Location': 0.033161185104648, 'Tracker': 0.8989482928053192, 'Demographic': 0.027515838333995443}, 'United Kingdom': {'IP Address': 0.039357909703476274, 'Location': 0.034062107193636795, 'Tracker': 0.9033361495188444, 'Demographic': 0.02324383358404253}}
df = {'values':[34604, 53739, 34981, 42917, 93249, 43878, 350, 387, 373, 24211, 29333, 25009],
      'region': ['Germany', 'California', 'United Kingdom', 'Germany', 'California', 'United Kingdom', 'Germany', 'California', 'United Kingdom', 'Germany', 'California', 'United Kingdom'],
      'cookie_violation_type': ['Rejected Cookie Usage', 'Rejected Cookie Usage', 'Rejected Cookie Usage', 'Cookie Consent Omission', 'Cookie Consent Omission', 'Cookie Consent Omission', 'Ambiguous Consent', 'Ambiguous Consent', 'Ambiguous Consent', 'Complies', 'Complies', 'Complies']}
df_data = {'Cookie Count': [], 'Region': [], 'Violation Type': [], 'Personal Info': [], 'Severity': []}
count = 0
for val, region, violation in zip(df['values'], df['region'], df['cookie_violation_type']):
    contains = perc[count] * val
    no_contains = val - contains
    count += 1
    for key, value in info_perc[region].items():
        df_data['Cookie Count'].append(int(value * contains))
        df_data['Personal Info'].append(key)
        df_data['Violation Type'].append(violation)
        df_data['Region'].append(region)
        if region == 'California':
            if violation == 'Complies':
                df_data['Severity'].append(0)
            elif violation == 'Ambiguous Consent':
                df_data['Severity'].append(0.6)
            elif violation == 'Cookie Consent Omission':
                df_data['Severity'].append(0.9)
            elif violation == 'Rejected Cookie Usage':
                df_data['Severity'].append(0.8)
        else:
            if violation == 'Complies':
                df_data['Severity'].append(0)
            elif violation == 'Ambiguous Consent':
                df_data['Severity'].append(0.7)
            elif violation == 'Cookie Consent Omission':
                df_data['Severity'].append(1.0)
            elif violation == 'Rejected Cookie Usage':
                df_data['Severity'].append(0.9)
    df_data['Cookie Count'].append(int(no_contains))
    df_data['Personal Info'].append('None')
    df_data['Violation Type'].append(violation)
    df_data['Region'].append(region)
    if region == 'California':
        if violation == 'Complies':
            df_data['Severity'].append(0)
        elif violation == 'Ambiguous Consent':
            df_data['Severity'].append(0.2)
        elif violation == 'Cookie Consent Omission':
            df_data['Severity'].append(0.4)
        elif violation == 'Rejected Cookie Usage':
            df_data['Severity'].append(0.3)
    else:
        if violation == 'Complies':
            df_data['Severity'].append(0)
        elif violation == 'Ambiguous Consent':
            df_data['Severity'].append(0.3)
        elif violation == 'Cookie Consent Omission':
            df_data['Severity'].append(0.5)
        elif violation == 'Rejected Cookie Usage':
            df_data['Severity'].append(0.4)

colors = px.colors.diverging.RdYlGn_r
colors.pop()
colors.pop(len(colors) - 1)
# colors = px.colors.diverging.Temps

fig = px.treemap(pd.DataFrame(df_data), path=[px.Constant('All'), 'Region', 'Violation Type', 'Personal Info'], values='Cookie Count', color='Severity', color_continuous_scale=colors, color_continuous_midpoint=0.5, hover_data=['Region', 'Violation Type', 'Personal Info'])
fig.update_traces(root_color="lightgrey", textinfo="label+value+percent root")
fig.update_layout(margin = dict(t=50, l=25, r=25, b=25), font=dict(size=16))

plotly.offline.plot(fig, filename='plots/treemap.html')
