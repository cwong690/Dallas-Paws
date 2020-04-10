# Dogs or Cats? Why not both?

Data is from 2 separate Dallas Animal Shelter records: one contains data from October 2018-September 2019 and the other from October 2019-March 2020.
This analysis will simply look year 2019, taking all data within 2019 from both datasets into one.  

Data Source: https://www.dallasopendata.com/City-Services/FY-2019-Dallas-Animal-Shelter-Data/kf5k-aswg
             https://www.dallasopendata.com/City-Services/FY2020-Dallas-Animal-Shelter-Data/7h2m-3um5

Dog lovers and cat lovers have been at war since the beginning of time (or whenever dogs and cats were discovered).
I decided to find out if this is true using data from the Dallas Animal Shelter. I want to know if there really is a difference between the amount of cats adopted vs dogs.


## Hypothesis Testing  

This is the question I am trying to answer:  

**Null Hypothesis**: There are no differences between the adoption rate of cats and dogs.
**Alternative Hypothesis**: There are differences between the adoption rate of cats and dogs.

I will calculate the p-value and set the rejection threshold to be the standard: **0.05**

The amount of dogs the shelter takes in is significantly greater than the amount of cats they take in.
After merging and cleaning up the datasets, I ended up with a dataset containing only the fields that will be important for finding the answer to my question.
This includes: animal_type, intake_type, intake_datetime, outcome_type, outcome_datetime.

Ultimately, I will be looking at the adoptions of cats and dogs per month relative to how many cats and dogs they take in each month.

Animal Count:
First I will examine how many total dogs and cats have been taken in by the shelter in 2019.

<img src="/img/animal_type_count.png"/>

From the bar graph, it is clear that there are definitely more dogs that are make it to the shelters.
Next I got plotted the intake count and the percentage of cats and dogs per month to see if there are certain months that have a higher intake count.

<img src="/img/count_perc_monthly.png"/>

Looking at just the count is a bit tougher to distinguish the differences in cats and dogs because of the high volume of dogs. Therefore, I also plotted the percentages of the intake per month. Looking at the percentages, it is clearer that there seems to be a higher intake of cats during the summer months (May-September) and a higher intake of dogs during winter/spring months.

A line plot is also plotted for additional visual.

<img src="/img/lineplt_count_perc_monthly.png"/>

Next, 

<img src="/img/count_intake_type.png"/>

<img src="/img/catplot_intake_type_monthly.png"/>

Outcome

<img src="/img/count_outcome_type.png"/>

<img src="/img/catplot_outcome_type_monthly.png"/>

adopt monthly

<img src="/img/lineplt_adpt_count_monthly.png"/>

<img src="/img/lineplt_adpt_perc_monthly.png"/>

<img src="/img/bar_perc_month_adopted.png"/>

pval

<img src="/img/pval.png"/>
