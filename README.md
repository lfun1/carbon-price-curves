# CarbonInsight: Guiding Companies to Net-zero
### Using supply and demand projections, our software advises companies on the tradeoff between decarbonizing their existing business practices and offsetting emissions through carbon credit purchasing.

By Lisa Fung, Elias Chikwanda, Rudraksh Mohapatra, Sam Jonker

Devpost: https://devpost.com/software/carbon-price-curves

## Inspiration

As the imperative to reduce carbon emissions intensifies, businesses are increasingly adopting innovative approaches to shrink their carbon footprint. One such approach, carbon offsetting, has grown into a [$5.5 billion industry](https://journals.library.columbia.edu/index.php/cjel/article/view/10442), garnering support from both fossil fuel companies and environmental advocates alike. Rather than curbing emissions directly at their source, carbon offsets mitigate carbon pollution by either preventing potential emissions or directly extracting carbon dioxide from the atmosphere, often employing technologies such as carbon capture and storage (CCS) or direct air capture (DAC). Presently, numerous critical sectors—such as the aviation industry—face challenges in achieving decarbonization due to financial constraints, material limitations, and a lack of innovative solutions. **As such, the combination of decarbonization strategies and carbon offsetting is often the most economical; by reducing easily avoidable emissions and offsetting the rest, companies can achieve net-zero emissions without the financial pressures of complete emissions reductions.**

However, there are three existing barriers to achieving this diversified net-zero strategy. First, reducing emissions is often a lengthy process, often taking years to decarbonize key components of a company’s business model fully. Second, reducing low-cost emissions is dependent on the equilibrium price of carbon offset—a price that often needs to be calculated far in advance to successfully execute decarbonization. Third, the financial tradeoff between the price of offsets and emissions reductions is blurry, with no clear brightline between offset and reduced emissions. 

## What does our project do?
Our product solves these issues by providing key insights about decarbonization strategy through forward pricing curves for carbon offsets. By calculating the expected demand and supply of carbon offsets for a given time in the future, the market equilibrium—the going price of carbon offsets at that time—can be estimated and given to the user in the present. Our results are displayed on a website dashboard. 

Our project contains two central components: the market price of carbon credits over time, based on calculated demand and supply curves, and a carbon-zero pathway based on these curves (based on user inputs and other external data). The demand and supply curves are generated for each year until the user’s target year, this allows them to see how the market changes year-by-year, allowing them to optimize their offset buying distribution over a certain period. The carbon-zero pathway allows 

After inputting information about a company’s carbon footprint, emissions targets, and the marginal cost of abatement, financial metrics about the best carbon-zero path are computed. The output of this function relies on market equilibrium outputs only available after computing the forward price curves. The output gives the user valuable information about the percentage breakdown between decarbonized emission reductions and credit offsets, and the financial projections of both strategies. 

This tool, importantly, allows companies to see how the market price of carbon credits changes over time based on user-given inputs such as the type of carbon removal technology, the year of their net-zero goal, and the scope of emissions they are considering. This tool emphasizes the importance of decarbonization by reorienting the goal of maximizing profits towards environmental advocacy. This is key in assisting companies plan their emissions-reduction strategy in the most economical way—two priorities that have often been at odds with each other. 

## How we built our project 
We built all of our projection models in Python and used the Reflex framework to display our outputs in a user dashboard. Each of the three system functions—the demand curve, supply curve, and decarbonization-offset tradeoff scheme—are integrated into the user dashboard, with various inputs related to the computation of the base futures curve model and tradeoff model being imputed as fields. Each of the three system functions are described below: 

The demand curve uses the emissions profiles of the top 2,000 largest companies in the world to project their future carbon emissions based on their emissions reduction goals. Using generated GICS sector data for industry-specific emissions—combined with company revenue—we project yearly emissions—including scope 1, 2, and 3 emissions—depending on carbon reduction goals. Using an exponential Pareto distribution—tuned to represent companies buying offsets closer to their consumption date—we generalize the year-to-year demand for carbon permits on a per-company basis. This data returns the expected demand for carbon credits per year for a theoretical global market. Using this data, combined with decarbonization prices generalized from half-normal, sector-level decarbonization costs, our model produces the expected carbon demand for a given period for each company. As each company faces a different cost of decarbonizing their business, the marginal benefit of each company is unique. We fit a demand curve to these projected quantity and price demands from individual companies using polynomial regressions from this data. This process is done for each year in the model. 

The supply curve is interpolated from the technology pathway of the carbon credit and price range. Based on our research, most companies pay anywhere from $50/ton CO2 to $700/ton CO2 for a range of carbon credits. This data is combined with the cost of implementing the selected pathway for a single ton of CO2 and the ranking of the industries based on their relative CO2 emissions. A coefficient is calculated on these values that inform the supply curve on the scale of 50$/tCO2 to 700$/tCO2.  We create a supply curve for each year until the user-specified target year with the values being adjusted for the following years accordingly. 

The decarbonization-offset tradeoff graph is produced by mapping another exponential Pareto distribution to the marginal cost of reducing carbon emissions. The resulting intersection of the market price of carbon offsets for a given year with the CDF returns the percentage of total emissions for which it is more economical to reduce the production of emissions over buying offsets, and vice versa. The total cost associated with purchasing carbon offsets, alongside the quantity, can be calculated for a given company’s carbon footprint. 

## Challenges we ran into
The biggest challenge we ran into was the lack of data for building the supply curves. One way in which we handled this was by taking data corresponding to the maximum and minimum prices, as well as the range of carbon credits companies were buying in bulk. We used these to generate a pseudo-supply curve that would allow us to reasonably estimate the curve as if we had the data. We expect this problem to be solved as more data becomes available.



## What we learned and accomplished
We learned a lot about time-series analysis, data analysis, and synthesizing, as well as how to use Reflex to implement our website.  We made a working model and website on a project that aimed to encapsulate the entire carbon credits market for the next few decades. 

## What's next for CarbonInsights

Short Term: The biggest thing we would like to change is to make the website dynamically update. Although the models we wrote _are perfectly suited to update dynamically_, the Reflex framework we are using has made that difficult. 

Long Term: Improve the statistical models to create the projection for the supply-demand curves and use ARIMA, ETS, and ML models like Random Forests to validate and provide a more detailed analysis of the trends.
