# ABC CORP
An Equipment Management System

## Project Overview
ABC Corp has grown from a small office, in a single location, to 1000 employees spread across multiple locations, including a few satellite offices throughout the U.S. During this period of growth, the number of IT equipment leased or purchased by the company has become increasingly difficult to track.
<br/><br/>
Presently the company tracks this information on an excel spreadsheet that is shared amongst different IT staff across multiple office locations. This has become very difficult to maintain as multiple copies of the spreadsheet have been made, which has resulted in fragmented and redundant information. There is no single source of truth that accurately reflects the number of equipment in the company’s possession. This is affecting the company’s purchasing decisions as they have ordered too many or not ordered enough equipment, which has resulted in low inventory some items.
<br/><br/>
ABC’s IT department would like to develop an application to track all IT equipment the company currently owns or leases. This includes:
<br/>
* Desktop computers
* Laptops
* Servers
* Printers
* Mobile devices (phone and tablets)

The department would like to:
<br/>
* Track inventory on each item to know when new equipment should be ordered
* Know the location of each items (office location, floor, etc...)
* In the case of a desktop, laptop, phone and tablet devices, they would like to track which employee each has been assigned. The system would like to track each employee’s name, email, contact information and office location
* For all equipment there should be an owner/contact person
* Track the vendor the equipment was purchased/leased from, along with expiration dates for leased items.

The system should allow users to:
<br/>
* Import existing data from excel spreadsheets (CSV files) into the database.
* Add/Update/Deactivate/Search equipment.
* Add/Update/Deactivate/Search employees.
* Add/Update/Deactivate/Search vendors.

Security Requirements<br/>
The system should group users in two roles.
<br/>
* InventoryAdmin - Can perform all functions in the application.
* InventoryUser - Can perform all functions except the following
* Add/Deactivate equipment
* Add/Deactivate employees
* Add/Deactivate vendors
* Import existing data into the database

### Deliverables
Below are the item required deliverables for the final group project.
 <br/>
Project documentation in the form of PowerPoint, Word document or README/Wiki Page(s) in GitHub that contains

* Project overview
* Architecture overview, including technology stack chosen for various modules in the system
* Sample screenshots/wireframes of the user interface
<br/>
Project artifacts in the form of GitHub repository URL. The repository should contain:

* All source code for the application
* Unit tests
* Any other useful information

### Grading
* Teams will be graded based on
	* Previously outlined deliverables being met
	* Code quality - well written and structured code. Adherence to best practices where necessary


## Architecture Overview
<br/><br/>

## Technology Stack
* Django 3.2.7
* Python
* Html, CSS & JavaScript
* SQL LITE


## Application Flow Sample
https://abccorp5.godaddysites.com/  <br/>
(Work in Progress)

## Models/Entities
### User
id: Integer <br/>
name: String <br/>
email: String <br/>
phone: String <br/>
address: String <br/>
officeLocation: Location <br/>
password: String

### Equipment
id: Integer <br/>
name: String <br/>
vendor: Vendor <br/>
equipmentType: String <br/>
purchaseDate: DateTime <br/>
expirationDate: DateTime <br/>
officeLocation: Location  <br/>
floor: String <br/>
assignedTo: UserID 

### Vendor
id: Integer <br/>
name: String <br/>
address: String <br/>
phone: String <br/>
email: String 

### Location
id : Integer <br/>
name : String 



