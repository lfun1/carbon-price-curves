#Libraries
import numpy as np
import matplotlib.pyplot as plt
import csv
import pandas as pd
from scipy import stats
import statsmodels.api as sm
import statsmodels.formula.api as smf
import random
import math
from scipy.stats import halfnorm, norm


"""Supply Model"""
"""Example call: df_supply = supply_model(2030, "tech", "Biochar")"""

def supply_model(year: int, industry: str, pathway: str):
  #user inputs
  #year = int(input('Enter emission goal year'))
  #industry = str(input('Enter industry type: tech, manufacturing, finance, oil/gas, other'))
  #pathway = str(input('CCS, Biochar, Mineralization, DAC'))

  #creation of the x_axis for all supply curves.
  x_axis = []
  for i in range(1, 501):
      x_axis.append(i*10000000)


  #defines the coefficient we use.
  def coefficient_calc(industry, pathway):
    ind = 0
    if(industry == 'tech' or industry == 'other'):
      ind = 2
    if(industry == 'manufacturing'):
      ind = 3
    if(industry == 'finance'):
      ind = 1
    if(industry == 'oil/gas'):
      ind = 4

    p = 20
    if(pathway == 'CCS'):
        p = 50
    if(pathway == 'Biochar'):
        p = 150
    if(pathway == 'Mineralization'):
        p = 30
    if(pathway == 'DAC'):
        p = 800

    coefficient = ((ind/10) + (p/1300) + 50)/10
    return coefficient


  coefficient = coefficient_calc(industry, pathway)
  #print(coefficient)

  supply_df = pd.DataFrame()
  supply_df["Quantity"] = x_axis

  #Makes our supply curves for all the years.
  def supply_generator(year, coefficient):
          
          #for i in range(2024, year + 1):
              count = year - 2023
              y_axis = []
              for j in range(1, 500):
                  if(j == 1):
                      y_axis.append(50 + (((65/99000)*x_axis[j])/10000+ count) + np.random.randint(0, 10*coefficient))
                  if(j == 500):
                      y_axis.append(y_axis[j-1])
                  else:
                      if(np.random.randint(0, 2) == 1):
                          y_axis.append(((65/99000)*(x_axis[j])/10000+ count)) # np.random.randint(0, coefficient))
                      else:
                          y_axis.append(50*((65/99000)*(x_axis[j])/10000)**(1/4) + count) # np.random.randint(0, coefficient))

              #Printing plot for the year
              #print(i)
              #print(coefficient)
              #print(y_axis)
              y_axis1 = []
              y_axis2 = []

              m = np.polyfit(x_axis, y_axis, 2)
              x = np.array(x_axis)

              f1 = np.polyval(m,x)

              price = []
              #Translating the curve to an array
              for j in range(0, 500):
                price.append(np.polyval(m, x_axis[j]))
              arr = np.array(price)
              supply_df[i] = arr
        
  m = supply_generator(year, coefficient)

  supply_df = supply_df.rename(columns={500:"Price"})
  return supply_df


"""Demand Model"""
"""Example call: 
modelInputs = {
    "modelLength":30, # gives us actual year
    "scope1":1,
    "scope2":1,
    "scope3":1,
}

scenarioInputs = {
    "industry":"Technology",
    "goal_year":"2045", #yes
    "goal_red":"-53", #yes
    "bio_char":"on",
    "mineralization":"on",
    "cur_emission":"434",
    "market_price":"434",
    "company_price":"54", #yes
    }

demand_df = demand_model('assets/demand_ref_data.xlsx',2.6,3.7,1.7,modelInputs,scenarioInputs)
"""

def prob_function(a,b,c,percent): #source: https://www.mdpi.com/2227-9717/11/1/232
  #desmos: https://www.desmos.com/calculator/9wa4fw41v8
  radical = -a*((percent/(b*(1-(percent-0.0001))))**c)
  compute = 1 - math.e**radical
  return compute

def demand_model(file_path,lambdav,alphav,betav,modelInputs,scenarioInputs):
  years = modelInputs["modelLength"]
  currentYear = 2024
  yearEndDate = currentYear + years

  #PROB INPUTS:
  # lambdav,alphav,betav = 2.6,3.7,1.7

  #emissions conversions (source: https://www.msci.com/documents/1296102/26195050/MSCI-Net-Zero-Tracker.pdf)
  sectorEmissions = { #measured in tons of CO^2 per million USD
    "Services":[50,15,400],
    "Manufacturing":[20,10,650], #household personal products
    "Materials":[950,200,1500],
    "Infrastructure":[550,10,300],
    "Retail":[10,5,650],
    "Biotech, health care & pharma":[10,5,300],
    "Fossil Fuels":[500,50,4250],
    "Food, beverage & agriculture":[50,20,830],
    "Transportation services":[550,10,300],
    "Power generation":[2650,100,1950],
    "Hospitality":[50,15,400], #consumer servicing                       25
    "Apparel":[10,5,650],
    "Chemicals":[950,200,1500], #materials                            1
  }

  carbonMBbySector = { #average cost of co2 reduction per industry, currently arbitrary but roughly mapped to cost
    "Services":20,
    "Manufacturing":40,
    "Materials":45,
    "Infrastructure":20,
    "Retail":0,
    "Biotech, health care & pharma":25,
    "Fossil Fuels":80,
    "Food, beverage & agriculture":20,
    "Transportation services":35,
    "Power generation":30,
    "Hospitality":10,
    "Apparel":20,
    "Chemicals":35,
  }

  #importing & cleaning
  data_import = pd.read_excel(file_path)
  data_import = data_import[data_import['actor_type'] == "Company"]
  data_import = data_import[data_import['id_code'] != 'COM-1396'] #remove foreign currency issue companies
  data_import = data_import[data_import['id_code'] != 'COM-1111']
  data_import = data_import[data_import['id_code'] != 'COM-0774']
  data_import = data_import[data_import['annual_revenue'] > 0] #only keep companies with revanue

  #emissions target percent breakdown:
  zero_carbon = ['Net zero','Carbon neutral(ity)','Climate neutral','Zero emissions','Zero carbon']
  emissionsTargetsList = []
  for (target, percentReduction) in zip(data_import['end_target'],data_import['end_target_percentage_reduction']):
    if target in zero_carbon:
      emissionsTargetsList.append(1) #100$% reduction
    elif percentReduction > 0:
      emissionsTargetsList.append(percentReduction/100)
    else:
      emissionsTargetsList.append(0)

  data_import.insert(2,"co2_reduction_percent",emissionsTargetsList,True)

  #calculate company emissions 2024

  carbonEmissionsList = []

  #compute industry average emissions, unweighted (todo, implement weighted average)
  sum = 0
  for k in sectorEmissions.values():
    sum += k[0]+k[1]+k[2]
  emissionsAverage = sum/len(sectorEmissions)


  #industry average:

  for (ghg,revanue,industry,reduction_target) in zip(data_import['ghg'],data_import['annual_revenue'],data_import['industry'],data_import['co2_reduction_percent']):
    #print(reduction_target)
    if ghg > 0:
      carbonEmissionsList.append(float(ghg))
    elif pd.isna(industry) == False:
      scopeSumTonPerDollar = (sectorEmissions[industry][0]+sectorEmissions[industry][1])/1000000 #+sectorEmissions[industry][2]
      carbonEmissionsList.append(revanue*scopeSumTonPerDollar)
    else:
      carbonEmissionsList.append(revanue*emissionsAverage) #does industry average if no industry is listed and multiplies by emissions reduction target per year

  data_import.insert(2,"co2_emission_projections",carbonEmissionsList,True)

  #emissions reduction over time calculations
  #NEW VERSION 3.0!!

  yearlists = {}

  for year in range(years):
    incrementedYear = currentYear + year
    yearlists[incrementedYear] = list()

  for index, row in data_import.iterrows():
    emissionsReductionsDict = {}

    #per company, define their midterm and final goals
    if pd.isna(row['interim_target_percentage_reduction']) == False:
      midtermReduction = float(row['interim_target_percentage_reduction']/100)
    else:
      midtermReduction = row['interim_target_percentage_reduction']

    if pd.isna(row['interim_target_year']) == False:
      midtermReductionDate = int(row['interim_target_year'])
    else:
      midtermReductionDate = row['interim_target_year']

    if pd.isna(row['end_target_year']) == False:
      finalReductionDate = int(row['end_target_year'])
    else:
      finalReductionsDate = row['end_target_year']

    entireLength = finalReductionDate - currentYear

    if pd.isna(entireLength) == False: #checks if there is vald target to begin with
      for l in range(int(entireLength)):
        incrementedYear = currentYear + l
        totalemissions = int(entireLength)*row['co2_emission_projections']
        if l == 0:
          emissionsReductionsDict[incrementedYear] = prob_function(lambdav,alphav,betav,(1/int(entireLength)))*totalemissions
        else:
          convertion = prob_function(lambdav,alphav,betav,(l/int(entireLength)))-prob_function(lambdav,alphav,betav,((l-1)/int(entireLength)))
          emissionsReductionsDict[incrementedYear] = convertion*totalemissions

    else:
      for r in range(years):
        incrementedYear = currentYear + r
        emissionsReductionsDict[incrementedYear] = 0


    #compile individual carbon reductions per company into yearly bins of all company offsets
    for year in range(years): #this is super jank but it works [adds emissions data to original dataframe]
      incrementedYear = currentYear + year
      if incrementedYear in emissionsReductionsDict:
        yearlists[incrementedYear].append(emissionsReductionsDict[incrementedYear])
      else: #if target is met, fill in zero carbon offsets for each successive year (todo, make this some operating expense model)
        yearlists[incrementedYear].append(row['co2_emission_projections'])


  #insert co2 emissions projections back into the original dataframe
  ticker = 0
  for key, value in yearlists.items():
    data_import.insert(2+ticker,key,value,True)
    ticker += 1


  plotting = {}
  for key, value in yearlists.items():
    plotting[key] = data_import[key].sum()


  #cost functions for curve calculations
  industryCostList = []
  for index, row in data_import.iterrows():
    if pd.isna(row['industry']) == False:
      industryCost = float(halfnorm.rvs(loc = 0, scale = 100, size=1)) #carbonMBbySector[row['industry']]
      industryCostList.append(round(industryCost, -1)) #rounds all values to the nearest $10
    else:
      industryCostList.append(round(float(halfnorm.rvs(loc = 20, scale = 100, size=1)), -1)) #20 is arbitrary here

  data_import.insert(2,"MB",industryCostList,True)

  demandCurvePointsList = []

  for k in range(years):
    currentYear = 2024+k

    priceDict = {}
    for k in range(45):
      priceDict[k*10] = float()

    for index, row in data_import.iterrows():
      MB = int(row["MB"])
      priceDict[MB] += row[currentYear] #carbon usage per year

    priceDict.pop(0)

    demandCurvePointsList.append(priceDict)
    
  demand_curves = demandCurvePointsList[-1]

  prices = np.array(list(demand_curves.keys()))
  quantities = np.array(list(demand_curves.values()))
  demand_coeffs = np.polyfit(np.log(prices), quantities, 1)

  neg_log_prices = np.arange(1, 350)
  neg_log_quantities = np.array([(demand_coeffs[0]*np.log(x) + demand_coeffs[1]) for x in neg_log_prices])
  demand_df = pd.DataFrame({"Price": neg_log_prices, "Quantity" : neg_log_quantities})

  return demand_df


"""CDF demand"""
"""Call: comparison(totalEmissions,maxDecarbonizationPrice,baselineDecarbonizationPrice,eq_price)"""
def closest_value(dictionary, target): #chatgpt my love
    closest_val = None
    min_difference = float('inf')  # Initialize with positive infinity

    for key, value in dictionary.items():
        difference = abs(value - target)
        if difference < min_difference:
            min_difference = difference
            mykey = key

    return mykey

totalEmissions = 17000
maxDecarbonizationPrice = 140
eq_price = 70
baselineDecarbonizationPrice = 30

def comparison(totalEmissions,maxDecarbonizationPrice,baselineDecarbonizationPrice,eq_price):
  outputCompanyComparison = {}
  curvePoints = {}
  for k in range(20):
    curvePoints[0.05*k] = ((prob_function(2.6,3.7,1.7,0.05*k)*maxDecarbonizationPrice)+baselineDecarbonizationPrice)
  #print(curvePoints)
  outputCompanyComparison['curvePoints'] = curvePoints
  plt.plot(curvePoints.keys(),curvePoints.values())
  plt.axhline(y=eq_price)
  plt.show()
  carbonCreditQ = totalEmissions*(1 - closest_value(curvePoints,eq_price))
  outputCompanyComparison['carbonCreditsPurchasedTotalQ'] = carbonCreditQ
  outputCompanyComparison['carbonCreditsPurchasedTotalCost'] = carbonCreditQ*eq_price


  decarbonizationCosts = 0
  for key, value in curvePoints.items():
    if key < closest_value(curvePoints,eq_price):
      decarbonizationCosts += value*0.05*totalEmissions
    else:
      pass

  outputCompanyComparison['decarbonizationCosts'] = decarbonizationCosts

  df = pd.DataFrame({'x': list(outputCompanyComparison['curvePoints'].keys()), 'y': list(outputCompanyComparison['curvePoints'].values())})
  return df

def main():
    return 0

if __name__ == "__main__":
    main()