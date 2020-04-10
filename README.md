# Dallas-Paws


# Dallas Animal Shelter 2019

Data is from 2 separate Dallas Animal Shelter records: one contains data from October 2018-September 2019 and the other from October 2019-March 2020.

This analysis will simply look year 2019, taking all data within 2019 from both datasets into one.

## Hypothesis Testing  

**Null Hypothesis**: There are no differences between the adoption percentage of cats and dogs.

**Alternative Hypothesis**: Cats are more likely to be adopted than dogs.


## Load in data


```python
import numpy as np
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

pd.set_option('display.max_columns', 100)
pd.set_option('display.max_rows', 50)

plt.style.use('ggplot')

%matplotlib inline

# description of fields: https://www.dallasopendata.com/City-Services/Animals-Inventory/qgg6-h4bd
# https://gis.dallascityhall.com/documents/StaticMaps/Council/2013_Council_PDFs/2013_CouncilDistrictAllA.pdf
```


```python
fy_2020 = pd.read_csv('FY2020_Dallas_Animal_Shelter_Data.csv', low_memory=False)
fy_2019 = pd.read_csv('FY_2019_Dallas_Animal_Shelter_Data.csv', low_memory=False)
```

_Check months to make sure it has all of 2019 months that are missing in the 2020 dataset._


```python
fy_2020['Month'].value_counts()
```




    OCT.2019    3998
    JAN.2020    3658
    NOV.2019    3526
    DEC.2019    3363
    FEB.2020    3127
    MAR.2020    2575
    Name: Month, dtype: int64




```python
fy_2019['Month'].value_counts()
```




    JUN.2019    4953
    MAY.2019    4658
    JUL.2019    4539
    AUG.2019    4239
    SEP.2019    3928
    JAN.2019    3843
    APR.2019    3759
    MAR.2019    3681
    DEC.2018    3523
    OCT.2018    3219
    FEB.2019    3093
    NOV.2018    2974
    Name: Month, dtype: int64




```python
print(fy_2020.shape)
print(fy_2019.shape)
```

    (20247, 34)
    (46409, 34)


_Checking to make sure the column names match so they can be merged correctly._


```python
print('FY2020 Column Names: ', fy_2020.columns)
print('FY2019 Column Names: ', fy_2019.columns)
```

    FY2020 Column Names:  Index(['Animal Id', 'Animal Type', 'Animal Breed', 'Kennel Number',
           'Kennel Status', 'Tag Type', 'Activity Number', 'Activity Sequence',
           'Source Id', 'Census Tract', 'Council District', 'Intake Type',
           'Intake Subtype', 'Intake Total', 'Reason', 'Staff Id', 'Intake Date',
           'Intake Time', 'Due Out', 'Intake Condition', 'Hold Request',
           'Outcome Type', 'Outcome Subtype', 'Outcome Date', 'Outcome Time',
           'Receipt Number', 'Impound Number', 'Service Request Number',
           'Outcome Condition', 'Chip Status', 'Animal Origin',
           'Additional Information', 'Month', 'Year'],
          dtype='object')
    FY2019 Column Names:  Index(['Animal_Id', 'Animal_Type', 'Animal_Breed', 'Kennel_Number',
           'Kennel_Status', 'Tag_Type', 'Activity_Number', 'Activity_Sequence',
           'Source_Id', 'Census_Tract', 'Council_District', 'Intake_Type',
           'Intake_Subtype', 'Intake_Total', 'Reason', 'Staff_Id', 'Intake_Date',
           'Intake_Time', 'Due_Out', 'Intake_Condition', 'Hold_Request',
           'Outcome_Type', 'Outcome_Subtype', 'Outcome_Date', 'Outcome_Time',
           'Receipt_Number', 'Impound_Number', 'Service_Request_Number',
           'Outcome_Condition', 'Chip_Status', 'Animal_Origin',
           'Additional_Information', 'Month', 'Year'],
          dtype='object')


_It looks like 2019 dataset columns have an underscore instead spaces. Let's change it all to the standard python snake case with underscore as spaces._


```python
fy_2020.columns = fy_2020.columns.str.strip().str.lower().str.replace(' ', '_')
fy_2019.columns = fy_2019.columns.str.strip().str.lower()
```

## Time and Date

_Checking the date and time columns to make sure the formats are similar because it will need to be combined later on._


```python
fy_2020[['intake_date', 'intake_time', 'outcome_date', 'outcome_time']].head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>intake_date</th>
      <th>intake_time</th>
      <th>outcome_date</th>
      <th>outcome_time</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>11/8/19</td>
      <td>15:48:00</td>
      <td>11/9/19</td>
      <td>11:31:00</td>
    </tr>
    <tr>
      <th>1</th>
      <td>11/10/19</td>
      <td>14:18:00</td>
      <td>11/10/19</td>
      <td>0:00:00</td>
    </tr>
    <tr>
      <th>2</th>
      <td>10/3/19</td>
      <td>11:08:00</td>
      <td>10/3/19</td>
      <td>13:36:00</td>
    </tr>
    <tr>
      <th>3</th>
      <td>10/11/19</td>
      <td>9:55:00</td>
      <td>10/15/19</td>
      <td>17:35:00</td>
    </tr>
    <tr>
      <th>4</th>
      <td>11/8/19</td>
      <td>11:55:00</td>
      <td>11/9/19</td>
      <td>12:57:00</td>
    </tr>
  </tbody>
</table>
</div>



_The 2020 date and time column looks good._


```python
fy_2019[['intake_date', 'intake_time', 'outcome_date', 'outcome_time']].head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>intake_date</th>
      <th>intake_time</th>
      <th>outcome_date</th>
      <th>outcome_time</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>03/03/2019 12:00:00 AM</td>
      <td>16:00:00</td>
      <td>03/03/2019 12:00:00 AM</td>
      <td>16:03:00</td>
    </tr>
    <tr>
      <th>1</th>
      <td>10/03/2018 12:00:00 AM</td>
      <td>22:04:00</td>
      <td>10/12/2018 12:00:00 AM</td>
      <td>12:21:00</td>
    </tr>
    <tr>
      <th>2</th>
      <td>01/26/2019 12:00:00 AM</td>
      <td>13:21:00</td>
      <td>01/26/2019 12:00:00 AM</td>
      <td>17:06:00</td>
    </tr>
    <tr>
      <th>3</th>
      <td>06/08/2019 12:00:00 AM</td>
      <td>14:29:00</td>
      <td>06/08/2019 12:00:00 AM</td>
      <td>14:29:00</td>
    </tr>
    <tr>
      <th>4</th>
      <td>12/31/2018 12:00:00 AM</td>
      <td>12:51:00</td>
      <td>12/31/2018 12:00:00 AM</td>
      <td>13:12:00</td>
    </tr>
  </tbody>
</table>
</div>



_The time inside the date column is unnecessary and will only cause trouble later on. It will be stripped._


```python
#The intake_date column does not contain any null values and the outcome_date column contains 6.
print(fy_2019[fy_2019['intake_date'].str.contains('12:00:00 AM')].shape)
print(fy_2019[fy_2019['outcome_date'].isnull()].shape)
```

    (46409, 34)
    (6, 34)



```python
fy_2019['intake_date'] = fy_2019['intake_date'].str.replace(' 12:00:00 AM', '')
fy_2019['outcome_date'] = fy_2019['outcome_date'].str.replace(' 12:00:00 AM', '')
print(fy_2019[['intake_date','outcome_date']].head(1))
```

      intake_date outcome_date
    0  03/03/2019   03/03/2019


_In order to exact information such as day, month, and so on, the datetime columns need to be converted to DateTime objects._


```python
fy_2019['intake_datetime'] = fy_2019['intake_date'] + ' ' + fy_2019['intake_time']
fy_2019['outcome_datetime'] = fy_2019['outcome_date'] + ' ' + fy_2019['outcome_time']
fy_2019['intake_datetime'] = pd.to_datetime(fy_2019['intake_datetime'], format='%m/%d/%Y %H:%M:%S')
fy_2019['outcome_datetime'] = pd.to_datetime(fy_2019['outcome_datetime'], format='%m/%d/%Y %H:%M:%S')

fy_2020['intake_datetime'] = fy_2020['intake_date'] + ' ' + fy_2020['intake_time']
fy_2020['outcome_datetime'] = fy_2020['outcome_date'] + ' ' + fy_2020['outcome_time']
fy_2020['intake_datetime'] = pd.to_datetime(fy_2020['intake_datetime'], format='%m/%d/%y %H:%M:%S')
fy_2020['outcome_datetime'] = pd.to_datetime(fy_2020['outcome_datetime'], format='%m/%d/%y %H:%M:%S')
```


```python
print(fy_2019[['intake_datetime', 'outcome_datetime']].head(1))
print('\n')
print(fy_2020[['intake_datetime', 'outcome_datetime']].head(1))
```

          intake_datetime    outcome_datetime
    0 2019-03-03 16:00:00 2019-03-03 16:03:00
    
    
          intake_datetime    outcome_datetime
    0 2019-11-08 15:48:00 2019-11-09 11:31:00


## Merge datasets


```python
original_df = pd.concat([fy_2020, fy_2019], axis=0, join='outer')
original_df.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>animal_id</th>
      <th>animal_type</th>
      <th>animal_breed</th>
      <th>kennel_number</th>
      <th>kennel_status</th>
      <th>tag_type</th>
      <th>activity_number</th>
      <th>activity_sequence</th>
      <th>source_id</th>
      <th>census_tract</th>
      <th>council_district</th>
      <th>intake_type</th>
      <th>intake_subtype</th>
      <th>intake_total</th>
      <th>reason</th>
      <th>staff_id</th>
      <th>intake_date</th>
      <th>intake_time</th>
      <th>due_out</th>
      <th>intake_condition</th>
      <th>hold_request</th>
      <th>outcome_type</th>
      <th>outcome_subtype</th>
      <th>outcome_date</th>
      <th>outcome_time</th>
      <th>receipt_number</th>
      <th>impound_number</th>
      <th>service_request_number</th>
      <th>outcome_condition</th>
      <th>chip_status</th>
      <th>animal_origin</th>
      <th>additional_information</th>
      <th>month</th>
      <th>year</th>
      <th>intake_datetime</th>
      <th>outcome_datetime</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>A0144701</td>
      <td>DOG</td>
      <td>HAVANESE</td>
      <td>VT 12</td>
      <td>IMPOUNDED</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>1</td>
      <td>P0098773</td>
      <td>6301</td>
      <td>4</td>
      <td>OWNER SURRENDER</td>
      <td>GENERAL</td>
      <td>1</td>
      <td>PERSNLISSU</td>
      <td>CDM</td>
      <td>11/8/19</td>
      <td>15:48:00</td>
      <td>11/14/19</td>
      <td>APP SICK</td>
      <td>NaN</td>
      <td>RETURNED TO OWNER</td>
      <td>WALK IN</td>
      <td>11/9/19</td>
      <td>11:31:00</td>
      <td>R19-558731</td>
      <td>K19-486742</td>
      <td>NaN</td>
      <td>APP SICK</td>
      <td>SCAN CHIP</td>
      <td>OVER THE COUNTER</td>
      <td>RETURNED TO OWNER</td>
      <td>NOV.2019</td>
      <td>FY2020</td>
      <td>2019-11-08 15:48:00</td>
      <td>2019-11-09 11:31:00</td>
    </tr>
    <tr>
      <th>1</th>
      <td>A0442587</td>
      <td>DOG</td>
      <td>TERRIER MIX</td>
      <td>FREEZER</td>
      <td>IMPOUNDED</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>1</td>
      <td>P0492284</td>
      <td>7102</td>
      <td>2</td>
      <td>OWNER SURRENDER</td>
      <td>DEAD ON ARRIVAL</td>
      <td>1</td>
      <td>OTHRINTAKS</td>
      <td>CDM</td>
      <td>11/10/19</td>
      <td>14:18:00</td>
      <td>11/10/19</td>
      <td>DEAD</td>
      <td>NaN</td>
      <td>DEAD ON ARRIVAL</td>
      <td>DISPOSAL</td>
      <td>11/10/19</td>
      <td>0:00:00</td>
      <td>NaN</td>
      <td>K19-486954</td>
      <td>NaN</td>
      <td>DEAD</td>
      <td>SCAN CHIP</td>
      <td>OVER THE COUNTER</td>
      <td>NaN</td>
      <td>NOV.2019</td>
      <td>FY2020</td>
      <td>2019-11-10 14:18:00</td>
      <td>2019-11-10 00:00:00</td>
    </tr>
    <tr>
      <th>2</th>
      <td>A0458972</td>
      <td>DOG</td>
      <td>CATAHOULA</td>
      <td>RECEIVING</td>
      <td>UNAVAILABLE</td>
      <td>NaN</td>
      <td>A19-195601</td>
      <td>1</td>
      <td>P9991718</td>
      <td>4600</td>
      <td>1</td>
      <td>STRAY</td>
      <td>AT LARGE</td>
      <td>1</td>
      <td>OTHER</td>
      <td>MG1718</td>
      <td>10/3/19</td>
      <td>11:08:00</td>
      <td>10/3/19</td>
      <td>TREATABLE REHABILITABLE NON-CONTAGIOUS</td>
      <td>NaN</td>
      <td>RETURNED TO OWNER</td>
      <td>FIELD</td>
      <td>10/3/19</td>
      <td>13:36:00</td>
      <td>NaN</td>
      <td>K19-482022</td>
      <td>NaN</td>
      <td>TREATABLE REHABILITABLE NON-CONTAGIOUS</td>
      <td>SCAN NO CHIP</td>
      <td>SWEEP</td>
      <td>NaN</td>
      <td>OCT.2019</td>
      <td>FY2020</td>
      <td>2019-10-03 11:08:00</td>
      <td>2019-10-03 13:36:00</td>
    </tr>
    <tr>
      <th>3</th>
      <td>A0525642</td>
      <td>DOG</td>
      <td>GERM SHEPHERD</td>
      <td>INJD 001</td>
      <td>IMPOUNDED</td>
      <td>NaN</td>
      <td>A19-196573</td>
      <td>1</td>
      <td>P0903792</td>
      <td>16605</td>
      <td>8</td>
      <td>OWNER SURRENDER</td>
      <td>GENERAL</td>
      <td>1</td>
      <td>OTHER</td>
      <td>RA 1549</td>
      <td>10/11/19</td>
      <td>9:55:00</td>
      <td>10/17/19</td>
      <td>TREATABLE REHABILITABLE NON-CONTAGIOUS</td>
      <td>EMERGENCY RESCUE</td>
      <td>TRANSFER</td>
      <td>MEDICAL-CONTAGIOUS</td>
      <td>10/15/19</td>
      <td>17:35:00</td>
      <td>NaN</td>
      <td>K19-483073</td>
      <td>NaN</td>
      <td>TREATABLE REHABILITABLE NON-CONTAGIOUS</td>
      <td>SCAN CHIP</td>
      <td>SWEEP</td>
      <td>TAGGED</td>
      <td>OCT.2019</td>
      <td>FY2020</td>
      <td>2019-10-11 09:55:00</td>
      <td>2019-10-15 17:35:00</td>
    </tr>
    <tr>
      <th>4</th>
      <td>A0565586</td>
      <td>DOG</td>
      <td>SILKY TERRIER</td>
      <td>LFD 119</td>
      <td>UNAVAILABLE</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>1</td>
      <td>P0890077</td>
      <td>6900</td>
      <td>1</td>
      <td>STRAY</td>
      <td>AT LARGE</td>
      <td>1</td>
      <td>OTHRINTAKS</td>
      <td>JR</td>
      <td>11/8/19</td>
      <td>11:55:00</td>
      <td>11/14/19</td>
      <td>APP WNL</td>
      <td>RESCU ONLY</td>
      <td>RETURNED TO OWNER</td>
      <td>WALK IN</td>
      <td>11/9/19</td>
      <td>12:57:00</td>
      <td>R19-558750</td>
      <td>K19-486694</td>
      <td>NaN</td>
      <td>APP WNL</td>
      <td>SCAN CHIP</td>
      <td>OVER THE COUNTER</td>
      <td>RETURNED TO OWNER</td>
      <td>NOV.2019</td>
      <td>FY2020</td>
      <td>2019-11-08 11:55:00</td>
      <td>2019-11-09 12:57:00</td>
    </tr>
  </tbody>
</table>
</div>



_Looked at value counts of many columns to determine which ones are necessary._

## Create dataframe with necessary columns


```python
dallas = original_df[['animal_id', 'animal_type', 'animal_breed', 'council_district', 'intake_type', 'intake_subtype', 
                      'intake_condition', 'intake_datetime', 'reason', 'outcome_type', 
                      'outcome_subtype', 'outcome_condition', 'outcome_datetime']]
```


```python
dallas.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>animal_id</th>
      <th>animal_type</th>
      <th>animal_breed</th>
      <th>council_district</th>
      <th>intake_type</th>
      <th>intake_subtype</th>
      <th>intake_condition</th>
      <th>intake_datetime</th>
      <th>reason</th>
      <th>outcome_type</th>
      <th>outcome_subtype</th>
      <th>outcome_condition</th>
      <th>outcome_datetime</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>A0144701</td>
      <td>DOG</td>
      <td>HAVANESE</td>
      <td>4</td>
      <td>OWNER SURRENDER</td>
      <td>GENERAL</td>
      <td>APP SICK</td>
      <td>2019-11-08 15:48:00</td>
      <td>PERSNLISSU</td>
      <td>RETURNED TO OWNER</td>
      <td>WALK IN</td>
      <td>APP SICK</td>
      <td>2019-11-09 11:31:00</td>
    </tr>
    <tr>
      <th>1</th>
      <td>A0442587</td>
      <td>DOG</td>
      <td>TERRIER MIX</td>
      <td>2</td>
      <td>OWNER SURRENDER</td>
      <td>DEAD ON ARRIVAL</td>
      <td>DEAD</td>
      <td>2019-11-10 14:18:00</td>
      <td>OTHRINTAKS</td>
      <td>DEAD ON ARRIVAL</td>
      <td>DISPOSAL</td>
      <td>DEAD</td>
      <td>2019-11-10 00:00:00</td>
    </tr>
    <tr>
      <th>2</th>
      <td>A0458972</td>
      <td>DOG</td>
      <td>CATAHOULA</td>
      <td>1</td>
      <td>STRAY</td>
      <td>AT LARGE</td>
      <td>TREATABLE REHABILITABLE NON-CONTAGIOUS</td>
      <td>2019-10-03 11:08:00</td>
      <td>OTHER</td>
      <td>RETURNED TO OWNER</td>
      <td>FIELD</td>
      <td>TREATABLE REHABILITABLE NON-CONTAGIOUS</td>
      <td>2019-10-03 13:36:00</td>
    </tr>
    <tr>
      <th>3</th>
      <td>A0525642</td>
      <td>DOG</td>
      <td>GERM SHEPHERD</td>
      <td>8</td>
      <td>OWNER SURRENDER</td>
      <td>GENERAL</td>
      <td>TREATABLE REHABILITABLE NON-CONTAGIOUS</td>
      <td>2019-10-11 09:55:00</td>
      <td>OTHER</td>
      <td>TRANSFER</td>
      <td>MEDICAL-CONTAGIOUS</td>
      <td>TREATABLE REHABILITABLE NON-CONTAGIOUS</td>
      <td>2019-10-15 17:35:00</td>
    </tr>
    <tr>
      <th>4</th>
      <td>A0565586</td>
      <td>DOG</td>
      <td>SILKY TERRIER</td>
      <td>1</td>
      <td>STRAY</td>
      <td>AT LARGE</td>
      <td>APP WNL</td>
      <td>2019-11-08 11:55:00</td>
      <td>OTHRINTAKS</td>
      <td>RETURNED TO OWNER</td>
      <td>WALK IN</td>
      <td>APP WNL</td>
      <td>2019-11-09 12:57:00</td>
    </tr>
  </tbody>
</table>
</div>



## Missing values and strange datatypes


```python
dallas.info()
```

    <class 'pandas.core.frame.DataFrame'>
    Int64Index: 66656 entries, 0 to 46408
    Data columns (total 13 columns):
     #   Column             Non-Null Count  Dtype         
    ---  ------             --------------  -----         
     0   animal_id          66656 non-null  object        
     1   animal_type        66656 non-null  object        
     2   animal_breed       66656 non-null  object        
     3   council_district   63398 non-null  object        
     4   intake_type        66656 non-null  object        
     5   intake_subtype     66656 non-null  object        
     6   intake_condition   66656 non-null  object        
     7   intake_datetime    66656 non-null  datetime64[ns]
     8   reason             45300 non-null  object        
     9   outcome_type       66656 non-null  object        
     10  outcome_subtype    66656 non-null  object        
     11  outcome_condition  63930 non-null  object        
     12  outcome_datetime   66331 non-null  datetime64[ns]
    dtypes: datetime64[ns](2), object(11)
    memory usage: 7.1+ MB


_Every column seems to have minimal amounts of missing values except for the 'reason' column. We will check the values within that column and see if it is important._


```python
dallas['reason'].unique()
```




    array(['PERSNLISSU', 'OTHRINTAKS', 'OTHER', 'MEDICAL', 'FINANCIAL',
           'BEHAVIOR', 'NOTRIGHTFT', nan, 'HOUSING', 'TOO OLD', 'ILL',
           'EUTHANASIA ILL', 'LANDLORD', 'COST', 'DEAD ON ARRIVAL',
           'QUARANTINE', 'OWNER DIED', 'NO HOME', 'AGGRESSIVE - ANIMAL',
           'MOVE', 'OTHER PET', 'ALLERGIC', 'VOCAL', 'RESPONSIBLE',
           'MOVE APT', 'NO TIME', 'NO YARD', 'OWNER PROBLEM',
           'DESTRUCTIVE OUTSIDE', 'BLIND', 'AGGRESSIVE - PEOPLE', 'ESCAPES',
           'BITES', 'FOSTER', 'DESTRUCTIVE AT HOME', 'CAUTIONCAT', 'HYPER',
           'INJURED', 'ABANDON', 'CHILD PROBLEM', 'ATTENTION', 'TRAVEL',
           'DISOBIDIEN', 'FOUND ANIM', 'NEW BABY', 'TOO BIG', 'NOFRIENDLY',
           'JUMPS UP', 'TOO MANY', 'GIFT', 'HOUSE SOIL', 'RETURN', 'AFRAID',
           'WONT ALLOW', 'UNKNOWN', 'PET LIMITS', 'STRAY', 'FENCE',
           'CONFISCATE', 'WILDLIFE', 'WANTS OUT', 'KILLED ANOTHER ANIMAL',
           'EUTHANASIA OTHER', 'TOO YOUNG', 'CHASES PEOPLE', 'WRONG SEX',
           'EUTHANASIA OLD', 'EUTHANASIA BEHAV', 'ZONE', 'DEAF', 'SHEDS',
           'BLIND/DEAF', 'CRUELTY', 'DULL'], dtype=object)



_Most of the reasons are similar but different and very specific. It will not be too useful for this hypothesis since we are looking at simply the intake condition and the general intake type. Checking out the value counts, they are also mainly in the 'other' category will small amounts in the other categories. We can safely drop the 'reason' column entirely._


```python
pd.options.mode.chained_assignment = None

dallas.drop(['reason'], axis=1, inplace=True)
```


```python
# check to make sure 'reason' column got dropped
dallas.columns
```




    Index(['animal_id', 'animal_type', 'animal_breed', 'council_district',
           'intake_type', 'intake_subtype', 'intake_condition', 'intake_datetime',
           'outcome_type', 'outcome_subtype', 'outcome_condition',
           'outcome_datetime'],
          dtype='object')



_The rest of the columns do not contain a huge amount of missing values that would affect the testing. Therefore, we will drop all rows with null values._


```python
dallas.dropna(axis=0, inplace=True)
```


```python
dallas.info()
```

    <class 'pandas.core.frame.DataFrame'>
    Int64Index: 62860 entries, 0 to 46408
    Data columns (total 12 columns):
     #   Column             Non-Null Count  Dtype         
    ---  ------             --------------  -----         
     0   animal_id          62860 non-null  object        
     1   animal_type        62860 non-null  object        
     2   animal_breed       62860 non-null  object        
     3   council_district   62860 non-null  object        
     4   intake_type        62860 non-null  object        
     5   intake_subtype     62860 non-null  object        
     6   intake_condition   62860 non-null  object        
     7   intake_datetime    62860 non-null  datetime64[ns]
     8   outcome_type       62860 non-null  object        
     9   outcome_subtype    62860 non-null  object        
     10  outcome_condition  62860 non-null  object        
     11  outcome_datetime   62860 non-null  datetime64[ns]
    dtypes: datetime64[ns](2), object(10)
    memory usage: 6.2+ MB



```python
dallas['council_district'].value_counts(dropna=False)
```




    6.0     9277
    4.0     6000
    8.0     5540
    5.0     4893
    6       4756
    7.0     3938
    1.0     3809
    3.0     3195
    2.0     2357
    4       2224
    8       2041
    5       1894
    9.0     1565
    7       1432
    1       1299
    3       1248
    10.0    1134
    14.0     831
    12.0     823
    11.0     802
    13.0     782
    2        767
    9        651
    10       396
    13       341
    14       318
    11       313
    12       220
    0          7
    AS         4
    21.0       2
    0.0        1
    Name: council_district, dtype: int64



_The council district is a bit messy. It has multiple datatypes but are basically the same number. The numbers will have to be changed to integer type and drop the random string value.  
Also, looking at the Dallas district map, there are no districts 0 or 21. Those rows will also be dropped._


```python
#Taking only rows where council_district is not the string value thus dropping those rows.
dallas = dallas[(dallas['council_district'] != 'AS')]
```


```python
#Mapping the int() function on all values to change the datatype
dallas['council_district'] = dallas['council_district'].map(int)
```


```python
#Dropping all the district 0's and 21's
dallas.drop(dallas[dallas['council_district'] == 0].index, inplace=True)
dallas.drop(dallas[dallas['council_district'] == 21].index, inplace=True)
```


```python
dallas['council_district'].value_counts().sort_index()
```




    1      5107
    2      3123
    3      4442
    4      8224
    5      6787
    6     14032
    7      5370
    8      7578
    9      2216
    10     1530
    11     1115
    12     1043
    13     1123
    14     1149
    Name: council_district, dtype: int64



### Datatypes


```python
dallas.dtypes
```




    animal_id                    object
    animal_type                  object
    animal_breed                 object
    council_district              int64
    intake_type                  object
    intake_subtype               object
    intake_condition             object
    intake_datetime      datetime64[ns]
    outcome_type                 object
    outcome_subtype              object
    outcome_condition            object
    outcome_datetime     datetime64[ns]
    dtype: object



_animal id should be an integer type but it contains an 'A' in front. It will need to be stripped and convert to int._


```python
dallas['animal_id'] = dallas['animal_id'].str.strip('A')
dallas['animal_id'].head()
```




    0    0144701
    1    0442587
    2    0458972
    3    0525642
    4    0565586
    Name: animal_id, dtype: object




```python
dallas['animal_id'] = dallas['animal_id'].astype('int')
dallas['animal_id'].head()
```




    0    144701
    1    442587
    2    458972
    3    525642
    4    565586
    Name: animal_id, dtype: int64



### Reset Index


```python
#Check index duplicates
dallas[dallas.index.duplicated()].count()
```




    animal_id            17856
    animal_type          17856
    animal_breed         17856
    council_district     17856
    intake_type          17856
    intake_subtype       17856
    intake_condition     17856
    intake_datetime      17856
    outcome_type         17856
    outcome_subtype      17856
    outcome_condition    17856
    outcome_datetime     17856
    dtype: int64




```python
dallas[dallas.index == 1207]
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>animal_id</th>
      <th>animal_type</th>
      <th>animal_breed</th>
      <th>council_district</th>
      <th>intake_type</th>
      <th>intake_subtype</th>
      <th>intake_condition</th>
      <th>intake_datetime</th>
      <th>outcome_type</th>
      <th>outcome_subtype</th>
      <th>outcome_condition</th>
      <th>outcome_datetime</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1207</th>
      <td>A1074783</td>
      <td>CAT</td>
      <td>DOMESTIC SH</td>
      <td>6</td>
      <td>TRANSFER</td>
      <td>SURGERY</td>
      <td>HEALTHY</td>
      <td>2019-10-30 09:14:00</td>
      <td>TRANSFER</td>
      <td>SURGERY</td>
      <td>HEALTHY</td>
      <td>2019-10-30 17:30:00</td>
    </tr>
    <tr>
      <th>1207</th>
      <td>A0955803</td>
      <td>CAT</td>
      <td>DOMESTIC SH</td>
      <td>11</td>
      <td>OWNER SURRENDER</td>
      <td>GENERAL</td>
      <td>TREATABLE REHABILITABLE NON-CONTAGIOUS</td>
      <td>2019-06-28 11:49:00</td>
      <td>ADOPTION</td>
      <td>EAC</td>
      <td>HEALTHY</td>
      <td>2019-07-17 17:02:00</td>
    </tr>
  </tbody>
</table>
</div>



_There appears to be duplicate indexes in the dataframe even though the animal id is different. It will need to be reset to 0 to the length of the dataframe._


```python
dallas.index = np.arange(len(dallas))
```


```python
dallas[dallas.index.duplicated()].count()
```




    animal_id            0
    animal_type          0
    animal_breed         0
    council_district     0
    intake_type          0
    intake_subtype       0
    intake_condition     0
    intake_datetime      0
    outcome_type         0
    outcome_subtype      0
    outcome_condition    0
    outcome_datetime     0
    dtype: int64



# Exploratory Data Analysis (EDA)


```python
#Plotting helper functions

def autolabel(bar_graph, ax):
    for bar in bar_graph:
        height = bar.get_height()
        ax.annotate(f'{height}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom')

def bar_count(ax, cat_col, dog_col, width=0.35):
    axes_labels = cat_col.index
    x = np.arange(len(axes_labels))
    cat = ax.bar(x - width/2, cat_col, width, label='Cats', color='tomato')
    dog = ax.bar(x + width/2, dog_col, width, label='Dogs', color='lightseagreen')
    ax.set_ylabel('Counts')
    ax.set_title(f'Count of {cat_col.name}: Cats vs Dogs')
    ax.set_xticks(x)
    ax.set_xticklabels(axes_labels, rotation=45)
    ax.legend(loc='upper center')
    autolabel(cat, ax)
    autolabel(dog, ax)
    
def bar_percent(ax, cat_col, dog_col, width=0.35):
    cats_data = cat_col.values
    cats_percent = ((cats_data / cats_data.sum()) * 100).round()
    dogs_data = dog_col.values
    dogs_percent = ((dogs_data / dogs_data.sum()) * 100).round()
    
    axes_labels = cat_col.index
    x = np.arange(len(axes_labels))
    cat = ax.bar(x - width/2, cats_percent, width, label='Cats', color='tomato')
    dog = ax.bar(x + width/2, dogs_percent, width, label='Dogs', color='lightseagreen')
    ax.set_ylabel('Percentage')
    ax.set_title(f'Percentage of {cat_col.name}: Cats vs Dogs')
    ax.set_xticks(x)
    ax.set_xticklabels(axes_labels, rotation=45)
    ax.legend(loc='upper center')
    autolabel(cat, ax)
    autolabel(dog, ax)
```

## Column Values


```python
dallas.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>animal_id</th>
      <th>animal_type</th>
      <th>animal_breed</th>
      <th>council_district</th>
      <th>intake_type</th>
      <th>intake_subtype</th>
      <th>intake_condition</th>
      <th>intake_datetime</th>
      <th>outcome_type</th>
      <th>outcome_subtype</th>
      <th>outcome_condition</th>
      <th>outcome_datetime</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>144701</td>
      <td>DOG</td>
      <td>HAVANESE</td>
      <td>4</td>
      <td>OWNER SURRENDER</td>
      <td>GENERAL</td>
      <td>APP SICK</td>
      <td>2019-11-08 15:48:00</td>
      <td>RETURNED TO OWNER</td>
      <td>WALK IN</td>
      <td>APP SICK</td>
      <td>2019-11-09 11:31:00</td>
    </tr>
    <tr>
      <th>1</th>
      <td>442587</td>
      <td>DOG</td>
      <td>TERRIER MIX</td>
      <td>2</td>
      <td>OWNER SURRENDER</td>
      <td>DEAD ON ARRIVAL</td>
      <td>DEAD</td>
      <td>2019-11-10 14:18:00</td>
      <td>DEAD ON ARRIVAL</td>
      <td>DISPOSAL</td>
      <td>DEAD</td>
      <td>2019-11-10 00:00:00</td>
    </tr>
    <tr>
      <th>2</th>
      <td>458972</td>
      <td>DOG</td>
      <td>CATAHOULA</td>
      <td>1</td>
      <td>STRAY</td>
      <td>AT LARGE</td>
      <td>TREATABLE REHABILITABLE NON-CONTAGIOUS</td>
      <td>2019-10-03 11:08:00</td>
      <td>RETURNED TO OWNER</td>
      <td>FIELD</td>
      <td>TREATABLE REHABILITABLE NON-CONTAGIOUS</td>
      <td>2019-10-03 13:36:00</td>
    </tr>
    <tr>
      <th>3</th>
      <td>525642</td>
      <td>DOG</td>
      <td>GERM SHEPHERD</td>
      <td>8</td>
      <td>OWNER SURRENDER</td>
      <td>GENERAL</td>
      <td>TREATABLE REHABILITABLE NON-CONTAGIOUS</td>
      <td>2019-10-11 09:55:00</td>
      <td>TRANSFER</td>
      <td>MEDICAL-CONTAGIOUS</td>
      <td>TREATABLE REHABILITABLE NON-CONTAGIOUS</td>
      <td>2019-10-15 17:35:00</td>
    </tr>
    <tr>
      <th>4</th>
      <td>565586</td>
      <td>DOG</td>
      <td>SILKY TERRIER</td>
      <td>1</td>
      <td>STRAY</td>
      <td>AT LARGE</td>
      <td>APP WNL</td>
      <td>2019-11-08 11:55:00</td>
      <td>RETURNED TO OWNER</td>
      <td>WALK IN</td>
      <td>APP WNL</td>
      <td>2019-11-09 12:57:00</td>
    </tr>
  </tbody>
</table>
</div>




```python
dallas.shape
```




    (62839, 12)



#### Animal ID


```python
# Check the animal ids for any duplicates
dallas['animal_id'].nunique()
```




    49276




```python
#Testing to see how many ids have more than one count
(dallas['animal_id'].value_counts()).head(8750)
```




    1050623    1
    953138     1
    1052043    1
    1049994    1
    1056137    1
              ..
    1071172    1
    1075266    1
    1095736    1
    1077313    1
    1079360    1
    Name: animal_id, Length: 8750, dtype: int64




```python
#Keep the most recent entries
dallas.drop_duplicates('animal_id', keep='last', inplace=True)
```


```python
#Check if any animal ids still have multiple counts.
(dallas['animal_id'].value_counts() > 1).any()
```




    False




```python
dallas['animal_type'].value_counts()
```




    DOG          35847
    CAT          11334
    WILDLIFE      1625
    BIRD           442
    LIVESTOCK       28
    Name: animal_type, dtype: int64



_For the hypothesis, the only data we need are cats and dogs. The dataframe will be filtered to have only rows where the animal type is either cats or dogs._


```python
dallas = dallas[(dallas['animal_type'] == 'CAT') | (dallas['animal_type'] == 'DOG')]
dallas['animal_type'].value_counts()
```




    DOG    35847
    CAT    11334
    Name: animal_type, dtype: int64




```python
#Plot counts
sns.countplot(x=dallas['animal_type'])
plt.savefig('animal_type_count.png')
```


![png](output_71_0.png)



```python
print('Intake Type: ', list(dallas['intake_type'].unique()))
print('\n')
print('Intake Subtype: ', list(dallas['intake_subtype'].unique()))
print('\n')
print('Intake Condition: ', list(dallas['intake_condition'].unique()))
print('\n')
print('Outcome Type: ', list(dallas['outcome_type'].unique()))
print('\n')
print('Outcome Subtype: ', list(dallas['outcome_subtype'].unique()))
print('\n')
print('Outcome Condition: ', list(dallas['outcome_condition'].unique()))
```

    Intake Type:  ['OWNER SURRENDER', 'STRAY', 'CONFISCATED', 'TRANSFER', 'FOSTER', 'TREATMENT', 'KEEPSAFE', 'DISPOS REQ']
    
    
    Intake Subtype:  ['GENERAL', 'DEAD ON ARRIVAL', 'AT LARGE', 'RETURN30', 'EUTHANASIA REQUESTED', 'CONFINED', 'QUARANTINE', 'OTHER', 'KEEP SAFE', 'QUARANTINE DEAD ON ARRIVAL', 'SURGERY', 'RETURN', 'SAC DEAD ON ARRIVAL', 'APPOINT', 'HEART WORM', 'CRUELTY', 'DIED', 'TREATMENT', 'DANGEROUS', 'TRAP NEUTER RETURN', 'FOR ADOPT', 'EVICTION', 'KEEP SAFE DEAD ON ARRIVAL', 'FIELD', 'OWN ARREST', 'SX POST OP', 'OTC', 'MISSING', 'AGG OPPS', 'ALUMNI', 'OWN HOSPIT', 'FOLLOWUP', 'SAC', 'ARC', 'POSSIBLY OWNED', 'TRAP PROGRAM', 'SPCA TEXAS', 'CRUELT DEAD ON ARRIVAL', 'STRAY']
    
    
    Intake Condition:  ['APP SICK', 'DEAD', 'TREATABLE REHABILITABLE NON-CONTAGIOUS', 'APP WNL', 'UNHEALTHY UNTREATABLE NON-CONTAGIOUS', 'CRITICAL', 'APP INJ', 'UNKNOWN', 'UNHEALTHY UNTREATABLE CONTAGIOUS', 'TREATABLE MANAGEABLE NON-CONTAGIOUS', 'TREATABLE MANAGEABLE CONTAGIOUS', 'HEALTHY', 'UNDERAGE', 'TREATABLE REHABILITABLE CONTAGIOUS', 'FATAL', 'DECEASED']
    
    
    Outcome Type:  ['RETURNED TO OWNER', 'DEAD ON ARRIVAL', 'TRANSFER', 'DIED', 'EUTHANIZED', 'ADOPTION', 'FOSTER', 'TREATMENT', 'MISSING', 'DISPOSAL']
    
    
    Outcome Subtype:  ['WALK IN', 'DISPOSAL', 'FIELD', 'MEDICAL-CONTAGIOUS', 'ENROUTE', 'BITE', 'HUMANE', 'MICROCHIP', 'PROMOTION', 'MEDICAL-NONCONTAGIOUS', 'BEHAVIOR', 'OFFSITE', 'SPACE', 'EAC', 'HOLD', 'TRANSPORT', 'UNDERAGE', 'GENERAL', 'TRANS-INV', 'INV', 'SPCA TEXAS', 'SURGERY', 'IN FOSTER', 'EVENT', 'WESTMORELD', 'SPAY NEUTER NETWORK', 'COMPLETED', 'DAS OUTREACH', 'IN KENNEL', 'TO ADOPT', 'BY FOSTER', 'TREATMENT', 'DD/AGG', 'TNR', 'NTCOMPLETE', 'IN SURGERY', 'SBI', 'OTHER', 'SHORT TERM', 'RETURN', 'STOLEN', 'MEDICAL', 'ARC', 'TELEADOPT', 'AT VETERINARIAN', 'DOA', 'SNR', 'REFERRAL', 'ESCAPED', 'DAS', 'AD TV', 'UNKNOWN', 'ADOPT/TRANSFER', 'RESCUE', 'STAFF', 'TAG NUMBER', 'PHONE', 'WEB', 'RESCUE GROUP', 'PAY PENDNG', 'LIVESTOCK', 'EAC OFFSIT']
    
    
    Outcome Condition:  ['APP SICK', 'DEAD', 'TREATABLE REHABILITABLE NON-CONTAGIOUS', 'APP WNL', 'UNHEALTHY UNTREATABLE NON-CONTAGIOUS', 'UNKNOWN', 'CRITICAL', 'APP INJ', 'FATAL', 'UNDERAGE', 'TREATABLE MANAGEABLE NON-CONTAGIOUS', 'TREATABLE MANAGEABLE CONTAGIOUS', 'HEALTHY', 'TREATABLE REHABILITABLE CONTAGIOUS', 'UNHEALTHY UNTREATABLE CONTAGIOUS', 'DECEASED']



```python
dallas['intake_type'].value_counts()
```




    STRAY              31856
    OWNER SURRENDER    10366
    FOSTER              2180
    CONFISCATED         2001
    TREATMENT            444
    TRANSFER             323
    KEEPSAFE               7
    DISPOS REQ             4
    Name: intake_type, dtype: int64




```python
dallas['outcome_type'].value_counts()
```




    ADOPTION             15850
    RETURNED TO OWNER    13545
    TRANSFER              9140
    EUTHANIZED            5556
    FOSTER                1654
    DIED                   497
    DEAD ON ARRIVAL        465
    TREATMENT              444
    MISSING                 27
    DISPOSAL                 3
    Name: outcome_type, dtype: int64




```python
dallas.groupby(['outcome_type', 'outcome_subtype']).count()['intake_subtype'].head(50)
```




    outcome_type       outcome_subtype      
    ADOPTION           AD TV                        2
                       BY FOSTER                  128
                       EAC                       1346
                       EAC OFFSIT                   2
                       EVENT                      109
                       IN FOSTER                  279
                       OFFSITE                    320
                       PAY PENDNG                   7
                       PHONE                        1
                       PROMOTION                 1308
                       REFERRAL                   146
                       RESCUE GROUP                 1
                       TELEADOPT                   16
                       WALK IN                  11885
                       WEB                          6
                       WESTMORELD                 294
    DEAD ON ARRIVAL    DISPOSAL                   356
                       HOLD                        72
                       RETURN                       5
                       TRANS-INV                   32
    DIED               AT VETERINARIAN             10
                       DOA                         11
                       ENROUTE                     59
                       IN FOSTER                  109
                       IN KENNEL                  290
                       IN SURGERY                  18
    DISPOSAL           ARC                          3
    EUTHANIZED         BEHAVIOR                  1182
                       BITE                       352
                       DD/AGG                      27
                       HUMANE                    1766
                       MEDICAL-CONTAGIOUS         313
                       MEDICAL-NONCONTAGIOUS      620
                       SBI                         13
                       SPACE                     1283
    FOSTER             DAS                        128
                       GENERAL                     96
                       RESCUE                      12
                       SHORT TERM                 115
                       STAFF                       20
                       SURGERY                     48
                       TO ADOPT                    23
                       TRANSPORT                   75
                       TREATMENT                  348
                       UNDERAGE                   789
    MISSING            ESCAPED                      8
                       STOLEN                      11
                       UNKNOWN                      8
    RETURNED TO OWNER  DAS OUTREACH                 1
                       FIELD                     8425
    Name: intake_subtype, dtype: int64




```python
dallas.groupby(['intake_type', 'intake_subtype']).count()['outcome_type'].head(50)
```




    intake_type      intake_subtype            
    CONFISCATED      CRUELT DEAD ON ARRIVAL           18
                     CRUELTY                         113
                     DANGEROUS                        25
                     EVICTION                         63
                     KEEP SAFE                       646
                     KEEP SAFE DEAD ON ARRIVAL        17
                     QUARANTINE                     1024
                     QUARANTINE DEAD ON ARRIVAL       83
                     SAC                              10
                     SAC DEAD ON ARRIVAL               2
    DISPOS REQ       ARC                               2
                     FIELD                             2
    FOSTER           APPOINT                           1
                     DIED                             79
                     FOR ADOPT                         2
                     GENERAL                         787
                     MISSING                           5
                     QUARANTINE                        7
                     RETURN                          661
                     STRAY                             3
                     SURGERY                         247
                     TREATMENT                       388
    KEEPSAFE         OTHER                             2
                     OWN ARREST                        2
                     OWN HOSPIT                        3
    OWNER SURRENDER  APPOINT                          48
                     DEAD ON ARRIVAL                 165
                     EUTHANASIA REQUESTED            222
                     FIELD                            20
                     GENERAL                        8796
                     QUARANTINE                      153
                     RETURN30                        962
    STRAY            AGG OPPS                         13
                     AT LARGE                      26703
                     CONFINED                       3756
                     DEAD ON ARRIVAL                 169
                     FIELD                             8
                     OTC                              24
                     POSSIBLY OWNED                 1058
                     QUARANTINE                       72
                     TRAP NEUTER RETURN               13
                     TRAP PROGRAM                     40
    TRANSFER         ALUMNI                            5
                     OTHER                           227
                     SPCA TEXAS                        4
                     SURGERY                          86
                     TREATMENT                         1
    TREATMENT        FOLLOWUP                          6
                     HEART WORM                      428
                     SX POST OP                       10
    Name: outcome_type, dtype: int64



_Looking at the outcome type and the outcome subtype, it seems the intake subtype and outcome subtype is not really necessary. The main goal is to see if they make it to adoption stage, but it doesn't matter who does the adoption. The intake subtype and outcome subtype column will be dropped._


```python
dallas.drop('outcome_subtype', axis=1, inplace=True)
# dallas.drop('intake_subtype', axis=1, inplace=True)
```


    ---------------------------------------------------------------------------

    KeyError                                  Traceback (most recent call last)

    <ipython-input-99-83caf78db0e7> in <module>()
    ----> 1 dallas.drop('outcome_subtype', axis=1, inplace=True)
          2 # dallas.drop('intake_subtype', axis=1, inplace=True)


    ~/anaconda3/lib/python3.7/site-packages/pandas/core/frame.py in drop(self, labels, axis, index, columns, level, inplace, errors)
       3995             level=level,
       3996             inplace=inplace,
    -> 3997             errors=errors,
       3998         )
       3999 


    ~/anaconda3/lib/python3.7/site-packages/pandas/core/generic.py in drop(self, labels, axis, index, columns, level, inplace, errors)
       3934         for axis, labels in axes.items():
       3935             if labels is not None:
    -> 3936                 obj = obj._drop_axis(labels, axis, level=level, errors=errors)
       3937 
       3938         if inplace:


    ~/anaconda3/lib/python3.7/site-packages/pandas/core/generic.py in _drop_axis(self, labels, axis, level, errors)
       3968                 new_axis = axis.drop(labels, level=level, errors=errors)
       3969             else:
    -> 3970                 new_axis = axis.drop(labels, errors=errors)
       3971             result = self.reindex(**{axis_name: new_axis})
       3972 


    ~/anaconda3/lib/python3.7/site-packages/pandas/core/indexes/base.py in drop(self, labels, errors)
       5016         if mask.any():
       5017             if errors != "ignore":
    -> 5018                 raise KeyError(f"{labels[mask]} not found in axis")
       5019             indexer = indexer[~mask]
       5020         return self.delete(indexer)


    KeyError: "['outcome_subtype'] not found in axis"



```python
dallas.head(1)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>animal_id</th>
      <th>animal_type</th>
      <th>animal_breed</th>
      <th>council_district</th>
      <th>intake_type</th>
      <th>intake_subtype</th>
      <th>intake_condition</th>
      <th>intake_datetime</th>
      <th>outcome_type</th>
      <th>outcome_condition</th>
      <th>outcome_datetime</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>144701</td>
      <td>DOG</td>
      <td>HAVANESE</td>
      <td>4</td>
      <td>OWNER SURRENDER</td>
      <td>GENERAL</td>
      <td>APP SICK</td>
      <td>2019-11-08 15:48:00</td>
      <td>RETURNED TO OWNER</td>
      <td>APP SICK</td>
      <td>2019-11-09 11:31:00</td>
    </tr>
  </tbody>
</table>
</div>




```python
cats = dallas[dallas['animal_type'] == 'CAT']
dogs = dallas[dallas['animal_type'] == 'DOG']
```


```python
dogs['animal_breed'].value_counts().sort_values(ascending=False).head(5)
```




    PIT BULL         8053
    CHIHUAHUA SH     5253
    GERM SHEPHERD    4580
    LABRADOR RETR    3989
    CAIRN TERRIER    1108
    Name: animal_breed, dtype: int64




```python
cats['animal_breed'].value_counts().sort_values(ascending=False).head(5)
```




    DOMESTIC SH    9923
    DOMESTIC MH     957
    DOMESTIC LH     177
    SIAMESE         136
    AMER SH          52
    Name: animal_breed, dtype: int64



## Percentages

cats:
- count per month intakes (intake_datetime.dt.month)
- each_intake_type/total_intake_type
- each_outcome_type/total_outcome_type
- count of month outcomes  
- type of intake and the outcome

dogs:
- count per month intakes (intake_datetime.dt.month)
- each_intake_type/total_intake_type
- each_outcome_type/total_outcome_type
- count of month outcomes
- type of intake and the outcome


```python
dallas['month'] = dallas['intake_datetime'].dt.month
cats['month'] = cats['intake_datetime'].dt.month
dogs['month'] = dogs['intake_datetime'].dt.month
cats['day'] = cats['intake_datetime'].dt.day
dogs['day'] = dogs['intake_datetime'].dt.day

cats_month = cats['month'].value_counts().values
cats_percent = ((cats_month / cats_month.sum()) * 100).round()
dogs_month = dogs['month'].value_counts().values
dogs_percent = ((dogs_month / dogs_month.sum()) * 100).round()

cats_day = cats['day'].value_counts().values
cats_day_percent = ((cats_day / cats_day.sum()) * 100).round()
dogs_day = dogs['day'].value_counts().values
dogs_day_percent = ((dogs_day / dogs_day.sum()) * 100).round()
```

### Count/Percentage of Cats and Dogs per Month


```python
fig, axes = plt.subplots(2,1,figsize=(12,10))

bar_count(axes[0], cats['month'].value_counts().sort_index(), 
          dogs['month'].value_counts().sort_index())

bar_percent(axes[1], cats['month'].value_counts().sort_index(), 
            dogs['month'].value_counts().sort_index())

axes[0].set_xlabel('month')
axes[1].set_xlabel('month')

plt.tight_layout()

plt.savefig('count_perc_monthly.png')
```


![png](output_87_0.png)



```python
fig, ax = plt.subplots(figsize=(12,4))
sns.lineplot(x=cats['month'].value_counts().index, y=cats_percent)
sns.lineplot(x=dogs['month'].value_counts().index, y=dogs_percent)
ax.legend(labels=['cat', 'dog'])
ax.set_xlabel('month')
ax.set_ylabel('percent of intake')
ax.set_title('Percentage of Monthly Intakes: Cats vs Dogs')

plt.savefig('lineplt_count_perc_monthly.png')
```


![png](output_88_0.png)


### Count/Percentage of Intake Type


```python
fig, axes = plt.subplots(2,1, figsize=(12,7))

bar_count(axes[0], cats['intake_type'].value_counts(), dogs['intake_type'].value_counts())
bar_percent(axes[1], cats['intake_type'].value_counts(), dogs['intake_type'].value_counts())

axes[0].set_xlabel('intake_type')
axes[1].set_xlabel('intake_type')

plt.tight_layout()

plt.savefig('count_intake_type.png')
```


![png](output_90_0.png)


### Intake Type Per Month


```python
g = sns.catplot(x='month', col="intake_type", hue='animal_type', col_wrap=4,
                data=dallas, kind="count", palette= 'pastel', legend_out=False)

plt.tight_layout()

plt.savefig('catplot_intake_type_monthly.png')
```


![png](output_92_0.png)


### Count/Percentage of Outcome Type


```python
fig, axes = plt.subplots(2,1, figsize=(12,7))

bar_count(axes[0], cats['outcome_type'].value_counts(), dogs['outcome_type'].value_counts())
bar_percent(axes[1], cats['outcome_type'].value_counts(), dogs['outcome_type'].value_counts())

axes[0].set_xlabel('outcome_type')
axes[1].set_xlabel('outcome_type')

plt.tight_layout()

plt.savefig('count_outcome_type.png')
```


![png](output_94_0.png)


## Outcome Type per Month


```python
g = sns.catplot(x='month', col='outcome_type', hue='animal_type', col_wrap=4,
                data=dallas, kind="count", palette= 'pastel', legend_out=False)

plt.tight_layout()

plt.savefig('catplot_outcome_type_monthly.png')
```


![png](output_96_0.png)


## Hypothesis Testing


```python

```


```python

```


```python

```


```python

```


```python

```

## Map


```python
dallas.to_pickle('df.pkl.bz2', compression='bz2')
```
