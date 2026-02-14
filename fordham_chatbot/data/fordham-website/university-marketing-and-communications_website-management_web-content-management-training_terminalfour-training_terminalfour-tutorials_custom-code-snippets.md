https://www.fordham.edu/university-marketing-and-communications/website-management/web-content-management-training/terminalfour-training/terminalfour-tutorials/custom-code-snippets

# Custom Code Snippets

## Align Three Images Side-by-Side Inside Of Accordion Tab

In order to align multiple images inside of an accordion tab we first need to insert our images using the WYSIWYG editor and then we will open the source code and wrap our images with a custom class `<div class="image-row">`

as shown below.

<img alt="" /><img alt="" /><img alt="" />

</div>


Next, for organiztion, we will add a Code Content Type where we will insert the custom styles below that will align our images within our accordion tab.

.tabs__content-wrapper .image-row {

width: 100%;

}

.tabs__content-wrapper .image-row img {

width: 33.33%;

height: auto;

float: left;

padding-left: 2.5px;

padding-right: 2.5px;

}

</style>

## Highlighted Items Full Image

In an effort to be super flexible and accomodate any image you may want to add to your Highlighted Items content type, the default functionality is to crop or hide some areas of your image in order to keep all images, visible area an equal hight and width. Howerver, sometimes you may desire to show the full image. This can be done by creating a variant sized to 1000 x 1000 px and inserting the image into your Highlighted Items content type.

We then add a Code Content Type and paste the styles shown below.

.inner__content .cta-box__col--3 .cta-box__img {

height: auto;

}

.cta-box__img img {

object-fit: contain;

}

.cta-box__block {

margin-top: 30px;

}

</style>

## Content General Image Resize

The Content General Content Type allows images to be aligned with paragraph text. The image area is 234 x 234 px, which means your image will be scaled to fit within that area. For maximum vieability it is recommended to size your image with a variant of 1000 x 1000 px. If we add a Code Content Type and paste the styles below, our image area will now scale to 320 x 320 px.

@media only screen and (min-width: 767px) {

.general-content__img-block {

width: 320px;

height: 320px;

min-width: 30%;

max-width: 100%;

}

}

</style>


![](/media/home/commonly-used-images/classroom-and-campus-life/698A6897-copy-squashed-1000x1000.jpg)

### Image Resize Example

Vestibulum mollis condimentum arcu, a convallis dui mattis ut. Nunc efficitur, risus quis faucibus venenatis, nulla nunc placerat sapien, a interdum massa justo et tellus. Integer vehicula nunc urna, porta dictum nibh hendrerit vitae. Donec fermentum a risus id hendrerit. Pellentesque rhoncus sodales ipsum, vitae egestas ligula pellentesque vel. Phasellus nec nibh dui. Sed nunc mi, aliquet in risus ac, finibus tristique ante. Curabitur congue rutrum diam, ut tincidunt mauris commodo efficitur. Vestibulum vel elementum tortor. Maecenas ultrices, purus ut molestie varius, elit neque dignissim libero, non ullamcorper metus lectus quis elit. Maecenas id tortor dolor. Vivamus sed tempor ligula, ut molestie est. Sed sem ante, aliquet sit amet tellus in, pretium commodo urna. Duis sed felis quis neque finibus fermentum. Proin hendrerit quam sed purus rutrum, ac vestibulum libero pharetra.

## Three Column Border

The Column Content Type allows us to have content in column containers of equal height regardless of the content inside of each container. if we were to open the source code and wrap our content for example with `<div style="border: 1px solid #ccc;">`

, the border would only be applied around the specific content in that container and may differ in height from the other column content. Giving staggered borders which may not be the desired look.

We can add a Code Content Type and paste the below styles to add equal borders around all three of our columns.

.col-md-4 .general-content {

border: 1px solid #ccc;

min-height: 100%;

padding: 15px;

}

.col-md-4 .general-content p, .col-md-4 .general-content img {

margin: 0 !important;

}

@media only screen and (max-width: 767px) {

.col-md-4 {

padding: 15px 47px;

}

}

@media only screen and (min-width: 767px) and (max-width: 991px) {

.col-md-4:nth-child(1) {

padding-left: 47px;

}

.col-md-4:nth-child(3) {

padding-right: 47px;

}

}

</style>

Column 1

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis ante magna, ultrices et nunc quis, iaculis faucibus lectus. Maecenas lectus dolor, lobortis sed nisl in, mattis imperdiet lectus.

Column 2

Suspendisse semper elit arcu. Vestibulum interdum lectus ut accumsan posuere. Sed imperdiet sit amet sapien sed dignissim. Vestibulum mattis, leo vitae ornare auctor, purus ligula porta dolor, sed porttitor nulla massa quis sem. Ut bibendum felis fringilla arcu tristique, quis rhoncus metus venenatis.

Column 3

Etiam felis sapien, consectetur vel ipsum at, mattis vehicula libero. Sed euismod magna ut varius ornare.

## Remove Table Background Color

By default whenever table is inserted the rows are zebra striped. Inorder to remove the background color of the table, add a Code Content Type and paste the below styles.

table:nth-child(1) tbody tr {

background-color: #fff !important;

border: 1px solid #e7ebe7;

}

table:nth-child(1) tbody tr td {

background-color: #fff !important;

border: 1px solid #e7ebe7;

}

</style>


| Column 1 | Column 2 | Column 3 |
|---|---|---|
| cell 1 | cell 2 | cell 3 |
| cell 4 | cell 5 | cell 6 |
| cell 7 | cell 8 | cell 9 |

## Banner Button Alt Color

The Banner Button Content Type defaults to a red bar and white box with a red arrow. The styles below will change the color of the Banner Button to a gray bar and red box with a white arrow.

.header-button__block {

display: flex;

justify-content: space-between;

align-items: center;

background-color: #E7EBE7;

color: #333333 !important;

padding: 2rem;

}

.header-button__button .btn-arrow-icon {

position: relative;

width: 48px;

height: 48px;

padding: .75rem;

margin-left: 1rem;

background-color: #900128;

}

.header-button__button .btn-arrow-icon:before {

position: absolute;

content: "";

display: block;

width: 0;

height: 0;

pointer-events: none;

top: 1.05rem;

left: 45%;

border-style: solid;

border-color: rgba(144, 1, 40, 1.0);

border-left-color: #ffffff;

border-width: 7px;

}

</style>