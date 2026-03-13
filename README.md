SafeType chat 

SafeType is a smart keyboard prototype designed to reduce toxic communication online. It detects potentially harmful or abusive language while the user is typing and gently encourages them to rethink their message before sending it.

Problem

Online conversations often become toxic, especially on social media and messaging platforms. Most moderation systems act after a message is posted, when the harm may already be done.

Solution

SafeType works like a normal keyboard but includes real-time toxicity detection.
If harmful language is detected while typing, the keyboard shows a warning message and suggests more respectful alternatives, helping users rethink their message before sending it.

Features

Real-time toxic word detection

Warning popup for harmful messages

Rephrase suggestions

Simple keyboard interface

Privacy-friendly (no message storage)

Tech Stack
| Layer              | Technology                          | Purpose                                                        |
| ------------------ | ----------------------------------- | -------------------------------------------------------------- |
| **Frontend UI**    | HTML5, CSS3, JavaScript (Vanilla)   | Builds the chat interface, keyboard UI, popups, and animations |
| **Real-time Chat** | Socket.IO (Node.js)                 | Enables live group messaging between users                     |
| **AI Detection**   | Hugging Face Transformers + PyTorch | Performs toxicity and tone analysis on typed messages          |
| **API Server**     | Flask (Python)                      | Provides the `/analyze-text` endpoint for message analysis     |
| **Persistence**    | Browser `localStorage`              | Stores user actions such as "Send Anyway" strikes              |
| **Build Tools**    | Rust + Visual C++ Build Tools       | Required for tokenizer dependencies during setup               |


Future Improvements

Multi-language support

Context-aware message suggestions

Goal

To promote healthier and more respectful digital communication by preventing harmful messages before they are sent.

Contributors

Arpita Singh,
Afreen Khan ,
Drishti Shina,
Kriti Mishra,
Jiya Sharma
