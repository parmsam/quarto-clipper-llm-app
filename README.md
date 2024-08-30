# quarto-clipper-llm-app

This is a Shiny for Python app that uses Beautiful Soup to scrap a webpage then the OpenAI API to generate a Quarto document. You can choose from a variety of output types including an HTML document, PDF, RevealJS slides, flashcards, and quiz questions.

It will summarize the text and generate flashcards or quiz questions based on the webpage text, if you pick those options.

## Setup

The app expects that you have an OpenAI API key that you can paste into the input box. You can get one by visting the [OpenAI API quickstart page](https://platform.openai.com/docs/quickstart/).