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

* `First change  <ns2:pdmData xmlns:ns2="http://asset.availity.com/PDM/provider"> to <ns2> amd </ns2:pdmData> to </ns2>`


> Linux
```bash
  ./run.sh sample.xml
```

> Windows
```batch
  .\run.bat .\sample.xml
```

* After Runnig the above command the output folder will be generated and inside that specific folder multiple folders will be created and each folder will contain one CSV file, folder name and csv file name will be same.