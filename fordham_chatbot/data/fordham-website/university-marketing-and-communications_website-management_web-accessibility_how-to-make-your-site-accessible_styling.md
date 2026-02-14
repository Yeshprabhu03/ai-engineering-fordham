https://www.fordham.edu/university-marketing-and-communications/website-management/web-accessibility/how-to-make-your-site-accessible/styling

# Accessible Styling

## Text Layout

Text should be left aligned on web. Text layout can affect the way some people may read on the web. Please do not center text on the web as it may be difficult for some readers.

## Headings

**Heading tags** dictate how screenreaders scan a web page. If tags are out of order, it makes it hard for those using screenreaders to follow the content.

- Do not use the Heading 1 <h1> tag. The
**title of the page in an H1 tag**, adding another one will compete with the page title **The first heading manually added on a page must be a <h2>**. Do not start with an <h3> <h4> etc**Headings must be in chronological order**in either direction but**do not skip a tag**(i.e. <h1> <h2> <h3 <h2> or <h2> <h3> <h3> <h4> <h3>)**Do not bold headings**. It is best to one type of styling: heading, bold, italics, body-lead-font, etc.

## Bold, Italics, and Body-lead-font

To bring attention to specific words or phrases in your content, you can use the formatting buttons to select either bold or italicize. This will automatically add the **<strong>** or *<em>* tags to the content (keyboard shortcuts also work). If coding in HTML, please use **<strong>** and *<em>* tags to assist screen readers.

If **Heading tags are too large**, you can use body-lead-font which is located under Format > Formats > Custom Formats[Sample body-lead-font](/give/ways-to-give/womens-philanthropy/fordham-womens-summit-philanthropy--empowerment--change/pioneering-women-in-philanthropy-at-fordham/).

## Underlining on the Web

When text is hyperlinked, it is automatically underlined. Content on the web should never be manually underlined because it gives the appearance of a broken link. To bring attention to specific words or phrases in your content, please either bold or italicize them using **<strong>** or *<em>* tags. In Jadu, the bold and italicize buttons will use the correct formatting tags.

## Font Tags

The <font> tag should never be used when coding in HTML since stylistic formatting should now be handled within CSS. For the Fordham website, we have a CSS style sheet in place that defines how each tag will be displayed. **Do not** use the <font> tag or other styling because it will override the CSS style sheet.

## Colors and Contrast

The contrast between the color of the text and the background it is overlayed on should be at least 7:1 for normal text and 4.5:1 on large text. With the CSS style sheet in place, this should not be an issue unless the text is being altered with the <font> tag. As previously mentioned, the <font> tag should never be used due to the conflict with the CSS style sheet.

Learn more about web best practices and [Tips and Tricks](/university-marketing-and-communications/website-management/web-content-management-training/terminalfour-training/tips-and-tricks/).