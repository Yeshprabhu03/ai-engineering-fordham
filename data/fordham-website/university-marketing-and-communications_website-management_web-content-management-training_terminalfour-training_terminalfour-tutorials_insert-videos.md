https://www.fordham.edu/university-marketing-and-communications/website-management/web-content-management-training/terminalfour-training/terminalfour-tutorials/insert-videos

# Insert Videos

**Video files must be uploaded to a platform such as YouTube or Vimeo.** We can then access the video link or the embed code to add to web pages.

- When editing a page and viewing the "Content" tab, click "Add content" in the upper right
- Filter the list for "Video" and select the "Video" content type
- Complete the following mandatory fields:
- Name
- Location of Content
- Embed URL (YouTube or Vimeo)
- YouTube Embed Example: https://www.youtube.com/embed/auGAapIq_mY
- Vimeo Embed Example: https://player.vimeo.com/video/363657062

- Heading
- Description

- Click "Save changes" at the bottom of the page

## Responsive iFrame (YouTube)

### Embed responsive video into the Tabs content type

Page example: [GSE Administration and Staff](/graduate-school-of-education/about/administration-and-staff/)

To embed a YouTube video into a content type other than the "Video" content type (eg. Content - General, Accordion, Tabs, etc.)

- Access the video at YouTube.com
- Click on the "share" button
- Select "Embed" from the list of share options.
- Copy all the HTML code

![YouTube share options](/media/review/sample-site/site-assets/images/Screen-Shot-2022-04-19-at-12.27.15-PM.png)

![YouTube Embed options](/media/review/sample-site/site-assets/images/Screen-Shot-2022-04-19-at-12.25.17-PM.png)

![CSS Snippet for responsive iFrame](/media/review/sample-site/site-assets/images/Screen-Shot-2022-04-19-at-2.52.43-PM.png)


- From the Tools dropdown select "Source code"
- Pasted the YouTube embed code
- Wrap the iframe inside of a <div> tag and add the class name "iframe-container"
- Copy/paste the CSS styles below
- Save changes

## CSS Code:

<style>

.iframe-container {


position: relative;

width: 100%;

padding-bottom: 56.25%;

height: 0;

}.iframe-container iframe {


position: absolute;

top:0;

left: 0;

width: 100%;

height: 100%;

}</style>