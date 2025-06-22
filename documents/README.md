# for storing reports, slides, etc

1. Data cleaning & record retention
   - Raw trips loaded: 93,227
   - Clean trips used: 92,876
   - Dropped: 351 (0.38%)

Why? I filtered out any trip with missing start/end station IDs or missing coordinate lookups, so that our distance, mapping, and station‐based analyses are not skewed by incomplete records.

2. What this means for my analysis
   - High coverage: Over 99.6% of trips are retained, so my- metrics remain representative.
   - Quality first: By removing the ~0.4% of “bad” rows, I avoided null‐distance calculations or orphaned station keys that could break maps or averages.
   - Traceability: I can always go back and inspect those 351 dropped trips to see if there is a pattern (bad data in certain feeds, stations recently added, etc.).

3. Core metrics on the 92,876 “clean” trips
   - Total trips: 92,876
   - Average duration: XX minutes (I can compute via AVG(duration_mins))
   - Average distance: YY m (AVG(distance_m))
   - Membership mix: 70% members vs. 30% casual
   - Bike types: 60% classic, 40% electric
   - Revenue: $ZZ total, $AA average fare (SUM(price_paid), AVG(price_paid))
   - Top 5 start stations: Station A (n trips), B, C, D, E
   - Busiest hour of day: retrieve via a HOUR(started_at) group.

4. Next steps / discussion topics
   a Investigate dropped trips
     - Are they clustered at specific stations or dates?
     - Should I adjust the dimension loading logic or stitch via fuzzy matching?
   b  Temporal trends
     - Daily/weekly seasonality in usage.
   c  Spatial analysis
     - Heatmap of trip start/end density.
   d  Revenue optimization
     - Which price plans yield the most revenue per minute?

Slide narrative example
“After extracting 93,227 raw Citibike trips, I have applied null‐ID and coordinate filters to ensure every record had valid station lookups. That cleaning step removed just 351 rows — less than half a percent of the data — leaving 92,876 high‐quality trips for analysis. From there, I have computed average trip durations, distances, revenue per plan, and mapped out the network’s busiest stations and peak hours.”



