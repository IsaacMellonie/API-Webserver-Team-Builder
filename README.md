# API Webserver Project
## "Pick-Up" Team Builder

### Installation and Setup

---
### R1 Problem Identification

If you’ve ever played social team sports, you’ll know how tough it can be to get everyone to communicate whether they’re available each week. There are a few reasons for this, apart from the obvious heel-draggers who will always cause team admins to pull their hair out, there’s no easy way to create and manage a team for social sports leagues. 

Some simple solutions use social media to create polls or ask for a show of hands so to speak. Then there’s the old method of starting a group chat and texting everyone days before the game. All of these solutions are cumbersome and require tedious management. They also rely on the admin to act as a repository, which can cause headaches for league administrators and other players who need to update information constantly. This app will provide a more effective solution than what is currently available.

This app aims to address the following problems:

- Promote Well-being and Health: Many trickle-down benefits will affect the players involved. One of which is the increase in socialisation and physical activity. By increasing organised sports, community involvement and socialisation, players will see an increase in health benefits.

- Organisation and Scheduling: One primary challenge in managing sports teams and leagues is organising games and schedules. The app will provide a platform for creating and managing schedules, allowing players and teams to know when and where games are taking place.

- Team Formation and Management: Assist in forming teams by allowing players to sign up, and express their skill levels, and availability. This can help in balancing teams and ensuring that each team has the required number of players.

- Player Communication: Effective communication is crucial for coordinating games. The app can facilitate communication between team admins and their players through emails for game reminders and scheduling.

- Attendance Tracking and Player Availability: Keeping track of who is attending upcoming games is vital for ensuring that games can go ahead. The app will allow players to RSVP to games and provide visibility to others who will attend.

- Scorekeeping: Tracking scores and game results is essential for maintaining league ladders. Team positions will be calculated using collected score information that will be used to formulate team placement and play-off games. It’s also useful for league organisers interested in tracking progress and performance.



---
### R2 Why is it a problem that needs solving?

The challenges associated with organising and managing pick-up sports teams and leagues are significant problems. 

- Anxiety and Depression: Even 3 and a half years after the pandemic first hit, concerns about mental health and substance abuse have been elevated. According to the World Health Organisation (June 2022), “Young people have been left vulnerable to social isolation and disconnectedness which can fuel feelings of anxiety, uncertainty and loneliness and lead to affective and behavioural problems.” Regular exercise is proven to be effective in reducing anxiety and depressive symptoms by releasing endorphins and serotonin which can improve mode.

- Health and Fitness Promotion: The physical benefits of social sports and regular exercise are also problems that need addressing. Regular exercise can help prevent and manage stroke, metabolic syndrome, high blood pressure, type 2 diabetes, depression, anxiety, many types of cancer, and arthritis.

- Build friendships through socialisation. According to the Australian Institute of Health and Welfare (2022) social contact survey (see attached), interactions have been steadily declining since 2001. The most notable drop occurred in young adults ages 15-24. The app makes it easier to find connections in competitive or non-competitive settings. Promoting inclusivity and accessibility to people who may feel nervous about joining a league.


![frequency of social interaction](./docs/freq_social_interaction.jpg)

- Time and Resources: Without a centralised system, organising games can be time-consuming and inefficient, often relying on disjointed communication methods like social media, emails, or word-of-mouth. The app streamlines this process, saving time and making it easier for players to engage in activities.

- Accessibility and Inclusivity: Many people are interested in participating in sports but face barriers in accessing organised games or teams. Democratising access to sports by making it easier for individuals of all skill levels to find and join local games, and will foster a more inclusive community.

- Centralise Data: Creating a centralised system for storing users, teams, and league data will reduce redundancies, improve data integrity, add valuable insights, and reduce running costs. By having a centralised data point, the app can effectively communicate with all users. Securing user information is simpler with centralised data as it is easier to monitor and control who has access. Adding admin privileges is one way this is accomplished.

- Player Management: Without a system to match players by position and skill level, games can become unbalanced, leading to a less enjoyable experience. An app that considers skill levels and availability ensures more balanced and enjoyable games.

- Consistency and Commitment: Spontaneous or irregular sports games can lead to low commitment levels, resulting in games being cancelled or played with insufficient participants. A dedicated platform enhances commitment by providing structured schedules and reminders.

Solving these problems is essential for making sports more accessible, enjoyable, and safe, while also promoting health, fitness, and community engagement. The Team Builder app has the potential to significantly enhance the experience of participating in local sports, making it a valuable tool for individuals and communities alike. On the other hand, it provides beneficial management for administrators who need to deal with large sets of data.


---
### R3 Why have you chosen this database system. What are the drawbacks compared to others?

I’ve chosen to use the PostgreSQL database management system for my application due to its extensibility, support for complex data types, and scalability. The app must be using a database that offers support for future expansion, upgrades and additional features. PostgreSQL offers catalogue-driven operation which provides additionally stored information in the PostgreSQL catalogue. This is important due to the app requires different data types within our tables. The app will also require different functions which PostgreSQL has extensible support for. In future, expansion will be necessary for added features such as an online socialisation aspect, and a payment system for player and team registration. Postgres can also handle large amounts of data and concurrent users efficiently, making it suitable for scalable web and mobile applications. The app will be built with the expectation of a large database of users and teams. Due to the expanding database requirements, PostgreSQL will be well-suited. 

When comparing PostgreSQL to MongoDB we find some advantages:

- Scalability: MongoDB is noted for its horizontal scalability. It can handle large volumes of data and high levels of user load by distributing data across multiple servers (sharding). While PostgreSQL has made significant improvements in scalability, it traditionally excels in vertical scaling (scaling up) rather than horizontal scaling (scaling out).

- Ease of Use for Development: Some developers find MongoDB more straightforward to use due to its JSON-like syntax, dynamic schema, and the fact that it doesn't require advanced SQL knowledge. This can speed up development in certain scenarios.

- Schema Flexibility: MongoDB is schema-less, which means you can insert data without first defining its structure. This is particularly advantageous in applications where the data structure can change over time. PostgreSQL, being a relational database, requires a predefined schema, which can make it less flexible for applications that need to accommodate rapidly evolving data structures.

- Read and Write Performance: For certain types of applications, particularly those with heavy write loads or where data is predominantly accessed through key-value pairs, MongoDB can offer better performance. Its document model can lead to faster writes and reads for specific use cases, though this depends greatly on the nature of the workload and data.

Sources

https://www.postgresql.org/docs/6.3/c3001.htm#:~:text=Postgres%20is%20extensible%20because%20its,call%20this%20the%20data%20dictionary).

https://www.sql-easy.com/learn/how-to-scale-postgresql/#:~:text=Understanding%20PostgreSQL%20and%20Its%20Scalability&text=I've%20found%20that%20one,PostgreSQL%20is%20its%20remarkable%20scalability.

---
### R4 Identify and discuss the key functionalities and benefits of an ORM

---
### R5 Document all endpoints for your API

---
### R6 An ERD for your app

![Pickup Team Builder](./docs/Pickup_Team_Builder.png)

---
### R7 Detail any third party services that your app will use

---
### R8 Describe your projects models in terms of the relationships they have with each other

---
### R9 Discuss the database relations to be implemented in your application

---
### R10 Describe the way tasks are allocated and tracked in your project

---
### References

---
References

- Australian Institute of Health and Welfare (2023). Social Isolation and Loneliness - Australian Institute of Health and Welfare. [online] Australian Institute of Health and Welfare. Available at: https://www.aihw.gov.au/reports/australias-welfare/social-isolation-and-loneliness.

- Cotten, E. (2023). The Decline of Friendships and How It’s Shaping Society. [online] Newswritingsports. Available at: https://medium.com/newswritings/the-decline-of-friendships-and-how-its-shaping-society-e87687ec15f1 [Accessed 6 Dec. 2023].  

- WHO (2022). COVID-19 pandemic triggers 25% increase in prevalence of anxiety and depression worldwide. [online] World Health Organization. Available at: https://www.who.int/news/item/02-03-2022-covid-19-pandemic-triggers-25-increase-in-prevalence-of-anxiety-and-depression-worldwide. 

- World Health Organization (2022). The impact of COVID-19 on mental health cannot be made light of. [online] www.who.int. Available at: https://www.who.int/news-room/feature-stories/detail/the-impact-of-covid-19-on-mental-health-cannot-be-made-light-of. 
‌
