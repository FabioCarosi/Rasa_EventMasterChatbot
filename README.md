# TicketMaster Event Chatbot

This is a university project that implements a chatbot using the Rasa framework, that answers questions about events using the TicketMaster API. The chatbot also includes integration with Telegram.

### Getting Started

To run the chatbot, you will need to have Python and Rasa installed on your machine. You will also need to create a developer account with TicketMaster to obtain an API key.

API Key must be added in the **`actions/actions.py`** file for the calls to work properly.

Once you have all the necessary dependencies installed, you can clone this repository and run the following command to train the Rasa model:

```
rasa train
```

To run the Telegram integration, you will need to create a Telegram bot and add the bot token to the **`credentials.yml`** file. Then, you can run the following command to start the Telegram bot:

```
rasa run actions
rasa run
```

You can then start a conversation with the bot on Telegram and ask it questions about events.

Otherwise, to use the chatbot from the terminal, run the commands:

```
rasa run actions
rasa shell
```

### Screenshots

Include here screenshots of a sample conversation with the chatbot on Telegram.

![Searching for events in a city](images\screenshot\city.png)

Searching for events in a city

![Searching events for a sports team](images\screenshot\artist.png)

Searching events for a sports team

![Searching for events for a category](images\screenshot\category.png)

Searching for events for a category

![Get information about an event](images\screenshot\info.png)

Get information about an event

![Searching events for an artist in a country](images\screenshot\artist_county.png)

Searching events for an artist in a country

![Help request](images\screenshot\help.png)

Help request

![Search without results](images\screenshot\no_events.png)

Search without results

## **Built With**

- **[Rasa](https://rasa.com/)** - The open-source conversational AI framework used
- **[TicketMaster API](https://developer.ticketmaster.com/)** - Used to retrieve event information
- **[Telegram](https://telegram.org/)** - Used for the chatbot's messaging platform
