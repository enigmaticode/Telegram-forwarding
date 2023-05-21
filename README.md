# Telegram-forwarding
Forwarding and editing messages from telegram chat, with or without forwarding protection

--------------

Code 'forwardingEdit.py' description:

- The main function is to automatically forward messages that are written in a specific chat (target), to another chat. Both at our choice (to retrieve chat IDs: getNameID.py).
  In addition to forwarding messages, it also takes care of editing them. If messages are changed in the target chat, they will automatically also be changed in the destination chat;
- It is possible to set the number of initial messages you wish to send, then retrieve those that were inputted into the target chat before this code was started.
  Important: At the first run the number of messages you wish to monitor must be present in the chat, otherwise the code will fail;
- It is possible to indicate the number of messages to be monitored, for editing, in the target chat;
- By default, the number of messages to be monitored is set to 5;

- What can be forwarded: text messages, photos, videos, documents, audio.
- Forwarded messages don't indicate the sender.

Due to lack of time I cannot continue the development, I invite you to fork and add functions.

--------------

This code has been written for purely didactic purposes. I have no responsibility for misuse and do not encourage it.

--------------

