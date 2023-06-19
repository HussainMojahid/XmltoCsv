# XML TO CSV CONVERTER
> Validate XML
    >> Using XSD
>
    >> Basic XML Structure
>   

> Generate Relationship among Parent elements and Child elements.
>

> Generate CSV file
    >> For Elements which contain direct elements.
    > 
    >> If any Element contain Parent Element with child Element the table is not created.



## Requirments
* python3

## How to run 


> Linux
```bash
  ./run.sh sample.xml
  #./run.sh <path_to_xml_file>

  ./run.sh sample.xml schema.xsd # validate using xsd
  #./run.sh <path_to_xml_file> <path_to_xsd_file>

```

> Windows
```bat
  .\run.bat .\sample.xml
  Rem .\run.bat <path_to_xml_file>

  .\run.bat .\sample.xml .\schema.xsd  
  Rem validate using xsd
  Rem .\run.bat <path_to_xml_file> <path_to_xsd_file>
```

* After Runnig the above command the ***datasource*** folder will be generated and inside that specific folder multiple folders will be created and each folder will contain one CSV file, folder name and csv file name will be same.