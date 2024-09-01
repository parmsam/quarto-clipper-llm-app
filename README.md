# quarto-clipper-llm-app

This is a Shiny for Python app that uses Beautiful Soup to scrap a webpage then the OpenAI API to generate a Quarto document. You can choose from a variety of output types including an HTML document, PDF, RevealJS slides, flashcards, and quiz questions.

It will summarize the webpage text and generate flashcards or quiz questions in your Quarto file, if you pick those options.

It can also read PDF files and generate a Quarto document from the text in the PDF.

## Setup

The app expects that you have an OpenAI API key that you can paste into the input box. You can get one by visting the OpenAI API [quickstart page](https://platform.openai.com/docs/quickstart/).

## Accessing the app

You can clone this repo and run the app locally by run the app locally or access the app via [Connect Cloud](https://connect.posit.cloud/) at the website link in the repository details (under "About"). You may need to create a Connect Cloud account to access the app.

## Dependencies

After downloading the Quarto file you generate, if you want to render out the flashcards or quiz file using Quarto, you'll need my [quarto-flashcards](https://github.com/parmsam/quarto-flashcards/) and  [quarto-quiz](https://github.com/parmsam/quarto-quiz) extension in your Quarto project.

## Adding templates for more output types

If you want to add more output types, you can specify more templates in the quarto_templates dictionary object in the `app.py` file. 

You can also expand the types of files that the app can read from URLs by adding more URL endswith condition logic within the server code in `app.py`.