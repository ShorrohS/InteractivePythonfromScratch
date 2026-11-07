# Lesson 01 — HTML Basics for Web Scraping

**Phase:** 10 — Web Scraping | **Time:** ~20 min

---

## Part 1: Why Learn HTML?

Web scraping means extracting data from HTML pages. To find the data you want, you need to understand HTML structure.

---

## Part 2: HTML Structure

```html
<!DOCTYPE html>
<html>
  <head>
    <title>Page Title</title>
  </head>
  <body>
    <h1 id="main-title">Heading</h1>
    <p class="intro">Paragraph text.</p>
    <a href="https://example.com">Link text</a>
    <table>
      <tr>
        <th>Name</th><th>Price</th>
      </tr>
      <tr>
        <td>Laptop</td><td>$999</td>
      </tr>
    </table>
  </body>
</html>
```

---

## Part 3: Key HTML Concepts for Scraping

### Tags
```
<p>paragraph</p>
<h1>heading 1</h1> through <h6>heading 6</h6>
<a href="url">link</a>
<img src="url" alt="text">
<div class="container">block element</div>
<span class="price">inline element</span>
<table><tr><td>table data</td></tr></table>
<ul><li>list item</li></ul>
```

### Attributes — how to target elements
```
id="main-title"      → unique identifier, use with: #main-title
class="intro"        → group identifier, use with: .intro
href="..."           → link URL
src="..."            → image/script source
data-price="19.99"   → custom data attribute
```

---

## Part 4: CSS Selectors — Finding Elements

BeautifulSoup uses CSS selectors to find elements:

```python
# By tag name
soup.find("p")              # first <p>
soup.find_all("p")          # all <p> tags

# By id
soup.find(id="main-title")  # <tag id="main-title">

# By class
soup.find("div", class_="container")
soup.find_all("span", class_="price")

# CSS selector string
soup.select("div.container")       # div with class container
soup.select("#main-title")         # element with id=main-title
soup.select("table tr td")         # td inside tr inside table
soup.select("a[href]")             # all links with href attribute
soup.select("[data-price]")        # any element with data-price
```

---

## Part 5: Inspecting HTML in a Browser

To find the right selectors:

1. Right-click on the element you want
2. Click "Inspect" or "Inspect Element"
3. The HTML for that element highlights in DevTools
4. Note the tag, id, and class attributes
5. Right-click the element in DevTools → Copy → Copy selector

---

## Next Lesson

**[Lesson 02 → Making HTTP Requests](lesson-02-requests.md)**
