#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 30 13:19:56 2018

@author: derek
"""

"""
XML commands:
    
    To retrieve variable info:
        import xml.etree.ElementTree as ET
        tree = ET.parse('NAAMES.xml')  <--- use http connection
        root = tree.getroot()
        var = root.find("./projects/project/datasets/dataset[@name='%s']/variables/variable[@name='%s']" % (dset,varname))
            where dset = DataSet name
            where varname = variable name
            do another search for longname?
        id = var.get('id')
    
    To add data(update) to datagate:
        
        Request (POST only)
        /dg/update/[dbname]/[projectid]/[datasetid]/[varid]
        
        POST message (1D variable)
        <atchem>
           <data rank="1" type="time">
               <values>
                   2006-01-12T18:30:02.25+0000, [...]
                </values>
            </data>
            <data rank="1" type="float">
               <values>
                 1.2345, [...]
               </values>
             </data>
        </atchem>
                            
        POST message (2D variable)
        <atchem>
           <data rank="1" type="time">
               <values>
                   2006-01-12T18:30:02.25+0000, [...]
               </values>
            </data>
            <data rank="2" type="float">
               <values>
                  <values>
                    1.2345, [...]
                  </values>
                  <values>
                    6.7890, [...]
                  </values>
               </values>
            </data>
        </atchem>
                            
        Response
        <atchem/>
        
Datetime commands:
    from datetime import datetime as dt
    from datetime import tzinfo
    import datetime
    
    t = dt.now(tz=datetime.timezone.utc)
    format = '%Y-%m-%dT%H:%M:%S%z'
    dt.strftime(t,format)
        will yield 'YYYY-MM-DDTHH:mm:ss+0000' for use with datagate
        
   
urlllib commands:
    GET xml file:
        with urllib.request.urlopen('http://www.datagate.gov/file.xml') as f:
            xml = f.read().decode('utf-8') # returns xml as string 
        

    POST data:
        xml_data = ET.tostring(root,encoding='utf-8',method='xml')
        data = (xml_data)
        req = urllib.Request(url,data)        
     
"""

