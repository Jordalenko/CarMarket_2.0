Go back to [README.md](/README.md)

# Testing
- [Code Validation](#code-validation)
    - [HTML](#html)
    - [CSS](#css)
    - [JavaScript](#JavaScript)
    - [Python](#python)
- [Responsiveness](#Responsiveness)
- [Browser Compatibility](#browser-compatibility)
- [Lighthouse](#Lighthouse)
- [Manual Testing](#manual-testing)
- [User Story Testing](#user-story-testing)

## Code Validation
### HTML
|Page|Validator|Result|
| --- | --- | --- |
| Home |<mark>PASS<mark> |
| Listings | <mark>PASS<mark> |
| Single Listing | <mark>PASS<mark> |
| Create And Edit Listing | <mark>PASS<mark> |
| My Profile | <mark>PASS<mark> |
| My Listings | <mark>PASS<mark> |
| My Favourites | <mark>PASS<mark> |
| User Account | <mark>PASS<mark> |
| User Listings | <mark>PASS<mark> |
| Edit Profile | <mark>PASS<mark> |
| Delete Profile Conf| <mark>PASS<mark> |
| Profile Deleted | <mark>PASS<mark> |
| Delete Listing Conf | <mark>PASS<mark> |
| Remove Favourite | <mark>PASS<mark> |
| Log In | <mark>PASS<mark> |
| Sign Up | <mark>PASS<mark> |
| Sign Out Conf | <mark>PASS<mark> |
| Reset Password Enter email | <mark>PASS<mark> |
| Reset Password email sent | <mark>PASS<mark> |
| Reset Password Enter password | <mark>PASS<mark> |
| Reset Password Complete | <mark>PASS<mark> |
| Error pages | <mark>PASS<mark> |

### CSS
Test Results CSS  <mark>PASS<mark> 

### JavaScript
1. listing_form.js <mark>PASS<mark> 

2. search.js <mark>PASS<mark>

### Python
1. Api app
- urls.py <mark>PASS<mark>

- views.py <mark>PASS<mark>

2. Carmarket app
- settings.py <mark>PASS<mark> 

- urls.py <mark>PASS<mark>

- views.py <mark>PASS<mark>

3. Listings
- admin.py <mark>PASS<mark>

- models.py <mark>PASS<mark>

- urls.py <mark>PASS<mark>

- views.py <mark>PASS<mark>

4. Users
- admin.py <mark>PASS<mark>

- forms.py <mark>PASS<mark>

- models.py <mark>PASS<mark>

- urls.py <mark>PASS<mark>

- views.py <mark>PASS<mark>


## Responsiveness
During development each page was tested using dev tools in Google Chrome. The strategy involved ensuring that every page would adapt to various screen sizes beyond a width of 320px, as opposed to relying on fixed device-specific widths.
Further testing was done on mobile to confirm all is working as expected.

|Device|Screen Size|Pass/Fail|Comment|
| --- | --- | --- | ---|
| Iphone 4 | 320x480 |  | All sections are displayed correctly. All features work|
| Iphone 12 Pro | 390x844 |  | All sections are displayed correctly. All features work|
| Samsung Galaxy s20U | 412x915 |  | All sections are displayed correctly. All features work|
| Galaxy Tab S4 | 712x1138|  | All sections are displayed correctly. All features work|
| Nest Hub | 1024x600 |  | All sections are displayed correctly. All features work|


## Browser Compatibility


|Browser|Result|Pass/Fail|Notes|
| --- | --- | --- | ---|
| Google Chrome | All pages, load as expected. All features work as expected |  | --- |
| Firefox | All pages, load as expected. All features work as expected |  | --- |
| Edge | All pages, load as expected. All features work as expected | 

## Lighthouse

|Page|Validator|Result|
| --- | --- | --- |
| Home Desktop | <mark>PASS<mark> |
| Home Mobile | <mark>PASS<mark> |
| Listings Desktop| <mark>PASS<mark> |
| Listings Mobile| <mark>PASS<mark> |
| Single Listing Desktop| <mark>PASS<mark> |
| Single Listing Mobile| <mark>PASS<mark> |
| Create Listing Desktop| <mark>PASS<mark> |
| Create Listing Mobile| <mark>PASS<mark> |
| Edit Listing Desktop| <mark>PASS<mark> |
| Edit Listing Mobile| <mark>PASS<mark> |
| My Profile Desktop| <mark>PASS<mark> |
| My Profile Mobile| <mark>PASS<mark> |
| My Listings Desktop| <mark>PASS<mark> |
| My Listings Mobile| <mark>PASS<mark> |
| User Account Desktop| <mark>PASS<mark> |
| User Account Mobile| <mark>PASS<mark> |
| User Listings Desktop | <mark>PASS<mark> |
| User Listings Mobile | <mark>PASS<mark> |
| Edit Profile Desktop| <mark>PASS<mark> |
| Edit Profile Mobile| <mark>PASS<mark> |
| Delete Profile Desktop| <mark>PASS<mark> |
| Delete Profile Mobile| <mark>PASS<mark> |
| Delete Listing Conf Desktop| <mark>PASS<mark> |
| Delete Listing Conf Mobile| <mark>PASS<mark> |
| Log In Desktop| <mark>PASS<mark> |
| Log In Mobile| <mark>PASS<mark> |
| Sign Up Desktop| <mark>PASS<mark> |
| Sign Up Mobile| <mark>PASS<mark> |
| Sign Out Conf Desktop| <mark>PASS<mark> |
| Sign Out Conf Mobile| <mark>PASS<mark> |
| Reset Password Enter email Desktop| <mark>PASS<mark> |
| Reset Password Enter email Mobile| <mark>PASS<mark> |
| Reset Password Enter password Desktop| <mark>PASS<mark> |
| Reset Password Enter password Mobile| <mark>PASS<mark> |
| Profile Deleted Success Desktop | <mark>PASS<mark> |
| Profile Deleted Success Mobile | <mark>PASS<mark> |

## Manual Testing
- Home Page 

|Section|Test Action|Expected Result|Pass/Fail|Comments|
| ---| ---| ---| ---| ---|
|Navbar|Click on logo in Navbar|Redirect to Home |Pass|Navbar present on all pages |
||Click on All Vehicles, Cars or SUV links in Navbar|Redirect to appropriate Page |Pass|Navbar present on all pages |
||Click on Trade/Sell Vehicle link in Navbar|Redirect to Create Listing Page |Pass|Navbar present on all pages |
||Click on Profile link in Navbar|Redirect to My Profile Page |Pass|Navbar present on all pages |
||Click on Log Out link in Navbar|Redirect to Home Page |Pass|Navbar present on all pages |
||Click on Login/Sign Up in Navbar|Redirect to Login/SignUp Page |Pass|Navbar present on all pages |
|Hero section|Open Search page. Ensure the hero section loads as it should|Hero section loads as it should |Pass|Home Page BG present on all pages|
|Search form|Open the Home page. Ensure the search form section loads as it should|Search form section loads as it should |Pass| |
||Click on each input field. Ensure all choices are loaded.|All input fields appear as they should. |Pass| |
||Search listings by a combination of filters. Ensure the results displayed are accurate with the search filters|All search results match the search criteria |Pass| |
||Select a max year. Ensure the min year cannot exceed the max year|All values of min year that exceed the max year are disabled |Pass| |
||Select min year. Ensure the max year cannot be less than the max year|All values of the max year that are below the min year are disabled |Pass| |
||Select max price. Ensure the min price cannot exceed the max price|All values of min price which exceed the max price are disabled |Pass| |
||Select min price. Ensure the max price cannot be less than the max price|All values of max price which are below min price are disabled |Pass| |
||Click on the search button. Ensure the user is redirected to the listings page|The user is redirected to the listings page with accurate results |Pass| |
|Recent Listings|Open the Home page. Scroll down to recent listings. Ensure the most recent listings are showing by comparing the time added stamp|The most recent listings are displayed |Pass| |
||Open the Create Listing page and create a listing. Ensure it shows up in admin's to be approved listings section |The added listing is displayed as most recent |Pass| |
|Listing Card| Click on the listing card. Ensure it redirects to the correct single listing page |When clicked each card redirects to the correct single listing page |Pass| |
|| Click on the listing card button. Ensure it redirects to the correct single listing page |When clicked each card button redirects to the correct single listing page |Pass| |
|| Go to the Create Listings page and create a new listing. Ensure the details displayed on the card are accurate |The information displayed on the card is accurate |Pass| |
|Pagination| Click on all of the links in the pagination. Ensure they redirect to the appropriate page. |All links redirect to the correct page. |Pass| |
|Pagination| Use the search form to search listings. Click on all of the links in the pagination. Ensure they redirect to the appropriate page displaying only the search results. |All links redirect to the correct page displaying the correct results. |Pass| |

- Listings Page 

|Section|Test Action|Expected Result|Pass/Fail|Comments|
| ---| ---| ---| ---| ---|
|search form|Click on all of the links and dropdowns|Links open and dropdowns select as expected|Pass|Tested on home page|
|listing card|Click on all of the links|Links open as expected|Pass|Tested on search page|
|Pagination| Click on all of the links in the pagination. Ensure they redirect to the appropriate page. |All links redirect to the correct page. |Pass| |
|Pagination| Use the search form to search listings. Click on all of the links in the pagination. Ensure they redirect to the appropriate page displaying only the search results. |All links redirect to the correct page displaying the correct results. |Pass| |

- Single Listing Page 

|Section|Test Action|Expected Result|Pass/Fail|Comments|
| ---| ---| ---| ---| ---|
| Back button|Open the single listing page. Click on the back button. Ensure it sends you back to the previous page|When clicked the button brings you back to the previous page.|Pass||
|back button|Open the single listing page and the listing to favourites. Click on the back button. Ensure it sends you back to the previous page|When clicked the button does not bring you back to the previous page due to the fact the page reloaded|Pass|
|Images section|Click on the main image. Ensure it opens using Lightbox. Ensure arrows appear to navigate through the images|When clicked the images open using lightbox. Arrows appear on the sides and allow you to navigate through the images|Pass||
|Listing details|Ensure all the car specs are accurate with the details used when creating the listing. Ensure all icons display as they should|All icons display as they should, and the information is accurate.|Pass||
|Description|Scroll to the description section. Ensure the accurate description is displayed |The accurate description is displayed|Pass||

- Create listing Page 

|Section|Test Action|Expected Result|Pass/Fail|Comments|
| ---| ---| ---| ---| ---|
|Form|To test car make/model dependancy first select model and ensure there are no drop down options. Then select car make. Ensure the car model field is populated with the correct options for each make|The car model dropdown has no options initially. The car model field is populated with the correct options for each make|Pass||
||Click on each drop down field to ensure correct options are displayed|Correct options are displayed|Pass||
||Fill all fields with correct data in the expected format. Click Submit. Ensure the listing was created by: 1. checking for flash message, 2. Go to Home page and find the card with the new listing |When submitted success flash message is presented. The new listing card appears on the home page's recent listings|Pass||
||Fill all fields with correct data but one. Click Submit. Ensure the form does not submit and appropriate message is displayed. Repeat for all fields. |Form did not submit, appropriate message was displayed|Pass||

- Edit listing Page 

|Section|Test Action|Expected Result|Pass/Fail|Comments|
| ---| ---| ---| ---| ---|
|Form|||Pass|Tested at create listing|
||Open edit listing page. Ensure the form is populated with the correct listing's details|The form is populated with the correct listing's details|Pass||

- My Profile Page 

|Section|Test Action|Expected Result|Pass/Fail|Comments|
| ---| ---| ---| ---| ---|
|Profile Card|Open my profile page. Ensure the image is displaying correctly.|The image is displaying correctly.|Pass||
||Open my profile page. Ensure my details are accurate and are displaying correctly.|My details are accurate and are displaying correctly.|Pass||
|Edit profile button|Click on the edit profile button. Ensure it redirects to the edit profile page.|The edit profile button redirects to the edit profile page.|Pass||
|Delete profile button|Click on the delete profile button. Ensure it redirects to the delete profile page.|The delete profile button redirects to the delete profile page.|Pass||
||Click on my listings link on the sidebar nav. Ensure it redirects to my listings page| Redirects to my listings page|Pass||

- User Account Page 

|Section|Test Action|Expected Result|Pass/Fail|Comments|
| ---| ---| ---| ---| ---|
|Profile Card|Open the user account page from the seller card on the listing page. Ensure the image is displaying correctly.|The image is displaying correctly.|Pass||
||Open the user account page. Ensure the contact details are accurate and are displaying correctly.|The contact details are accurate and are displaying correctly.|Pass||
||Click on listings link on the sidebar nav. Ensure it redirects to the account listings page| Redirects to account listings page|Pass||

- Account Listings Page 

|Section|Test Action|Expected Result|Pass/Fail|Comments|
| ---| ---| ---| ---| ---|
|My Listings Card|When on the account listings page ensure the listings displayed were created by the account user.|The listings displayed were created by the account user. |Pass||
||Click on the More Info button. Ensure it redirects to the single listing page.|The button redirects to the single listing page. |Pass||

- Edit/Update Profile Page 

|Section|Test Action|Expected Result|Pass/Fail|Comments|
| ---| ---| ---| ---| ---|
|Back button|Open the edit profile page. Click on the back button. Ensure it sends back to previous page|When clicked the button brings back to previous page.|Pass||
|Form|Open the edit profile page. Ensure the form is pre-filled with the user's details.| The form is pre-filled with the user's details|Pass||
||Fill all fields with correct data in the expected format. Click Submit. Ensure 1. Flash message appears, the user is redirected to their profile, 3. The user's details have been updated |When submitted success flash message is presented, the user is redirected to the profile page and the details are updated.|Pass||
||Fill all fields with correct data but one. Click Submit. Ensure the form does not submit and appropriate message is displayed. Repeat for all fields. |Form did not submit, appropriate message was displayed|Pass||

- Delete Profile Page 

|Section|Test Action|Expected Result|Pass/Fail|Comments|
| ---| ---| ---| ---| ---|
|Go back button|Click on the go back button. Ensure it sends back to previous page |When clicked the button brings back to previous page.|Pass||
|Delete profile|Click on the delete profile button. Ensure it deletes the user account and the user is redirected to the We are sorry to see you go page. |The user is redirected to the We are sorry to see you go page. By checking in the admin pannel can be confirmed the user and the profile were deleted|Pass||

- Delete Listing Page 

|Section|Test Action|Expected Result|Pass/Fail|Comments|
| ---| ---| ---| ---| ---|
|Go back button|Click on the go back button. Ensure it sends back to previous page |When clicked the button brings back to previous page.|Pass||
|Delete Listing|Click on the delete listing button. Ensure it deletes the listing and the user is redirected to the my listings page. |The user is redirected to the my listings page. By checking in the admin pannel can be confirmed the was deleted|Pass||

- Log In page

|Section|Test Action|Expected Result|Pass/Fail|Comments|
| ---| ---| ---| ---| ---|
|Form|Fill all fields with correct data in the expected format. Click Sign In. Ensure Flash message appears and the user is redirected to the home page. To ensure the user is logged in: Open developer tools and navigate to application. On the side select cookies and check for sessionid being added. |When submitted success flash message is presented, the user is redirected to the home page. Sessionid is added to the cookies|Pass||
| | Fill in the form with incorrect details. Ensure the user is not logged in and flash message appears| Flash message appears in red letting the user know they have entered incorrect details. The user is not signed in|Pass | |
| | Click on the forgot password link. ensure it redirects to the reset password page.| The user is redirected to the reset password page|Pass | |
| | Click on the register here link. ensure it redirects to sign up page.| The user is redirected to the sign up page|Pass | |

- Sign Up Page

|Section|Test Action|Expected Result|Pass/Fail|Comments|
| ---| ---| ---| ---| ---|
|Form|Fill all fields with correct data in the expected format. Click Sign Up. Ensure Flash message appears and the user is redirected to the my profile page.|When submitted success flash message is presented, the user is redirected to the my profile page.|Pass||

- Reset password

|Section|Test Action|Expected Result|Pass/Fail|Comments|
| ---| ---| ---| ---| ---|
|form|Enter valid email, click on reset password |When submitted, email is sent to the email address with instructions.|Pass||


## User Story Testing
|User Story|Screenshot|Result|
| --- | --- | --- |
| As a developer I can set up a new Django project so that I can create the project's structure | The project was set up successfully| <mark>PASS<mark>  |
| As a developer I can connect database and media storage so that the user's stored data is stored successfully | Database and media storage were connected successfully| <mark>PASS<mark> |
| As a developer I can deploy the application early so that I can confirm that the initial setup is working and can continue testing the application during development | The application was deployed after the initial set up to confirm everything is working as expected| <mark>PASS<mark> |
| As a developer I can create wireframes so that the layout of the website is clear for desktop and mobile | wireframes were created and are included in the relevant section of the [README](https://res.cloudinary.com/dutukkel2/image/upload/v1776968971/Home_l29s84.png)| <mark>PASS<mark> |
|As a user I want the website to be responsive so I can view it on my mobile || <mark>PASS<mark> |
| As a user I want to be able to register an account so that I can have access to all functionality of AutoMarket. | | <mark>PASS<mark> |
| As a registered user I want to be able to log in to my account so I can view my profile page, my listings, and my favourites. | | <mark>PASS<mark> |
| As a registered user I want to be able to see my profile page so that I can update my information | | <mark>PASS<mark> |
| As a registered user I want to be able to reset my password so that I can regain access to my account in case I forget my password | | <mark>PASS<mark> |
| As a registered user I want to be able to delete my profile and all my listings if I do not wish to use the services of AutoMarket. | | <mark>PASS<mark> |
| As a user I want to be able to see details about the listing such as a description & images so that I can find suitable car options and make informed decisions before I contact the seller | | <mark>PASS<mark> |
| As a user I want to be able to easily navigate through pages of listings so that I can view all the listings in an organised way (pagination) | | <mark>PASS<mark> |
| As a registered user I want to be able to create a listing so that I can advertise my vehicle for sale. || <mark>PASS<mark> |
| As a registered user I want to be able to edit a listing so that I can correct any mistakes or adjust the listed price | | <mark>PASS<mark> |
| As a registered user I want to be able to delete a listing so that it is not available for admin users to view/approve. | | <mark>PASS<mark> |
| As a registered user I want to be able to see all of the listings I have created so that I can manage and keep track of the vehicles I have listed for sale. | | <mark>PASS<mark> |
| As a registered user I want to be able to send and receive messages with the seller after purchase of the listing. | | <mark>PASS<mark>  |
| As a registered user I want to be able to view any messages I may have received so that I can keep track of communication with other users. | | <mark>PASS<mark>  |
| As a registered user I want to be able to reply to messages so that I can connect with other users. | | <mark>PASS<mark>  |
| As a User I can navigate through the website so that I can access different sections efficiently | | <mark>PASS<mark> |
|As a user I can visit the home page so that I can quickly browse and find relevant car listings based on my preferences | | <mark>PASS<mark> |
