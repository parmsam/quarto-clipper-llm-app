# quarto-clipper-llm-app

This is a Shiny for Python app that uses Beautiful Soup to scrap a webpage then the OpenAI API to generate a Quarto document. You can choose from a variety of output types including an HTML document, PDF, RevealJS slides, flashcards, and quiz questions.

It will summarize the webpage text and generate flashcards or quiz questions in your Quarto file, if you pick those options.

## Setup

The app expects that you have an OpenAI API key that you can paste into the input box. You can get one by visting the [OpenAI API quickstart page](https://platform.openai.com/docs/quickstart/).

## Dependencies

You will need my [quarto-flashcards](https://github.com/parmsam/quarto-flashcards/) and  [quarto-quiz](https://github.com/parmsam/quarto-quiz) extension in your Quarto project if you want to render out the flashcards or quiz questions in Quarto.