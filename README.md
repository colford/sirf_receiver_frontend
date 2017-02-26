# SiRF Receiver Rrontend
SiRF receiver frontend to interpret and display the SiRF binary data format. Cross platform python/Qt, currently only receives SiRF binary messages at a hardcoded "COM7", 38400 (see sirfcontrol/sirui.py to change). Also only presents the message type 4 at the moment. 

To run you need python3 and pyqt4.

```
python .\bin\app.py
```

