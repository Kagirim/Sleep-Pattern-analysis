# Sleep pattern analysis
This python script analyses a database of sleeping behaviour of a sample of students. It computes the sleeping index as per the Stanford Sleep Index to assess trends in sleeping behavior.
***
## Data
The sleep diary is 21 days, so each matrix is 21 x N, where N is the number of sleep diaries submitted.  Arrays are parameters that change every day, such as bedtimes, waketimes and napping minutes.
Each vector is N x 1.  Vectors are parameters that don’t change, such as Section and Gender.

### Data Description - Arrays
**BedTimes.**  The time, relative to midnight, in fractions of an hour, when the subject went to bed.  For example, if the subject went to bed at 10p, their bedtime value would be -2.  If they went to bed at 1:30, it would be 1.5.  
**WakeTimes.**  Same format as BedTimes
Unusual situations – up all night “all nighter” – hard coded as went to bed at midnight (0.0) and woke up at 1 minute later (0.16).
**toSleepMinutes** – the number of minutes the individual was awake after they went to bed, before they fell asleep.  If they do not remember their head hitting the pillow, it’s a 0, if they tossed and turned for a short time, probably close to 10.
**minutesAwake** – the number of minutes the individual was awake during their primary sleep period.  If they slept through the night with no interruptions, it is 0.
**minutesNapping** – the number of minutes the individual slept during the day.
**dayCaffeine** – logical value – did the individual consume caffeine (coffee, soda, chocolate) during the period 6a-6p.  Does not reflect AMOUNT of consumption
nightCaffeine – same as dayCaffeine, but for the time frame 6p-6a.
**SSI** – Stanford Sleepiness Index.  A one number summary of how good the previous day was.  A 1 is a VERY GOOD day, where a 7 is almost comatose.  A more detailed explanation can be found at (https://www.gem-measures.org/public/DownloadMeasure.aspx?mid=2442)
**useAlarm**– logical – was an alarm used that morning?

### Data Description – Vectors
**Gender** – the gender of the individual – “male” or “female”
**Section** – the section of the class the student is registered in – Section 0 is instructors, Sections 1-5,7 are CS1173 students and Section 6 is DS4003/DS5003 students.
