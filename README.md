# AI Royale - Creating Bots for Head to Head Competition in Pong!

Our inspiration come from coding competitions/challenges being very one sided. We're all given a coding problem and the person with the fastest/most optimal solution wins. However, there's a real lack of satisfaction and competition when it comes to these competitions. Our solution to this was to create an online competition platform where individuals just plug their logic and play against other people's bots to score high on the leaderboard.

## Our Inspiration:
The typical coding competition involves algorithmic challenges on various coding platforms. The fastest and the most efficient are determined to be the best through various metrics. But we wanted to create **a platform to duel bots in a real-time head-to-head battle.**

Imagine two bot creators (ex. two students in high school) have been developing a [Pong](https://en.wikipedia.org/wiki/Pong) bot - each on their local machines. Now they want to put their bots up against each other - and the rest of the competitive bot community in a _classic multiplayer_ fashion.

The bot creators would need to **implement and deploy a web API around their bot, implement a multiplayer version of the game, use a data store to store game states, and design a user interface for creating/joining/watching competitions between bots**.

Our solution was bootstraping the bot creation process by implementing a stateless multiplayer server and created templates for developers who want to create bots. With our platform, **bot creators only need to write their bot logic** and _we take care of the rest_.

As a result, we made it so easy to use that this platform could also be used to teach everything from how to write your first line code to how to create a bot using AI.

## What's AI Royale?
AI Royale is a streamlined platform that makes it easy for any programmer to duel bots against other bots. We want to ensure every developer that wants to create and compete their algorithms against others can do so on our platform. 

- **Templates** - for creating live bots using [Standard Library](https://stdlib.com/)
- **Intuitive User Interface** - integrated [Standard Library's](https://stdlib.com/) IDE, [code](https://code.stdlib.com/), to make it easy for users to publish bots and go through tutorials without leaving our site or changing tabs
- **Tutorials** - [see here](https://imgur.com/a/Ny2NETV) - that teach everything from _the essentials of programming_ to _integrating AI into their bots_
- **Multiplayer Server (+Task Runner)** - for synchronizing game state and retrieving events from users' bots
- **Game Engine** - for _calculating the next game states_ from the previous game state and bots' event inputs
- **Game Lobby and Session System** - [see here](https://imgur.com/a/fhylPvK) and [here](https://imgur.com/a/oKjmmZY) - for  _matchmaking_ and _realtime spectating_ 

## How we built it:

![Architecuture Diagram](/airoyal-archdiagram.jpg)

- **User Interface:** HTML / CSS + Bootstrap / Native JavaScript
- **Backend:** Flask (Python Microframework) 
- **Data Store:** Redis
- **Task Runner:** Python
- **Game Engine:** Python
- **User's Bot Servers:** Standard Library API and _Sources_ functionality

We built this project using using a Flask web server for the backend; vanilla JavaScript and Boostrap on the frontend; Redis for the datastore; Python for a task runner; Python for the game engine; and [Standard Library](https://stdlib.com/) to host user's bots and edit code in the broswer.

A stateless version of Pong was created and individual games are managed by individually calculating the next state given the previous state and the bots' inputs. We also created a template on [Standard Library](https://stdlib.com/) for hosting bots to make it seemless for users to make live bots for multiplayer.
