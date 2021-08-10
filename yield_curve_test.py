from QuantLib import *
import QuantLib as ql
import numpy as np
from math import exp
import matplotlib.pyplot as plt

class leo:
    def __init__(self,name_arg,age_arg,gender_arg, *args):
        self.name = name_arg
        self.age = age_arg
        self.gender = gender_arg

    def treatment(self):
        symp = self.age * self.name / self.gender
        return symp

    def final(self):
        number = self.treatment() * 50
        print(number)


test = leo(6,3,9)
#test.final()

leo_period = Period('1M')
start = Date(12,12,2018)
expiration = Date(17,6,2022)
maturity = Date (12,12,2042)
leo_mksch = MakeSchedule(start,maturity,leo_period)

# create hard-coded yield term structure
# TODO : Remove this hardcoding with pullig the curve from an excel sheet or REST API

def CreateYieldTermStructure():
    termStructureDates = [Date(12, December, 2018), Date(13, December, 2018), Date(19, December, 2018),
                          Date(12, January, 2019), Date(12, February, 2019), Date(12, March, 2019),
                          Date(12, June, 2019),
                          Date(12, December, 2019), Date(12, December, 2020), Date(12, December, 2021),
                          Date(12, December, 2022),
                          Date(12, December, 2023), Date(12, December, 2024), Date(12, December, 2025),
                          Date(12, December, 2026),
                          Date(12, December, 2027), Date(12, December, 2028), Date(12, December, 2029),
                          Date(12, December, 2030),
                          Date(12, December, 2033), Date(12, December, 2038), Date(12, December, 2043),
                          Date(12, December, 2048),
                          Date(12, December, 2058), Date(12, December, 2068)]

    # USD Libor zero swap discount factors from swap manager as of 12.12.2018
    termStructureDiscountFactors = [1.0, 0.999758, 0.99957, 0.99792, 0.995597, 0.993108, 0.985659, 0.969519,
                                    0.94423, 0.918219, 0.892931, 0.86814, 0.843459, 0.819195, 0.794985, 0.770981,
                                    0.747243, 0.724021,
                                    0.701601, 0.639109, 0.548016, 0.472681, 0.408786, 0.310937, 0.239833]

    # create yield term structure from a given set of discount factors
    yieldTermStructure = DiscountCurve(termStructureDates, termStructureDiscountFactors, Actual360(), TARGET())
    yieldTermStructure.enableExtrapolation()
    return yieldTermStructure

class leo_grid:
    def __init__(self, startDate, endDate, tenor):
        # create date schedule, ignore conventions and calendars
        self.schedule = Schedule(startDate, endDate, tenor, NullCalendar(),
                                 Unadjusted, Unadjusted, DateGeneration.Forward, False)
        self.dayCounter = Actual365Fixed()
        self.tenor = tenor
    def GetDates(self):
        # get list of scheduled dates
        dates = []
        [dates.append(self.schedule[i]) for i in range(self.GetSize())]
        return dates
    def GetTimes(self):
        # get list of scheduled times
        times = []
        [times.append(self.dayCounter.yearFraction(self.schedule[0], self.schedule[i]))
            for i in range(self.GetSize())]
        return times
    def GetSize(self):
        # get total number of items in schedule
        return len(self.schedule)

def Plot(x, y, title, xlabel):
    # if(y.ndim == 1):
    #     Matplotlib.plot(x, y)
    # else:
    Matplotlib.plot(x,y)
    # for i in range(len(y)):
    #     y_i = y[i]
    #     Matplotlib.plot(x, y_i)
    Matplotlib.title(title)
    Matplotlib.xlabel(xlabel)
    Matplotlib.show()

#Plot(leo_grid(start,maturity,leo_period).GetDates(),CreateYieldTermStructure(),'Yield Structure','Time')

print(CreateYieldTermStructure().forwardRate(start,maturity,Actual360(),Compounded,Quarterly,False))
print(start,maturity)
#Plot(['today','tomorrow'],[2.85,2.95],'test','Date')
termStructureDates = [Date(12, December, 2018), Date(13, December, 2018), Date(19, December, 2018),
                          Date(12, January, 2019), Date(12, February, 2019), Date(12, March, 2019),
                          Date(12, June, 2019),
                          Date(12, December, 2019), Date(12, December, 2020), Date(12, December, 2021),
                          Date(12, December, 2022),
                          Date(12, December, 2023), Date(12, December, 2024), Date(12, December, 2025),
                          Date(12, December, 2026),
                          Date(12, December, 2027), Date(12, December, 2028), Date(12, December, 2029),
                          Date(12, December, 2030),
                          Date(12, December, 2033), Date(12, December, 2038), Date(12, December, 2043),
                          Date(12, December, 2048),
                          Date(12, December, 2058), Date(12, December, 2068)]

    # USD Libor zero swap discount factors from swap manager as of 12.12.2018
termStructureDiscountFactors = [1.0, 0.999758, 0.99957, 0.99792, 0.995597, 0.993108, 0.985659, 0.969519,
                                    0.94423, 0.918219, 0.892931, 0.86814, 0.843459, 0.819195, 0.794985, 0.770981,
                                    0.747243, 0.724021,
                                    0.701601, 0.639109, 0.548016, 0.472681, 0.408786, 0.310937, 0.239833]
curves = np.zeros((len(termStructureDates),len(termStructureDiscountFactors)))

#leo_schd = Schedule(start, maturity, Period(1, Weeks), NullCalendar(),
#            Unadjusted, Unadjusted, DateGeneration.Forward, False)

#dates = []
#[dates.append(leo_schd[i]) for i in range (len(leo_schd))]

#print(dates)

#times = []
#[times.append(Actual365Fixed.yearFraction(leo_schd[0], leo_schd[i])) for i in range(len(leo_schd))]
#print(times)

# for s in (1,len(leo_schd)):
#     for t in (1,len(termStructureDiscountFactors)):
#         curves[s][t] = DiscountCurve(leo_schd, termStructureDiscountFactors, Actual360(), TARGET())
leo_yc = DiscountCurve(termStructureDates, termStructureDiscountFactors, Actual360(), TARGET())
leo_yc.enableExtrapolation()
leo_fwd2 = [leo_yc.forwardRate(dates, dates + ql.Period('1m'),ql.Actual360(),ql.Simple).rate() for dates in leo_yc.dates()]
print(leo_fwd2)

leo_fwd1 = ForwardCurve(termStructureDates, termStructureDiscountFactors, Actual360(), TARGET())
print(leo_fwd1.forwards())

leo_schd = leo_grid(start,maturity,Period(1,Years))
times = leo_schd.GetTimes()
print(times)

plt.figure(figsize= (10,5))
plt.plot(times,leo_fwd2, label = ('DiscountCurve'))
plt.title('Test')
plt.legend()
plt.xlabel('Period in Days')
plt.ylabel('Forwards')
plt.show()

