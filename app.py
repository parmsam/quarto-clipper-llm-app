from shiny import App, Inputs, Outputs, Session, render, ui, reactive
from openai import OpenAI
import requests
from bs4 import BeautifulSoup
import os
import asyncio

api_key1 = os.getenv("OPENAI_API_KEY")
test_url = "https://posit.co/blog/announcing-the-2024-shiny-contest/"
model_options = ["gpt-3.5-turbo", "gpt-4o-mini", "gpt-4o",]

app_info = """
This app converts webpage content into a Quarto document using OpenAI's GPT-4o-mini model (by default). 
Enter the URL of the webpage and your OpenAI API key to get started. 
You can also select a different OpenAI model if needed. You will need my [quarto-flashcards](https://github.com/parmsam/quarto-flashcards/) and  [quarto-quiz](https://github.com/parmsam/quarto-quiz) extension depending on the output type.
"""

quarto_templates = {
    "Quarto document": """
        ---
        title: "Untitled"
        format: html
        params:
            source_url:
        ---

        ## Main Content

        Quarto enables you to weave together content and executable code into a finished document. To learn more about Quarto, visit <https://quarto.org>.

        ## Code Embedding

        Include code snippets using fenced code blocks and maintain any original formatting. Ensure all images and links are correctly referenced in the document.""",
    "Quarto quiz": """
        ---
        title: "Multiple Choice Quiz Example"
        format:
            revealjs: default
        revealjs-plugins:
        - quiz
        params:
            source_url:
        ---

        ## What is the capital of France? {.quiz-question}

        - London
        - [Paris]{.correct}
        - Berlin
        - Madrid
        
        ## What is the capital of Spain? {.quiz-question}

        - Paris
        - Berlin
        - [Madrid]{.correct}
        
        ## What is the capital of Germany? {.quiz-question}

        - Paris
        - [Berlin]{.correct}
        - Madrid
        - London
        """,
"Quarto flashcards": """
        ---
        title: "Flashcards Example"
        format:
            revealjs: default
        revealjs-plugins:
        - flashcards
        params:
            source_url:
        ---

        ## Intro

        ::: {.flashcard-front}
        This is an example of using the `flashcards` plugin in a reveal.js presentation. 

        Press the `q` key (by default) to flip a flashcard slide. You can you can override the default keybinding by setting the `flipKey` option in the YAML header. 

        You'll also see a flip button in the top right corner of the slide. You can hide this button by setting `showFlipButton: false` in the YAML header.
        :::

        :::{.flashcard-back}
        Nicely done! Let's go over some example flashcards to see how this looks.
        :::

        ## Question 1

        ::: {.flashcard-front}
        What is the capital of France?

        [![](https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/France_location_map.svg/1252px-France_location_map.svg.png?20160102094348){height=400px}](https://en.wikipedia.org/wiki/France)
        :::

        ::: {.flashcard-back}
        Paris

        ![](https://upload.wikimedia.org/wikipedia/commons/c/cf/France_and_its_region.png){height=400px}
        :::
        
        ## Question 2 {background-color="lightblue"}

        ::: {.flashcard-front}
        What is the equation to calculate Mean Squared Error (MSE)?
        :::

        ::: {.flashcard-back}
        $\frac{1}{n} \sum_{i=1}^{n} (y_i - \hat{y}_i)^2$

        where $y_i$ is the observed value and $\hat{y}_i$ is the predicted value.
        :::
        """
}


app_ui = ui.page_fluid(
    ui.layout_sidebar( 
        ui.sidebar(
            ui.input_password("api_key", "Enter your OpenAI API key:", value=api_key1),
            ui.input_select("model", "Select OpenAI model:", 
                            choices = model_options, 
                            selected = "gpt-4o-mini"),
            ui.input_text("url", "Enter webpage URL:", value = test_url),
            ui.input_select("selected_template", "Select Quarto output type:",
                            choices = list(quarto_templates.keys()),
                            selected = "Quarto document"),
            ui.input_action_button("convert", "Convert to Quarto"),
            open="always",
        ),
        ui.panel_title("Quarto Clipper"),
        ui.strong(ui.em("a webpage to quarto converter using large language models")),
        ui.markdown(app_info),
        ui.download_button("download", "Download Quarto Document"),
        ui.output_text_verbatim("quarto_output"),
    )
)

def server(input, output, session):
    quarto_content = reactive.Value("")
    llm_prompt = reactive.Value("")

    @reactive.Effect
    @reactive.event(input.convert)
    def _():
        url = input.url()
        api_key = input.api_key()
        
        if not api_key:
            ui.notification_show("Please enter your OpenAI API key.", type="error")
            return
        
        if url and api_key:
            client = OpenAI(api_key=api_key)
            # Fetch webpage content
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract text content
            text_content = soup.get_text()
            
            llm_prompt.set([
                {"role": "system", 
                "content": f"""You are a highly proficient assistant tasked with converting webpage content into a structured Quarto document.
                
                Your primary focus is to extract the main content, avoiding any irrelevant sections such as navigation bars, footers, advertisements, or any extraneous links. 
                The goal is to create a clean, well-formatted document using the Quarto format. Ensure you are adhering to the official Quarto file standard. 
                A Quarto file should start only with the Quarto metadata at the top of the file, including the title, format, and any other relevant parameters.

                The following is a reference Quarto file you should use as a basis: 
                {quarto_templates[input.selected_template()]}"""
                },
                {"role": "user", 
                "content": f"""Please convert the following webpage content into a {input.selected_template()} (.qmd) file. 
                - Extract only the main article or body content, and avoid including navigation menus, footers, sidebars, or any non-essential elements.
                - Ensure that the structure, headings, links, images, and any other relevant formatting are preserved according to Quarto standards.
                - Ensure you're adhering to the provided Quarto template structure and formatting guidelines.
                - Include the webpage URL in the Quarto metadata in the source_url parameter. 
                - Summarize information instead if it is for the flashcards or a quiz output into the main points in that format. 
                - Limit information to that which is important and relevant for a flashcard or quiz context, depending on what is picked.
                - Ensure you dont start and end the file with the typical three markdown backquotes (```) as it is not needed for Quarto.

                Webpage content: {text_content}"""}
            ])

            try:
                response = client.chat.completions.create(
                    model= input.model(),
                    messages=llm_prompt()
                )

                quarto_content.set(response.choices[0].message.content)
            except Exception as e:
                ui.notification_show(f"Error: {str(e)}", type="error")
    
    @output
    @render.text
    def quarto_output():
        if quarto_content():
            lines = quarto_content().split("\n")
            if lines[0].startswith("```") and lines[-1].startswith("```"):
                lines = lines[1:-1]
                return "\n".join(lines)
            else:
                return quarto_content()

    @output
    @render.download(
        filename=lambda: f"webpage_content_{hash(input.url())}.qmd",
    )
    async def download():
        await asyncio.sleep(0.25)
        yield quarto_content()

app = App(app_ui, server)
