# SiRF Receiver Frontend
SiRF receiver frontend to interpret and display the SiRF binary data format. Cross platform python/Qt, currently only receives SiRF binary messages at a hardcoded "COM7", 38400 (see sirfcontrol/sirui.py to change). Also only presents the message type 4 at the moment. 

To run you need python3 and pyqt4.

```
python .\bin\app.py
```

The current text layout is draw and was hacked in so probably doesn't scale very well at the moment but below is a screenshot of what it should look like. Carrier to noise scrolls right to left as new measurements are read and has a history over the last 10 seconds. The red C/No is when the C/No is zero, green is when there is a positive reading other than zero.

![Screenshot](https://cloud.githubusercontent.com/assets/13421296/23379214/018024aa-fd2e-11e6-8b9f-2176f5e38be4.JPG)
