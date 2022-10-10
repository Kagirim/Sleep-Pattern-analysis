import pandas as pd
import re
from matplotlib import pyplot as plt
from scipy.stats import ttest_ind

all_files = ["bedTimeHours.csv", "dayCaffeine.csv", "gender.csv", "minsAwake.csv", 
"minutesNap.csv", "nightCaffeine.csv", "section.csv", "SSI.csv", 
"toSleepMinutes.csv", "useAlarm.csv", "wakeHours.csv"]
section_number = 218

# Parse the files
for file_name in all_files:
    variable_name = re.search("(.+?).csv$", file_name).group(1)
    sample_df = pd
    
    # create the dataframes
    globals()[variable_name] = pd.DataFrame(pd.read_csv(file_name, header=None))

    # Overall medians
    globals()[f"{variable_name}_median"] = globals()[variable_name].median(skipna=True).T

hoursInBed = (wakeHours-bedTimeHours)
hours_napping = minutesNap / 60
hours_to_sleep = toSleepMinutes / 60
hours_awake = minsAwake / 60
total_daily_sleep_median = ((wakeHours-bedTimeHours) + hours_napping - hours_to_sleep - hours_awake).median(skipna=True).T

# concatenate median table
median_table = pd.concat([wakeHours_median, bedTimeHours_median, hoursInBed.median(skipna=True).T, 
toSleepMinutes_median, minutesNap_median, minsAwake_median, total_daily_sleep_median, SSI_median], axis = 1)

# reset index
median_table.index = median_table.index + 1

# arrange table
median_table = median_table.T
my_info = median_table[218]
median_table = median_table.drop(columns=[218])
median_table.insert(loc=0, column=218, value=my_info)
median_table.index = ["wakeHours", "bedTimeHours", "hoursInBed", 
"toSleepMinutes", "minutesNap", "minsAwake", "total_daily_sleep", "SSI"]
print(median_table)

# Statistics for individuals (bedTimeHours & hoursInBed)
average_bed_time_hours = bedTimeHours.mean(skipna=True)
average_hours_in_bed = hoursInBed.mean(skipna=True)

average_pair = pd.concat([average_bed_time_hours, average_hours_in_bed, section], axis=1)
average_pair.index += 1
average_pair = average_pair.T
average_pair.index = ["average_bed_time_hours", "average_hours_in_bed", "section"]
average_pair = average_pair.T
print(average_pair)

# Scatter plot
# average_pair.plot.scatter(x="average_bed_time_hours", y="average_hours_in_bed")

# Adding multiple data labels
instructors = average_pair[average_pair['section'] == 0]
section1 = average_pair.query("(section > 0) and (section < 6) or (section == 7)", inplace=False)
section2 = average_pair[average_pair['section'] == 6]

ax = instructors.plot(x="average_bed_time_hours", y="average_hours_in_bed", kind='scatter', c='r', label='Instructors')
section1.plot(x="average_bed_time_hours", y="average_hours_in_bed", kind='scatter', ax=ax, c='g', label='CS1173 students')
section2.plot(x="average_bed_time_hours", y="average_hours_in_bed", kind='scatter', ax=ax, c='b', label='DS4003/DS5003')
plt.show()

# Correlation
# For each section
instructor_correlation = instructors.corr()
CS1173_students_correlation = section1.corr()
CS1173_students_correlation = section2.corr()

# For overall
overall_pair = pd.concat([bedTimeHours.mean(axis=0), hoursInBed.mean(axis=0)], axis=1)
overall_pair.index += 1
overall_pair = overall_pair.T
overall_pair.index += 1
overall_pair.index = ["average_bed_time_hours", "average_hours_in_bed"]

overall_pair_average = overall_pair.mean(axis=1)

overall_correlation = overall_pair_average.corr()
print(overall_correlation)

# 4	Boxplot of average daily sleep by gender
hours_napping.index += 1
hours_napping = hours_napping.T
hours_napping.index += 1
hours_napping = hours_napping.T

gender.columns = gender.iloc[0]
gender = gender[1:]
gender.reset_index(drop=True, inplace=True)

gender.index += 1
men = hours_napping[gender.gender[gender.gender == "male"].index.tolist()]
women = hours_napping[gender.gender[gender.gender == "female"].index.tolist()]

men_average = men.mean(axis=1)
women_average = women.mean(axis=1)

hours_napping_average = pd.concat([men_average, women_average], axis=1)
hours_napping_average.columns = ["men", "women"]

hours_napping_average.plot(kind="box", title="Average daily sleep by gender")
plt.show()

# Differences in sleep patterns

# ttest_function
def average_ttest(test_data, test_group, groups):
    test_data.index += 1
    test_data = test_data.T
    test_data.index += 1
    test_data = test_data.T

    test_group.reset_index(drop=True, inplace=True)
    test_group.index += 1
    
    globals()[groups[0]] = test_data[test_group.gender[test_group.gender == groups[0]].index.tolist()]
    globals()[groups[1]] = test_data[test_group.gender[test_group.gender == groups[1]].index.tolist()]

    globals()[f"{groups[0]}_mean"] = globals()[groups[0]].mean(axis=1)
    globals()[f"{groups[1]}_mean"] = globals()[groups[1]].mean(axis=1)

    combined_mean = pd.concat([globals()[f"{groups[0]}_mean"], globals()[f"{groups[1]}_mean"]], axis=1)
    combined_mean.columns = [groups[0], groups[1]]

    ttest_result = ttest_ind(combined_mean[groups[0]], combined_mean[groups[1]])

    print(ttest_result)

average_ttest(bedTimeHours, gender, ["male", "female"])
average_ttest(useAlarm, gender, ["male", "female"])
napping_ttest = ttest_ind(hours_napping_average["men"], hours_napping_average["women"])