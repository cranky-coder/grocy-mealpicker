# grocy-mealpicker

This is a down and dirty script, maybe someone would like to contribute to it. 

This is a python script that connects to your grocy instance.  

I have a few rules in play here.  

1.  you need to have recipes added and tagged as "Dinner"
2.  In this code, the recipe for pizza is auto added automatically on friday since friday is pizza friday in our house.
3.  If we plan to go out to eat and know the restaurant i create a recipe for the restaurant, and tag it as a restaurant, this script filters those out.
4.  The script identifies how many days over the next week i don't have something already planned for dinner.  So if you have plans to go out to eat, or need a specific meal on a certain day you can add it ahead of time and it will compensate.  
5.  The script then spits out a list of potential meals

The ordering of the meals was something I was trying to be fancy with as I wanted it to be a little more fluid but not keep telling me the same thing if i just had it.  So i tried to do some weighted random here.  If it's a meal that has recently been added, then it has a higher chance of being picked, but ANY meal can come up at any times, it's just less likely the more recent you have had it.  

This is definitely not perfect, but it was something I did to help make picking the meals for grocery shopping easier.  The last an final step if you decide you want to go into it is to use the same code that sets the pizza to friday to have it iterate through your days and auto add a meal.  

