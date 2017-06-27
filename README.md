# ![](https://ga-dash.s3.amazonaws.com/production/assets/logo-9f88ae6c9c3871690e33280fcf557f33.png) BeerMe - Quick 2 Day Project for DSI at General Assembly

BeerMe came out of my own lacking knowledge of beer and a desire to use data to overcome that. The data is approximately 3 million reviews of beer from the website RateBeer.com. I used Natural Language Processing (NLP) on those reviews to find which beers were described in the most similar ways. My end goal was to create an easy to use user experience that combined data science and web development.

<br>BeerMe takes as input three things; a beer that the user already likes, a popularity floor, and the maximum number of results they want back. It then filters the database to find the 150 beers most similar to the input (150 may sound like a lot but the data is for over 110 thousand beers). It then limits those 150 to only ones over the popularity floor. The popularity is determined by how many reviews there are for each particular beer. Last is the maximum results filter, there to impose a limit on the number of results, in the case of a very popular beer having way too many suggestions to be useful.

<br>Returned to the user is a list of beers and their ABVs for them to hopefully enjoy.
