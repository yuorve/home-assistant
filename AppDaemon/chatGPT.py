import appdaemon.plugins.hass.hassapi as hass
import openai
import globals

#
# ChatGPT App
#
# Simply using telegram BOT to interact with chatGPT
#

class chatGPT_api(hass.Hass):

  def initialize(self):
     openai.api_key = globals.key
     self.log("Initialization of chatGPT")
     self.listen_event(self.receive_telegram_text, 'telegram_text')
     self.listen_event(self.receive_telegram_command, 'telegram_command')
     self.log("Waiting for messages from Telegram BOT")

  def receive_telegram_text(self, event_id, payload_event, *args):
    self.log("Receiving message from Telegram BOT")
    user_id = payload_event['user_id']
    chat_id = payload_event['chat_id']
    text = payload_event['text']
    self.log(f"Telegram text: user_id: {user_id}, chat_id: {chat_id}, text: {text}")
    self.chatgpt_response(text)

  def receive_telegram_command(self, event_id, payload_event, *args):
    self.log("Receiving command from Telegram BOT")
    user_id = payload_event['user_id']
    chat_id = payload_event['chat_id']
    command = payload_event['command'].lower()
    self.log(f"Telegram Command: user_id: {user_id}, chat_id: {chat_id}, command: {command}, message: {context}")
    if command == "/new":
        self.log("Reiniciando la conversación")
        globals.messages = [globals.context]
        self.call_service("telegram_bot/send_message", message="Reiniciando la conversación con chatGPT")

  def chatgpt_response(self, text):
    globals.messages.append({"role": "user", "content": f"{text}"})
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=globals.messages)
    response_content = ''
    for choice in response.choices:
        response_content += choice.message.content    
    globals.messages.append({"role": "assistant", "content": response_content})                             
    self.call_service("telegram_bot/send_message", message=f"{response_content}")
    self.log(f"Sending response to Telegram BOT: {globals.messages}")
