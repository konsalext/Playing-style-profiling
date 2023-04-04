USE superleague; --define the daatabase that contains the data
--we have six tables of data , one for each season ,
--first step we combine it all into one big table ,
--using UNION ALL (outer join/all rows) , 
--and naming the table raw_data

CREATE TABLE raw_data AS
SELECT * FROM 5th_season
UNION ALL
SELECT * FROM fourth_season
UNION ALL 
SELECT * FROM third_season
UNION ALL
SELECT * FROM second_season
UNION ALL
SELECT * FROM last_season
UNION ALL
SELECT * FROM twenty_three;

--then we cook our own three home-made metrics :

SELECT Teams,Season,Possession,to_att_3rd,att_3rd_acc,
		PPDA_vs,Pass_rate,through_pass,progr_runs,progr_passes,
		total_passes,long_passes,box_touches,shots_for,xg_for,
		chal_int,PPDA,shots_vs,xg_against,
--final_third_entries (total attempted passes to final third * % accurate) ,
--to give us only the successful entries to final third, 
        to_att_3rd*att_3rd_acc AS final_third_entries,
--finding the % of long pass share ,
		(long_passes/total_passes)*100 AS long_pass_share,
--and how direct/urgent is the team in its intent to progress the ball upfield ,
		(progr_passes/total_passes)*100 AS directness;
--then i export as a csv and i load it with pandas into python
--and i start to build the app script for streamlit !!