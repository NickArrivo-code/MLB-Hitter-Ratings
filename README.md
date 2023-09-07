# MLB-Hitter-Ratings
My name is Nick Arrivo, I am a Data Analyst for Pelotero Corporation, specializing in Player Development.
I created this MLB Hitter Rating system to prepare a model template for how we will use Pelotero to track in-game data for amateur players.
This model incorporates measures that aren't outcome-based.
I Used exit velocty (max,avg, and 95th percentile), barrel %, sweetspot %, runs gained from swings in the heart of the zone, flyball %, and linedrive % to create 
a power score for each hitter, scaled from 0-100.
I incorporated weights for each based on their relevance in describing a hitter's power.
Using sweetspot %, in zone contact %, whiff %, K %, and runs gained from swings at pitches in the shadow zone, I created a contact score also scaled from 0-100.
I used similar weights for all of the contact score measures, with negative weights for K% and whiff %.
Using runs lost from swinging at chase pitches, out of zone swing %, and runs gained from taking pitches in the chase zone, I created a discipline score that is scaled from 0-100.
Before calculating a composite score, I added penalties for hitters with low contact and discipline scores. 
The composite score weighs power score the highest, at 0.5, contact score the next most important at 0.333, and discipline score at 0.167.

I believe that this model does a good job ranking hitters beccause it looks at hitters through three different lenses, discerning what a hitter does best and where their production 
comes from. The importance of hitter qualities ranks power the highest, so hitters with the highest power are recognized, but are penalized when their contact and discipline are too low.

My creation of this model template not only shows some of the work that I do for Pelotero, but also the level of analysis that I can bring to an MLB Organization.
