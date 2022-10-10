# %%
import pandas as pd
import re
from matplotlib import pyplot as plt
from scipy.stats import ttest_ind
from pathlib import Path

# %%
all_files = ["bedTimeHours.csv", "dayCaffeine.csv", "gender.csv", "minsAwake.csv", 
"minutesNap.csv", "nightCaffeine.csv", "section.csv", "SSI.csv", 
"toSleepMinutes.csv", "useAlarm.csv", "wakeHours.csv"]
section_number = 218

# %% [markdown]
# Parse the files

# %%
for file_name in all_files:
    variable_name = re.search("(.+?).csv$", file_name).group(1)
    
    # create the dataframes
    globals()[variable_name] = pd.DataFrame(pd.read_csv(Path("data/"+ str(file_name)).resolve(), header=None))

    # Overall medians
    globals()[f"{variable_name}_median"] = globals()[variable_name].median(skipna=True).T


# %%
hoursInBed = wakeHours-bedTimeHours
hours_napping = minutesNap / 60
hours_to_sleep = toSleepMinutes / 60
hours_awake = minsAwake / 60
total_daily_sleep_median = ((wakeHours-bedTimeHours) + hours_napping - hours_to_sleep - hours_awake).median(skipna=True).T


# %% [markdown]
# concatenate median table

# %%
median_table = pd.concat([wakeHours_median, bedTimeHours_median, hoursInBed.median(skipna=True).T, 
toSleepMinutes_median, minutesNap_median, minsAwake_median, total_daily_sleep_median, SSI_median], axis = 1)


# %% [markdown]
# reset index

# %%
median_table.index = median_table.index + 1

# %% [markdown]
# arrange table

# %%
median_table = median_table.T
my_info = median_table[218]
median_table = median_table.drop(columns=[218])
median_table.insert(loc=0, column=218, value=my_info)
median_table.index = ["wakeHours", "bedTimeHours", "hoursInBed", 
"toSleepMinutes", "minutesNap", "minsAwake", "total_daily_sleep", "SSI"]
print(median_table)

# %% [markdown]
# Statistics for individuals (bedTimeHours & hoursInBed)

# %%
average_bed_time_hours = bedTimeHours.mean(skipna=True)
average_hours_in_bed = hoursInBed.mean(skipna=True)

average_pair = pd.concat([average_bed_time_hours, average_hours_in_bed, section], axis=1)
average_pair.index += 1
average_pair = average_pair.T
average_pair.index = ["average_bed_time_hours", "average_hours_in_bed", "section"]
average_pair = average_pair.T
print(average_pair)

# %% [markdown]
# Scatter plot

# %%
# average_pair.plot.scatter(x="average_bed_time_hours", y="average_hours_in_bed")

# %% [markdown]
# Adding multiple data labels

# %%
instructors = average_pair[average_pair['section'] == 0]
section1 = average_pair.query("(section > 0) and (section < 6) or (section == 7)", inplace=False)
section2 = average_pair[average_pair['section'] == 6]

ax = instructors.plot(x="average_bed_time_hours", y="average_hours_in_bed", kind='scatter', c='r', label='Instructors')
section1.plot(x="average_bed_time_hours", y="average_hours_in_bed", kind='scatter', ax=ax, c='g', label='CS1173 students')
section2.plot(x="average_bed_time_hours", y="average_hours_in_bed", kind='scatter', ax=ax, c='b', label='DS4003/DS5003')
plt.show()

# %% [markdown]
# Correlation
# For each section

# %%
instructor_correlation = instructors.iloc[:, :2].corr()
CS1173_students_correlation = section1.iloc[:, :2].corr()
DS4003_DS5003_students_correlation = section2.iloc[:, :2].corr()

# %% [markdown]
# For overall

# %%
overall_pair = pd.concat([bedTimeHours.mean(axis=0), hoursInBed.mean(axis=0)], axis=1)
overall_pair.index += 1
overall_pair = overall_pair.T
overall_pair.index += 1
overall_pair.index = ["average_bed_time_hours", "average_hours_in_bed"]

overall_correlation = overall_pair.T.corr()
print(overall_correlation)

# %% [markdown]
# Boxplot of average daily sleep by gender

# %%
hoursInBed.index += 1
hoursInBed = hoursInBed.T
hoursInBed.index += 1
hoursInBed = hoursInBed.T

gender.columns = gender.iloc[0]
gender = gender[1:]
gender.reset_index(drop=True, inplace=True)

gender.index += 1
men = hoursInBed[gender.gender[gender.gender == "male"].index.tolist()]
women = hoursInBed[gender.gender[gender.gender == "female"].index.tolist()]

men_average = men.mean(axis=1)
women_average = women.mean(axis=1)

hours_in_bed_average = pd.concat([men_average, women_average], axis=1)
hours_in_bed_average.columns = ["men", "women"]

fig, ax = plt.subplots()
hours_in_bed_average.plot(ax=ax, kind="box", title="Average daily sleep by gender")

plt.show()

# %% [markdown]
# Differences in sleep patterns
# ttest_function

# %%
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

    ttest_result = ttest_ind(combined_mean[groups[0]], combined_mean[groups[1]])[0]

    print(ttest_result)

print('bed time hours:', end = " ")
average_ttest(bedTimeHours, gender, ["male", "female"])
print("use alarm:", end = " ")
average_ttest(useAlarm, gender, ["male", "female"])
print("napping hours:", end = " ")
print(ttest_ind(hours_napping_average["men"], hours_napping_average["women"])[0])


