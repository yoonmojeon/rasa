# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []
# actions.py

import mysql.connector
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

# actions.py

from typing import Text, List, Dict, Any

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet


class ActionStoreLeague(Action):
    def name(self) -> Text:
        return "action_store_league"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        league = next(tracker.get_latest_entity_values("league"), None)
        dispatcher.utter_template("utter_preference_league", tracker, league=league)
        return [SlotSet("league", league)] if league else []

class ActionStorePosition(Action):
    def name(self) -> Text:
        return "action_store_position"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        position = next(tracker.get_latest_entity_values("position"), None)
        dispatcher.utter_template("utter_preference_position", tracker, position=position)
        return [SlotSet("position", position)] if position else []


class ActionStoreStyle(Action):
    def name(self) -> Text:
        return "action_store_style"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        style = next(tracker.get_latest_entity_values("style"), None)
        dispatcher.utter_template("utter_preference_style", tracker, style=style)
        return [SlotSet("style", style)] if style else []


class ActionStoreStrength(Action):
    def name(self) -> Text:
        return "action_store_strength"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        strength = next(tracker.get_latest_entity_values("strength"), None)
        dispatcher.utter_template("utter_preference_strength", tracker, strength=strength)
        return [SlotSet("strength", strength)] if strength else []

class ActionStoreFormation(Action):
    def name(self) -> Text:
        return "action_store_formation"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        formation = next(tracker.get_latest_entity_values("formation"), None)
        dispatcher.utter_template("utter_preference_formation", tracker, formation=formation)
        return [SlotSet("formation", formation)] if formation else []




import mysql.connector
from typing import Any, List, Dict, Text
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet


class ActionCheckSlots(Action):
    def name(self) -> Text:
        return "action_check_slots"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Get values from slots
        league = tracker.get_slot("league")
        position = tracker.get_slot("position")
        style = tracker.get_slot("style")
        strength = tracker.get_slot("strength")
        name = tracker.get_slot("name")

        # Debug: Print current slots
        current_slots = {
            "league": league,
            "position": position,
            "style": style,
            "strength": strength,
            "name": name
        }
        print(f"Current slots: {current_slots}")

        return []


class ActionRecommendPlayer(Action):
    def name(self) -> Text:
        return "action_recommend_player"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        # Get values from slots
        league = tracker.get_slot("league")
        position = tracker.get_slot("position")
        style = tracker.get_slot("style")
        strength = tracker.get_slot("strength")

        # Connect to MySQL database
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="0000",
            database="fifa"
        )

        # Create a cursor object
        cursor = connection.cursor()

        # Query to retrieve player information based on slots
        query = "SELECT name FROM player WHERE strength = %s"
        cursor.execute(query, (strength, ))

        # Fetch the result
        result = cursor.fetchall()

        # Close the cursor and connection
        cursor.close()
        connection.close()

        # Check if any players were found
        if result:
            # Assuming you have a column named "player_name" in your player_table
            player_names = [row[0] for row in result]
            players_str = ", ".join(player_names)
            dispatcher.utter_message(f"I recommend the following players: {players_str}")
        else:
            dispatcher.utter_message("Sorry, I couldn't find a player that matches your criteria.")

        return []

class ActionRecommendCoach(Action):
    def name(self) -> Text:
        return "action_recommend_coach"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        # Get values from slots
        formation = tracker.get_slot("formation")

        # Connect to MySQL database
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="0000",
            database="fifa"
        )

        # Create a cursor object
        cursor = connection.cursor()

        # Query to retrieve player information based on slots
        query = "SELECT name FROM coach WHERE formation = %s"
        cursor.execute(query, (formation, ))


        # Fetch the result
        result = cursor.fetchall()

        # Close the cursor and connection
        cursor.close()
        connection.close()

        # Check if any players were found
        if result:
            # Assuming you have a column named "player_name" in your player_table
            coach_names = [row[0] for row in result]
            coach_str = ", ".join(coach_names)
            dispatcher.utter_message(f"I recommend the following coach: {coach_names}")
        else:
            dispatcher.utter_message("Sorry, I couldn't find a coach that matches your criteria.")

        return []


class ActionFetchAllPlayers(Action):
    def name(self) -> Text:
        return "action_fetch_all_players"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        # Connect to MySQL database
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="0000",
            database="fifa"
        )

        # Create a cursor object
        cursor = connection.cursor()

        # Query to retrieve all player names
        query = "SELECT name FROM player"
        cursor.execute(query)

        # Fetch the result
        result = cursor.fetchall()

        # Close the cursor and connection
        cursor.close()
        connection.close()

        # Check if any players were found
        if result:
            # Assuming you have a column named "name" in your player_table
            player_names = [row[0] for row in result]
            players_str = ", ".join(player_names)
            dispatcher.utter_message(f"Here are all the players: {players_str}")
        else:
            dispatcher.utter_message("No players found in the database.")

        return []

class ActionCheckPotential(Action):
    def name(self) -> Text:
        return "action_check_potential"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        # Get values from slots
        name = tracker.get_slot("name")

        # Connect to MySQL database
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="0000",
            database="fifa"
        )

        # Create a cursor object
        cursor = connection.cursor()

        # Query to retrieve player information based on slots
        query = "SELECT potential FROM player WHERE name = %s"
        cursor.execute(query, (name, ))

        # Fetch the result
        result = cursor.fetchall()

        # Close the cursor and connection
        cursor.close()
        connection.close()
        
        # Check if any players were found
        if result:
            potential = result[0][0]
            dispatcher.utter_message(f"Potential: {potential}")
            dispatcher.utter_message("Over 70, we say high potential")
        else:
            dispatcher.utter_message("Sorry, I couldn't find a player that matches your criteria.")

        return []