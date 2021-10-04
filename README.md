# ABC CORP
An Equipment Management System

## Project Overview

## Architecture Overview

## Technology Stack

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
equipments: ListOfEquipmentIds  <br/>
isManager: Boolean <br/>
password: String

### Equipment
id: Integer <br/>
name: String <br/>
vendor: VendorID <br/>
equipmentType: String <br/>
purchaseDate: DateTime <br/>
expirationDate: DateTime <br/>
location: Location  <br/>
floor: String <br/>
assignedTo: UserID <br/>
owner: UserID

### Vendor
id: Integer <br/>
name: String <br/>
address: String <br/>
phone: String <br/>
email: String 

### Location
id : Integer <br/>
name : String 



