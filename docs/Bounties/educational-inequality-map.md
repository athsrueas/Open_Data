# Educational Inequality Map

**Source:** Adam dystopiq

## Problem
Educational access varies dramatically across regions, but the differences between cost, access, funding, and outcomes are often fragmented across separate datasets and difficult to compare directly.

## Bounty direction
Build an interactive model and map that compares countries on education cost, access, funding, and outcomes, highlighting disparities in educational opportunity.

## Targeted start
Start with a multi-country comparison using a small set of consistently available indicators, then expand the model as more detailed regional or subnational data becomes available.

## Datasets
- School availability
- Funding
- Literacy rates

## Graph advantage
- School -> serves -> population
- Region -> receives -> funding

## Visualization
- Map showing education access disparities
- Interactive model where you can compare countries in terms of cost, access, outcomes, and visualize the data

## Notes
- Normalize indicators by population size and age cohorts so cross-country comparisons are more meaningful.
- Separate national, regional, and school-level data where available to avoid overstating precision.
- Track source year carefully, since education, funding, and literacy data are often reported on different cadences.
- Define a transparent comparison framework for "cost," "access," and "outcomes" before building rankings.

## Starting point suggestions
- Begin with a global Phase 1 dataset from UNESCO, World Bank, or other widely available public education indicators.
- Build a minimum graph around countries, regions, schools, populations, and funding flows.
- Produce one map view for access disparities and one comparison view for cost, access, and outcome metrics.
- Document data gaps explicitly for countries where school availability or funding data is incomplete.
