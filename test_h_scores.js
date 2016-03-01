use sports
db.nba16.aggregate([{"$match": {"team": "chi"}}, 
						 {"$match": {"h_a": "vs"}},
						 {"$group": {"_id": {"scores": "$h_a"}, 
						 "chi": {"$push": "$s"} }}
						 ])

