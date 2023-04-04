# import libraries
import streamlit as st
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import math
from highlight_text import HighlightText
from mplsoccer import PyPizza , FontManager , Radar , grid

st.set_page_config(layout="wide")

choice_one= "Introduction"
choice_two="Single team profile"
choice_three="Compare two teams"
the_selector=st.sidebar.selectbox("Please select :",[choice_one,choice_two,choice_three])

@st.cache_data
def load_data():
    the_table=pd.read_excel("all_seasons.xlsx")
    return the_table

df= load_data()

linkedin_link="[Connect with me on LinkedIn !] (www.linkedin.com/in/konstantinos-alexiou-40013796)"


st.header("Profiling teams' playing style in the Greek Superleague")

if the_selector==choice_one:
    st.balloons()
    st.balloons()
    col_one,col_two=st.columns(2)
    with col_one :
        st.markdown("_Welcome_ ! Purpose of this app is trying to capture the **playing style** _(as complicated as that is)_ of football clubs\
                            in the Greek Superleague , including those who competed in Greece's top tier the last\
                            six seasons.")
        st.markdown("Getting familiar with the metrics and their definitions on the right is a good place to\
                            start , then you can head over to the **sidebar** on the left and choose whether you want to see a single\
                            team's profile , or you want to compare different clubs.You can even compare **the same**\
                            team across different seasons !")
        st.markdown("The visualizations used are **wheels** for the profiling of a single team and **radar plots** for the comparisons.")
        st.markdown("The scoring method used is **percentile ranks** , simply a score **0-100** for each metric when compared with\
                            all the teams that competed in the Superleague during the last six seasons.")
        st.markdown("- The metrics are grouped in five distinct categories : **Possession** , **Disrupt** _(the team's intent to disrupt\
                    the balance of the defending team)_ , **Finish** and finally **Defending** _(which was broken down further in **Pressing**\
                    and classic defending)._")
        st.markdown("- data is via Wyscout , valid until April 1st 2023 ,")
        st.markdown("- all raw data collected were adjusted per90.")
        st.info("created by Alexiou Konstantinos.I hold a BSc. in Sports Sciences and Physical Education , with my specialization being on\
                        football (soccer) analysis.I also mess with data analysis and soccer datasets.I live in Athens , Greece")
        st.markdown (linkedin_link,unsafe_allow_html=True)

    with col_two:
        st.subheader("Metric definitions :")
        st.markdown("_(some are pretty self-explanatory , like **Possession %** or like **touches in oppo box**)_ :")
        st.markdown("- **% long pass** --> a team's long pass share of total passes")
        st.markdown("- **PPDA vs** --> how much pressure is the team under , when in possession in the first 60% of the pitch.\
                            _(high score = opponents prefer not to press them high = speaks indirectly to the build-up capabilities of said team)_")
        st.markdown("- **pass tempo** --> passes per minute of pure possession _(does a team pursue a high-tempo passing game ?)_")
        st.markdown("- **directness** --> how direct/urgent is the team in progressing the ball through the thirds _(progressive passes/total passes)_")
        st.markdown("- **PPDA** --> passes allowed per defensive action (tackle , clearance , foul , interception) in the final 60% of the pitch\
                            _(shows the team's intent to press high and steal the ball)_")
        st.markdown("- **Challenge intensity** --> How many defensive actions the team has in 100% of the pitch per minute of opponent's ball possession\
                            _(how aggressive is the team's\
                            defending style , do they delay/passively close spaces or do they actively trying to win the ball back ?)_")

if the_selector==choice_two:
    st.subheader("Single team  profiler")
    col_three,col_four=st.columns(2)
    with col_three:
        st.markdown("Choose which team , for which season --> on the right you get the **playstyle wheel** !")
        st.markdown("_If you don't get a wheel it simply means that the team you chose was not in the league the\
                    season you selected , just try another year !_)")
        st.markdown("_(the list has 2 Aris teams (mistake in the app's design , **sorry**) , the first one works only for the 2019 season , while the second\
                    one is for 2019 onwards (Aris was not in Superleague in 2018)._")
        
        the_teams = df["Teams"]
        the_teams=the_teams.to_list()
        the_teams=set(the_teams)
        the_teams=sorted(the_teams)
        team_select=st.selectbox("Select the team you want to see :",the_teams,index=0)
        the_seasons=df["Season"]
        the_seasons=the_seasons.to_list()
        the_seasons=set(the_seasons)
        the_seasons=sorted(the_seasons)
        season_select=st.selectbox("Select which season you want to see :",the_seasons,index=0)
    with col_four :
        parameters=list(df.columns)
        parameters=parameters[3:]
        first_filter=df.loc[df["Teams"]==team_select]
        first_filter=first_filter.reset_index(drop=True)
        second_filter=first_filter[first_filter["Season"]==season_select]
        second_filter=second_filter.values
        get_the_vals=second_filter.tolist()
        get_the_vals=list(get_the_vals)
        get_the_vals=get_the_vals[0][3:]
        the_scores=[]
        for x in range(len(parameters)):
            the_scores.append(math.floor(stats.percentileofscore(df[parameters[x]],get_the_vals[x])))
        the_scores[-2]=100-the_scores[-2]
        the_scores[-1]=100-the_scores[-1]
        the_scores[-4]=100-the_scores[-4]
        metrics=["Possession %","final third\nentries","% long pass","PPDA vs","Pass tempo","Directness",
            "through\npasses","progressive\ncarries","touches in\noppo box","shots for","xG/shot for","PPDA",
            "challenge\nintensity","shots against","xG/shot\nagainst"]

        slice_colors = ["silver"] * 4 + ["dodgerblue"] * 4 + ["lightgreen"] * 3 + ["firebrick"] *2 + ["orange"] * 2
        text_colors = ["#000000"] * 15

        baker = PyPizza(
        params=metrics,                  # list of parameters
        background_color="#222222",     # background color
        straight_line_color="#000000",  # color for straight lines
        straight_line_lw=1,             # linewidth for straight lines
        last_circle_color="#000000",    # color for last line
        last_circle_lw=1,               # linewidth of last circle
        other_circle_lw=0,              # linewidth for other circles
        inner_circle_size=20   )         # size of inner circle

        # plot pizza
        fig, ax = baker.make_pizza(
        the_scores,                          # list of values
        figsize=(8,8),                # adjust the figsize according to your need
        color_blank_space="same",        # use the same color to fill blank space
        slice_colors=slice_colors,       # color for individual slices
        value_colors=text_colors,        # color for the value-text
        value_bck_colors=slice_colors,   # color for the blank spaces
        blank_alpha=0.4,                 # alpha for blank-space colors
        kwargs_slices=dict(
                edgecolor="#000000", zorder=2, linewidth=1
        ),                               # values to be used when plotting slices
        kwargs_params=dict(
                color="#F2F2F2", fontsize=11,
                va="center"
        ),                               # values to be used when adding parameter labels
        kwargs_values=dict(
            color="#F2F2F2", fontsize=11,
            zorder=3,
            bbox=dict(
                edgecolor="#000000", facecolor="cornflowerblue",
                boxstyle="round,pad=0.2", lw=1
            )
        )                                # values to be used when adding parameter-values labels
        )

        # add title
        fig.text(
        0.515, 0.98, f"Playing style profile {team_select} | season {season_select}", size=13,fontweight="bold",
        ha="center", color="#F2F2F2"
        )

        # add subtitle
        fig.text(
        0.515, 0.96,
        "Percentile rank compared to all Superleague teams from the last 5 seasons",fontstyle='italic',
        size=11,
        ha="center", color="#F2F2F2"
        )

         # add credits
        CREDIT_1 = "data via Wyscout"
        CREDIT_2 = "by Alexiou Kon/nos | inspired by TheAthletic playstyle wheels"

        fig.text(
        0.99, 0.02, f"{CREDIT_1}\n{CREDIT_2}", size=10,
        color="#F2F2F2",
        ha="right"
        )

        # add text
        fig.text(
        0.19, 0.93, "Possession      Disrupt           Finish           Pressing         Defence", size=12,
        fontweight="bold",
        color="#F2F2F2"
        )

        # add rectangles
        fig.patches.extend([
        plt.Rectangle(
            (0.16, 0.927), 0.025, 0.021, fill=True, color="silver",
            transform=fig.transFigure, figure=fig
        ),
        plt.Rectangle(
            (0.336, 0.927), 0.025, 0.021, fill=True, color="dodgerblue",
            transform=fig.transFigure, figure=fig
        ),
        plt.Rectangle(
            (0.50, 0.927), 0.025, 0.021, fill=True, color="lightgreen",
            transform=fig.transFigure, figure=fig
        ),
        plt.Rectangle(
            (0.651, 0.927), 0.025, 0.021, fill=True, color="firebrick",
            transform=fig.transFigure, figure=fig
        ),
        plt.Rectangle(
            (0.82, 0.927), 0.025, 0.021, fill=True, color="orange",
            transform=fig.transFigure, figure=fig
        ),
        ])


        # add image
        # ax_image = add_image(
        #     fdj_cropped, fig, left=0.4478, bottom=0.4315, width=0.13, height=0.127
        # )   # these values might differ when you are plotting


        st.pyplot(fig)

if the_selector==choice_three :
    low_end=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    high_end=[100,100,100,100,100,100,100,100,100,100,100,100,100,100,100]
    lower_is_better=[]
    st.subheader ("Comparison between two teams")
    st.markdown("_(Choose teams and seasons , then one of the 3 style areas **Possession\
                -Disrupt and Finish-Defence** .You can even choose the same team across two different seasons to see\
                what's new or changed !)_")
    col_five,col_six=st.columns(2)
    with col_five:
        the_teams = df["Teams"]
        the_teams=the_teams.to_list()
        the_teams=set(the_teams)
        the_teams=sorted(the_teams)
        team_select_first=st.selectbox("Select the first team :",the_teams,index=0)
        the_seasons=df["Season"]
        the_seasons=the_seasons.to_list()
        the_seasons=set(the_seasons)
        the_seasons=sorted(the_seasons)
        season_select_first=st.selectbox("Select the first team's season :",the_seasons,index=0)
        team_select_second=st.selectbox("Now select the team to compare :",the_teams,index=0)
        season_select_second=st.selectbox("And the second team's season:",the_seasons,index=0)
        area_of_comparison=st.selectbox("Which area of playing style you want the comparison to take place in :",["Possession","Disrupt and Finish","Defence"],index=0)
    with col_six :
        parameters=list(df.columns)
        parameters=parameters[3:]
        first_filter_team=df.loc[df["Teams"]==team_select_first]
        first_filter_team=first_filter_team.reset_index(drop=True)
        second_filter_team=first_filter_team[first_filter_team["Season"]==season_select_first]
        second_filter_first=second_filter_team.values
        get_the_vals_first_listed=second_filter_first.tolist()
        values_first_final=get_the_vals_first_listed[0][3:]
#now for the second team
        the_compared_team=df.loc[df["Teams"]==team_select_second]
        the_compared_team=the_compared_team.reset_index(drop=True)
        the_compared_df=the_compared_team[the_compared_team["Season"]==season_select_second]
        third_filter=the_compared_df.values
        compared_team_as_list=third_filter.tolist()
        values_second_final=compared_team_as_list[0][3:]
#now get the percentile scores for both teams
        perc_ranks_first=[]
        for x in range(len(parameters)):
            perc_ranks_first.append(math.floor(stats.percentileofscore(df[parameters[x]],values_first_final[x])))
        perc_ranks_first[-2]=100- perc_ranks_first[-2]
        perc_ranks_first[-1]=100- perc_ranks_first[-1]
        perc_ranks_first[-4]=100- perc_ranks_first[-4]
        perc_ranks_second=[]
        for x in range(len(parameters)):
            perc_ranks_second.append(math.floor(stats.percentileofscore(df[parameters[x]],values_second_final[x])))
        perc_ranks_second[-2]=100- perc_ranks_second[-2]
        perc_ranks_second[-1]=100- perc_ranks_second[-1]
        perc_ranks_second[-4]=100- perc_ranks_second[-4]

#filter by area of playing style
        poss_metrics=parameters[0:5]
        disrupt_and_finish_metrics=parameters[5:11]
        defending_metrics=parameters[11:]
        if area_of_comparison=="Possession" :
            the_metrics_plotted=poss_metrics
            the_first_team_plotted=perc_ranks_first[0:5]
            the_second_team_plotted=perc_ranks_second[0:5]
            low_boundary=low_end[0:5]
            high_boundary=high_end[0:5]
        elif area_of_comparison=="Disrupt and Finish" :
            the_metrics_plotted=disrupt_and_finish_metrics
            the_first_team_plotted=perc_ranks_first[5:11]
            the_second_team_plotted=perc_ranks_second[5:11]
            low_boundary=low_end[5:11]
            high_boundary=high_end[5:11]
        else:
            the_metrics_plotted=defending_metrics
            the_first_team_plotted=perc_ranks_first[11:]
            the_second_team_plotted=perc_ranks_second[11:]
            low_boundary=low_end[11:]
            high_boundary=high_end[11:]
            
            
            
        
            
#time to draw the radar
        radar = Radar(the_metrics_plotted, low_boundary, high_boundary,
              lower_is_better=lower_is_better,
              # whether to round any of the labels to integers instead of decimal places
              round_int=[True]*len(the_metrics_plotted),
              num_rings=4,  # the number of concentric circles (excluding center circle)
              # if the ring_width is more than the center_circle_radius then
              # the center circle radius will be wider than the width of the concentric circles
              ring_width=1, center_circle_radius=1)
# creating the figure using the grid function from mplsoccer:
        fig_second, axs = grid(figheight=14, grid_height=0.915, title_height=0.06, endnote_height=0.025,
                title_space=0, endnote_space=0, grid_key='radar', axis=False)

# plot radar
        radar.setup_axis(ax=axs['radar'])  # format axis as a radar
        rings_inner = radar.draw_circles(ax=axs['radar'], facecolor='oldlace', edgecolor='white')
        radar_output = radar.draw_radar_compare(the_first_team_plotted,the_second_team_plotted, ax=axs['radar'],
                                        kwargs_radar={'facecolor': 'firebrick', 'alpha': 0.35},
                                        kwargs_compare={'facecolor': 'dodgerblue', 'alpha': 0.35})
        radar_poly, radar_poly2, vertices1, vertices2 = radar_output
        range_labels = radar.draw_range_labels(ax=axs['radar'], fontsize=27)
        param_labels = radar.draw_param_labels(ax=axs['radar'], fontsize=27)
        axs['radar'].scatter(vertices1[:, 0], vertices1[:, 1],
                     c='firebrick', edgecolors='white', marker='o', s=195, zorder=2)
        axs['radar'].scatter(vertices2[:, 0], vertices2[:, 1],
                     c='dodgerblue', edgecolors='white', marker='o', s=195, zorder=2)

# adding the endnote and title text (these axes range from 0-1, i.e. 0, 0 is the bottom left)
# Note we are slightly offsetting the text from the edges by 0.01 (1%, e.g. 0.99)
        endnote_text = axs['endnote'].text(0.99, 0.5, 'by Alexiou Kon/nos', fontsize=22, ha='right', va='center')
        title1_text = axs['title'].text(0.01, 0.65, f"{team_select_first}", fontsize=25, color="firebrick",ha='left', va='center')
        title2_text = axs['title'].text(0.01, 0.25,f"season {season_select_first}", fontsize=27,
                                ha='left', va='center', color='firebrick')
        title3_text = axs['title'].text(0.99, 0.65,f"{team_select_second}", fontsize=27,
                                ha='right', va='center', color="dodgerblue")
        title4_text = axs['title'].text(0.99, 0.25,f"season {season_select_second}" , fontsize=27,
                                ha='right', va='center', color='dodgerblue')
        title_five=axs["title"].text(0.49,0.35,f"Compared on {area_of_comparison}",fontsize=27,ha="center",va="center",
                                     color="black",fontstyle="italic")
                                     
        st.pyplot(fig_second)

    
    





    
    
