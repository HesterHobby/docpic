# docpic

A selenium framework for adding screenshots to documentation.

## What is it?

docpic is a lightweight Markdown processor for adding screenshots of web apps to your markdown documentation.

## Why do I want it?

If you are maintaining markdown documentation alongside your web app, docpic will ensure the screenshots 
of different parts or states of the app are up-to-date, 
removing the overhead of having to manually update screenshots for every change in your app.  

## But I could just write my own Selenium?

You could. But, being a wrapper with a very simple config structure, docpic takes all the pain out of it. 
Do you really need to worry about where your webdriver is coming from or how you get to the selection in a 
dropdown? Plus, it takes care of all the error handling for you. It's a time saver.

## How does it work?

docpic uses simple YAML configuration to drive a series of selenium steps to get the web app into the 
desired state, and then takes a screenshot that is saved to a location specified in the config.
The config is added between [docpic]...[/docpic] tags in your markdown documents. 

After the screenshot is taken, docpic either saves a changed markdown file with the image embedded to a 
new location, or overwrites the existing YAML section with a Markdown link to the image.

## How do I call it?

docpic can be run in two ways:
* From within the IDE it can be run through `main.py` in the `docpic_py` folder. An example is set up that 
should run on all platforms.
* From the command line docpic can be run using 

  `python docpic_py/docpic.py --infile [input_file] --outfile [output_file] 
    --img-dir [output_folder]`. 

  For example, the following will run docpic on the included example yaml file and
    save the output into a folder called "assets": 
 
  `python docpic_py/docpic.py --infile ../yaml_and_markup/example_md_config.md --img-dir assets/`. 

  Note that the working directory for the process is `docpic_py`, so make sure the path to the markup folder is correct.
  Also note that if no output name is specified and the optional `--overwrite-existing` flag is not set, like in this example, the output
    markdown file will be saved in the format `out/[input_name].generated.[YYMMDD_hhmm].md` using the system date, in the working directory.

## YAML structure

The raw schema for docpic is in `schema/docpic.json`. An example working schema is in `example_config.dp.yaml`. 

In its most basic form, the config for docpic looks as follows:
* `initial-conditions`: The path to a docpic yaml which specifies initial steps.
* `url`: The initial URL that webdriver should open

  Either `url` OR `initial-conditions` must be present in the yaml.

* `webdriver-options`: Any webdriver options that you would like to add. This will accept anything from 
https://peter.sh/experiments/chromium-command-line-switches/
* `steps`: An array of steps that webdriver will follow.

Steps in docpic can be of the following `type`:
* `identify`: Identifies an element, and optionally stores it to variable.
* `var-ref`: Refers to a previously stored element variable, which can then be used for other actions.
* `click`: Click on the referenced element.
* `clear`: Clear the referenced element, e.g. a text box.
* `enter-text`: Enter text in the referenced element.
* `select`: Select text in a dropdown.
* `wait`: Wait for a number of seconds.
* `docpic`: Take a screenshot.

### Step type: `identify`
The `identify` step has various options for obtaining the element, and what to do with it next.
* `var`: Optional. The variable name that this element will be stored in.
* `using`: Required. The selector (`By` in Selenium terms) that will be used. Any of:
  * `id`: The element id.
  * `class`: The element class name.
  * `tag`: The element tag.
  * `name`: The element name.
  * `link`: The element link text.
  * `partial-link`: The element partial link text.
  * `css`: The element CSS.
  * `xpath`: XPATH reference to the element.
* `selector`: Required. The value of the selector set in `using`, e.g. the id, the name or the CSS 
reference of the element.

### Step type: `var-ref`
The `var-ref` step simply passes a variable to the calling step. Its only additional property is `var-name`, 
which is the name of the variable being passed.

### Step type: `env-var`
The `env-var` step obtains an environment variable to use, and optionally stores it in a docpic variable.
* `env-var`: Required. The name of the environment variable that is being read.
* `var`: Optional. The variable that this environment variable will be stored in.

### Step types: `click`, `enter-text`, `clear`, `select`
These action steps all follow a similar format.
* `target`: Required. The element receiving the action. This is either a `var-ref` step, or a `identify` step.
* `value`: For `enter-text` and `select` nodes only, the string being entered or selected, respectively. 
   The `enter-text` node also accepts a `var-ref` step as its value  

### Step type: `wait`
Docpic takes care of waiting for elements to be available, but sometimes it is necessary to build in a hard
wait for other reasons. `wait` has one property, `value`, which takes the wait time in seconds.

### Step type: `docpic`
The docpic step has the following properties:
* `outfile`: Required. The path of the output image.
* `alt-text`: Optional. The alternative text for the image. Use of this is strongly encouraged for accessibility.

## Command line options
When running docpic from the command line, the following options are available:
* `--infile`: Required. The location of your infile, relative to the current working directory.
* `--outfile`: Optional. Output file, relative to the current working directory. If not specified, 
`[input_name].generated.[YYMMDD_hhmm].md` will be used.
* `--img-dir`: Optional. Output folder, relative to the output folder. Defaults to `assets`.
* `--overwrite-existing`: Optional flag. When specified, this overwrites the `[docpic]..[/docpic]` 
sections in your input file.