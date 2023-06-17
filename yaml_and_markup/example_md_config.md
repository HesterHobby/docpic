# Docpic Markdown example

## A proof of concept

This is a simple paragraph

This is another paragraph with an unordered list
* So that I can show it is unaffected
* Just because it looks cool
* In order to fill the page a bit

[docpic] # Initial URL
url: 'https://tutorialsninja.com/demo/'

# Webdriver options as per https://peter.sh/experiments/chromium-command-line-switches/
webdriver_options:
  headless: false
  window-size: "1280,1200"

# Define the steps that will be carried out by the script before the screenshot is taken.

steps:
  - type: identify
    var: search
    using: name
    selector: "search"
  - type: enter-text
    target:
      type: var-ref
      var-name: search
    value: "samsung"
  - type: click
    target:
      type: identify
      var: ~
      using: css
      selector: "i.fa.fa-search"
  - type: identify
    var: sortdropdown
    using: id
    selector: "input-sort"
  - type: click
    target:
      type: var-ref
      var-name: sortdropdown
  - type: select
    target:
      type: var-ref
      var-name: sortdropdown
    value: "Rating (Highest)"
  - type: click
    target:
      type: identify
      var: ~
      using: link
      selector: "Samsung Galaxy Tab 10.1"
  - type: identify
    var: quantity
    using: id
    selector: "input-quantity"
  - type: clear
    target:
      type: var-ref
      var-name: quantity
  - type: enter-text
    target:
      type: var-ref
      var-name: quantity
    value: "2"
  - type: click
    target:
      type: identify
      var: ~
      using: id
      selector: "button-cart"
  - type: identify
    var: ~
    using: css
    selector: "div.alert.alert-success.alert-dismissible"
  - type: docpic # docpic could be extended, I would like this to be able to focus on a particular element.
    outfile: "test.png" # Ideally there'd be a post-processing step that can highlight elements of interest or add text or both.
    alt-text: "A test image"
[/docpic]
**We could add an image title, if we wanted**

## Here's another section

_There is some more text here._ Just because.