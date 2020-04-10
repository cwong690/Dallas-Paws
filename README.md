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

<img src="Dallas-Paws/img/animal_type_count.png"/>



_The time inside the date column is unnecessary and will only cause trouble later on. It will be stripped._

_In order to exact information such as day, month, and so on, the datetime columns need to be converted to DateTime objects._



_Looked at value counts of many columns to determine which ones are necessary._
_Every column seems to have minimal amounts of missing values except for the 'reason' column. We will check the values within that column and see if it is important._


_Most of the reasons are similar but different and very specific. It will not be too useful for this hypothesis since we are looking at simply the intake condition and the general intake type. Checking out the value counts, they are also mainly in the 'other' category will small amounts in the other categories. We can safely drop the 'reason' column entirely._

_The rest of the columns do not contain a huge amount of missing values that would affect the testing. Therefore, we will drop all rows with null values._


_The council district is a bit messy. It has multiple datatypes but are basically the same number. The numbers will have to be changed to integer type and drop the random string value.  
Also, looking at the Dallas district map, there are no districts 0 or 21. Those rows will also be dropped._
