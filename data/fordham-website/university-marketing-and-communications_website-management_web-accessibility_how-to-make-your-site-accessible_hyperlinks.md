https://www.fordham.edu/university-marketing-and-communications/website-management/web-accessibility/how-to-make-your-site-accessible/hyperlinks

# Accessible Hyperlinks

## Insufficient Link Text

Insufficient link text or non-descriptive link and button text is very important. “Read more” or “Click here” does not make the link destination apparent to people with visual impairments who use screen readers to navigate the web.

We need:

- “Learn more” to say “Learn more about the Center for Medieval Studies”
- “Read more” to say “Read more about our sustainability initiatives”
- “Register” to say “Register for the December 18 Information Session”

[Learn more about accessible links](https://www.w3.org/WAI/older-users/developing/#links).

## Link Without Text

When adding a link make sure to just highlight the word(s) you want linked, and not the space before or after the word(s). If you accidentally highlight the empty space, it will add the link twice and we will receive an accessibility error stating that there is a link without alt text. You can review the source code to make sure the link appears only once.

## Indistinguishable Link Text

When hyperlinking text that is repeated throughout the page, it is important to ensure that it leads to the same page. For example, if you wanted to promote an event, the hyperlinked text "View Event Details" should always lead to Event A. If you are planning to list multiple items that will use the same generic text but with different destination pages, you need to specify in the text where it will be going.

For example, if your events page mentions Events A, B, and C, and you want to have additional details for each event on different pages, the hyperlinked text will need to be "View Event A Details", "View Event B Details", and "View Event C Details".