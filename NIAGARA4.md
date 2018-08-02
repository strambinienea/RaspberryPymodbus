# Connecting a Pymodbus Server with Niagara4

#### Requirement

- Pymodbus Server [(link)](https://github.com/strambinienea/RaspberryPymodbus/blob/master/GUIDE.md "Link to our guide")
- Niagara4 license

#### Creating a station
In first we need a station, if you have already one you can skip to the next point otherways here we explain how to create one.
Start by clicking on the `Tools` button in the Menu Bar, you will then need to click on the `New Station` button, a window will pop-up, here you will need to write down the station name and select `NewControllerStation`. 
The new window will ask you if you want to set the password and username, write these information down and the check the box that says `copy it to secure platform for "localhost" with Station Copier`, then click finish, select then the safer connection method `Platform TLS Connection`, insert then the username and password, configure the Station Transfer Wizard putting a tick in the box wich says `START AFTER INSTALL` then click next and then Finish.
Close the dialog box and open the App Director to ensure the station is running properly. You have now a complete station ready to use.

#### Starting a Client
Now that you have a station you will need to start a Client in order to comunicate with the Pymodbus Server. To do that start by clicking in the `Window` tab in the Menu Bar, click then in the `Side Bar` tab and add the Palette, this tab is used to add preset and usefull function. In the palette tab on the left, click in the text box and write down these two name, modbusTcp and kitControl, the first one is used for the implementation of the modbus Tcp client, the second one contain usefull object, mathematical funcion and other usefull things. In first place we will need to create a Tcp network, to do that we need to put a ModbusTcpNetwork, find it in the modbusTcp palette, in the Config/Drivers folder, inside that we need to put a ModbusTcpDevice, also found in the modbusTcp palette. With a double click on the device a window is open, showing you all the device property, here you will need to set the Server IP and port, the type of register you are using and their address. If you then click the right mouse button on the TcpDrive, go to action and than click ping you should se on the server a connection and an excange of information.
In order to read the register value you will need to doubleclick on the point folder, here you will see a modbus point view, by clicking in the `new` button on the bottom a window will appear, if you then click in the dropdown menu you will se a list of point, here you can select the one usefull to your task, for example if you want to read a register containing a number you will need to select the `Numeric Point` you can select the ne number of points to add and their address in the server, here you can select the type of address if decimal, hex or modbus type, the decimal and hex one start from zero so if your register's address is zero you will need to type zero, if you select modbus type to read the same register you will need to type in not zero but  40001 bacause the modbus start counting by 1 and the register are allocate starting by the 40000.

You should now have a functioning Client that connect to the Server and is able to read the registers, you could now use all the math function found in the ktControll palette to process the data as you like.

#### Exporting histories into MySql database
Start by crating a `RdbmsNetworkMySQL` in the station, inside the network create a new device, a `MySQLDatabase`, this is the device that is going to be writing down the data on he MySql database, but first you will need to configure it, double-click on it, in the IP section you must write the ip of the Sql database, in the username and password field you need to write the username and passwordin order to acces to the database, the last thing you must do is write the name of the database, in the `Database Name`.Now you can save the data, in order to do that you will need to open the `Histories` tab inside the `MySQLDatabase` device, here you can create the object that will write on the database. Click on the `New` button on the bottom of the window and add `MySQLHistoryExport`, a new window will open, here you can write the name of the object, the ID of the history you want to save and how many times it will save it. In order to find the History ID you will need to open the `History` tab of the Station, inside there you will need to find the history you want to save and open it in the AXproperty view, here you will find the history ID. ONce you have wrote it downyou can save the new object. 


-Strambini Enea & Tezza Giacomo
