# AI Royale - Creating Bots for Head to Head Competition in Pong!

Our inspiration come from coding competitions/challenges being very one sided. We're all given a coding problem and the person with the fastest/most optimal solution wins. However, there's a real lack of satisfaction and competition when it comes to these competitions. Our solution to this was to create an online competition platform where individuals just plug their logic and play against other people's bots to score high on the leaderboard.

## Our Inspiration
The typical coding competition involves algorithmic challenges on various coding platforms. The fastest and the most efficient are determined to be the best through various metrics. But we wanted to create **a platform to duel code in a real-time head-to-head battle.** 

## What's AI Royale?
AI Royale is a streamlined platform that makes it easy for any programmer to duel their bots against other bots. We want to ensure every developer that wants to create and compete their algorithms against others can do so through our seamless interface. 

- **Connecting** the bots
- Creating a **standardized environment** to compete in
- **Spectating **the battle in real-time. 

## How we built it
- **User Interfaces:** HTML / CSS / Native JavaScript
- **Backend Logic:** Flask (Python Microframework) 
- **Data Storage:** Redis
- **Task Runner:** Python
- **Game Engine:** Python
- **User's Bot Servers:** Standard Library APIs

We built this project using using a Flask web server for the backend; vanilla JavaScript and Boostrap on the frontend; Redis for the datastore; Python for a task runner; Python for the game engine; and [Standard Library](https://stdlib.com/) to host user's bots and edit code in the broswer.

A stateless version of Pong was created and individual games are managed by individually calculating the next state given the previous state and the bots' inputs. We also created a template on [Standard Library](https://stdlib.com/) for hosting bots to make it seemless for users to make live bots for multiplayer.

## Challenges we ran into
- **Latency Issues:** The latency of communication between the Standard Library APIs / Backend / User Interfaces. 
- **Architecture Design:** The team had no experience developing and deploying backend systems. We had to continuously troubleshoot throughout the event and understand the discrepancies while integrating the various components of the project. 
- **Game Engine Development:** Writing a game engine from scratch without graphics was challenging in the early stages of development. 

## Accomplishments that we're proud of
- All of it. 

## What we learned
- How to use **redis** as a game state storage system.
- How to **write stateless games.*
- How to use **function as a service.** _"Yo STDLib is sick" _
- How to **survive** after 8 cans of Red Bull. 
- How to design and create a **multiplayer architecture.**


## What's next for AI Royale?
- Deploy our services to gather users 
- Win Hack Western
