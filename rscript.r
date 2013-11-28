
###------------------------ BUSINESS LOCATIONS ON MAP
install.packages('maps')
install.packages('mapdata')

train <- read.csv('data/yelp_training_set_business.json.csv', header=T, sep=',')
p <- NULL
p <- ggplot()
p <- p + geom_polygon( data=all_states, aes(x=long, y=lat, group=group),colour="white", fill="grey47" )
p
p <- p + geom_point( data=train, aes(x=longitude, y=latitude, size=stars), color="coral1") + scale_size(name="Stars")
p

states <- subset(all_states, region %in% c( "arizona", "new mexico", "california", "nevada", "utah"))
p <- NULL
p <- ggplot()
p <- p + geom_polygon( data=states, aes(x=long, y=lat, group=group, label=region, color=region),colour="white", fill="grey40")
p <- p + geom_point( data=train, aes(x=longitude, y=latitude,  hjust=0.5, vjust=-0.5), color="red", size=4)
p

###----------------------- BUSINESSES PER CITY
business <- read.csv('data/yelp_training_set_business.json.csv', header=T, sep=',')

#Top 15 cities in terms of businesses

df <- NULL
rbind(df,data.frame(name="Phoenix",count=4154))->df
rbind(df,data.frame(name="Scottsdale",count=2024))->df
rbind(df,data.frame(name="Tempe",count=1153))->df
rbind(df,data.frame(name="Mesa",count=898))->df
rbind(df,data.frame(name="Chandler",count=865))->df
rbind(df,data.frame(name="Glendale",count=610))->df
rbind(df,data.frame(name="Gilbert",count=439))->df
rbind(df,data.frame(name="Peoria",count=267))->df
rbind(df,data.frame(name="Surprise",count=161))->df
rbind(df,data.frame(name="Avondale",count=129))->df
rbind(df,data.frame(name="Goodyear",count=125))->df
rbind(df,data.frame(name="Queen Creek",count=78))->df
rbind(df,data.frame(name="Cave Creek",count=65))->df
rbind(df,data.frame(name="Paradise Valley",count=57))->df
rbind(df,data.frame(name="Casa Grande",count=48))->df

barplot(df$count, main="Top cities with the most no of businesses", horiz=TRUE, col=c("cadetblue", "coral", "yellow","lightpink", "azure", "lightgreen", "grey", "darkseagreen1", "khaki1"), names.arg=df$name, cex.names=0.7, las=1)

###----------------------- REVIEWS PER YEAR
train <- read.csv('data/yelp_training_set_review.json.csv.csv', header=T, sep=',')
m <- ggplot(train, aes(x=train$date))
m + geom_histogram()

ReviewDates = as.Date(train$date)
hist(ReviewDates, "years", format="%Y", col='lightgreen', border="grey", breaks=10, xlab="Reviews per Year", freq=T)

###----------------------- STARS FREQUENCY
reviews <- read.csv('data/yelp_training_set_review.json.csv.csv', header=T, sep=',')
hist(reviews$stars, "Stars", col='lightskyblue', border="grey", xlab="star ratings", freq=T, breaks=20)

###-----------------------
### From MongoDB

# db.review.count() - 229907
# db.business.count() - 11537
# db.user.count() - 43873
# db.checkin.count() - 8282

# db.review.count() - 22956
# db.business.count() - 1205
# db.user.count() - 5105
# db.checkin.count() - 734

#DATASET COUNTS

df <- NULL
rbind(df,data.frame(name="business",count=11537))->df
rbind(df,data.frame(name="checkin",count=8282))->df
rbind(df,data.frame(name="user",count=43873))->df
rbind(df,data.frame(name="review",count=229907))->df

barplot(df$count, main="Dataset Sizes", horiz=TRUE, names.arg=c("Business", "Checkin", "User", "Review"), cex.names=0.8,col=c("lightblue", "mistyrose", "lightcyan","lavender", "cornsilk"))

#! using ggplot2 for the same bar chart
ggplot(df, aes(x=name, y=count)) +
+ geom_bar(stat="identity", fill="white", colour="darkgreen")


###--------------------------
YELP SORT 
We use automated software developed by our engineers to recommend reviews from the Yelp community.
The software looks at dozens of different signals, including various measures of quality, reliability, and activity on Yelp.
Most of all, however, it’s looking for people who are intrinsically motivated to share the wide range of rich and detailed experiences they have every day with local businesses.
