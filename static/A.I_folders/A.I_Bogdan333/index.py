









import tflern
import sklearn.neural_networks

@app.route('/disease_prediction2',methods=['POST','GET'])
def disease_prediction2():
        age=float(request.form["age"])
        sex=float(request.form["sex"])
        bloodpresure=float(request.form["bloodpresure"])
        cholesterol=float(request.form["cholesterol"])
        blood_sugure=float(request.form["blood_sugure"])
        maximum_heart_reate=float(request.form["heart_reate"])
        disease=float(request.form["disease"])
        print(age)
        with open('static/training/data.json') as json_data:
            d = json.load(json_data)
        X=[]
        y=[]      
        for i in d:
            X.append([i["maximum heart reate"],i["age"],i["sex"],i["blood sugure"],i["bloodpresure"],i["cholesterol"]])
            y.append([i["disease"]])
       clf = MLPClassifier(solver='lbfgs',alpha=1e-5,hidden_layer_sizes=(12), random_state=1)
        clf.fit(X, y)
        get_prediction_proba=clf.predict_proba([[maximum_heart_reate,age,sex,blood_sugure,bloodpresure,cholesterol ]])
        get_prediction=clf.predict([[maximum_heart_reate,age,sex,blood_sugure,bloodpresure,cholesterol ]])
        save=get_prediction_proba[0][0]
        print(get_prediction_proba)
        for every in range(0,4):
            if get_prediction_proba[0][every]>save:
                save=get_prediction_proba[0][every]
            

        send_this=[save,get_prediction[0]]
        return json.dumps(send_this)



##first

<!DOCTYPE html>
<html lang="en">

  <head>
    <meta charset="UTF-8">
    <title>ACE Autocompletion demo</title>
    <style type="text/css" media="screen">
      body {
        overflow: hidden;
      }
      
      #editor {
        margin: 0;
        position: absolute;
        top: 0;
        bottom: 0;
        left: 0;
        right: 0;
      }
    </style>
  </head>

  <body>
    <!-- html -->
    <div class="myDiv" style="height:800px">
      <div class="ui-layout-center">Center
        <button id="fullscreenButton" type="button">Full-Screen</button>
      </div>
      <div class="ui-layout-north">North</div>
      <div class="ui-layout-south">South</div>
      <div class="ui-layout-east"> code Mirror
        <div id="main-container">
          <div id="editor">Type in a word like "will" below and press ctrl+space or alt+space to get "rhyme completion"</div>
        </div>
      </div>
      <div class="ui-layout-west">West</div>
    </div>
    <!-- ace-plugin -->
    <script src="https://rawgithub.com/ajaxorg/ace-builds/master/src/ace.js" type="text/javascript" charset="utf-8"></script>
    <script src="https://rawgithub.com/ajaxorg/ace-builds/master/src/ext-language_tools.js" type="text/javascript" charset="utf-8"></script>
    <!-- layout.jquery-plugin -->
    <script src="https://code.jquery.com/jquery-1.12.4.min.js"></script>
    <link type="text/css" rel="stylesheet" href="http://layout.jquery-dev.com/lib/css/layout-default-latest.css" />
    <script type="text/javascript" src="http://layout.jquery-dev.com/lib/js/jquery-ui-latest.js"></script>
    <script type="text/javascript" src="http://layout.jquery-dev.com/lib/js/jquery.layout-1.3.0.rc30.80.js"></script>
    <!-- jquery-fullscreen-plugin -->
    <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/jquery-fullscreen-plugin/1.1.4/jquery.fullscreen-min.js"></script>
    <script>
      //
      // setup ace editor
      function setupAce() {
        // trigger extension
        ace.require("ace/ext/language_tools");
        var editor = ace.edit("editor");
        editor.session.setMode("ace/mode/html");
        editor.setTheme("ace/theme/tomorrow");
        // enable autocompletion and snippets
        editor.setOptions({
          enableBasicAutocompletion: true,
          enableSnippets: true,
          enableLiveAutocompletion: false
        });
        $("#fullscreenButton").click(function(event) {
          $("#main-container").toggleFullScreen();
        });
      }
      // init layout
      $('.myDiv').layout({
        resizeWhileDragging: true,
        resizable: true,
        east: {
          size: 800
        },
        onload_end: function() {
          setupAce();
        }
      });
      //
    </script>
  </body>

</html>


##second





<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <title>HTML5 File Upload Demo With Saxon-CE and ACE</title>
    <style>
        /* ACE won't work without explicit CSS. */
        .aceEditor
        {
            position: relative;
            width: 500px;
            height: 200px;
        }
    </style>
    <script src='Scripts/ace/ace.js'></script>
    <script src='Scripts/saxon-ce/Saxonce.nocache.js'></script>
    <!--
        FileSaver.js is an open-source Javascript project that provides support for the HTML5 FileSaver API
        on browsers that do not natively support it.
    -->
    <script src='Scripts/FileSaver.js'></script>
</head>
<body>
    Input XML
    <br />
    <div class='aceEditor' id='aceInputXml' style='float:left;'>&lt;test&gt;
    &lt;testing&gt;
        1 2 3
    &lt;/testing&gt;
&lt;/test&gt;</div>
    <div>
        To input XML, drag-and-drop a file into the text editor to the left,
        use the file input below, or key XML into the text editor.
        <br />
        <input id='xmlFileInput' type='file' />
    </div>
    <br style='clear:both;' />
    Input XSLT    
    <br />
    <div class='aceEditor' id='aceInputXslt' style='float:left;'>&lt;!-- 
    Note: This sample XSLT is an "identity" transformation.
    The result of applying this transformation to a document should be the original document.
--&gt;
&lt;xsl:stylesheet version=&quot;1.0&quot;
 xmlns:xsl=&quot;http://www.w3.org/1999/XSL/Transform&quot;&gt;
    &lt;xsl:template match=&quot;node()|@*&quot;&gt;
      &lt;xsl:copy&gt;
        &lt;xsl:apply-templates select=&quot;node()|@*&quot;/&gt;
      &lt;/xsl:copy&gt;
    &lt;/xsl:template&gt;
&lt;/xsl:stylesheet&gt;</div>
    <div>
        To input XSLT, drag-and-drop a file into the text editor to the left,
        use the file input below, or key XSLT into the text editor.
        <br />
        <input id='xsltFileInput' type='file' />
    </div>
    <br style='clear:both;' />
    Output
    <div class='aceEditor' id='aceOutputXml'></div> 
    <br />
    <input type='button' id='btnTransform' value='Transform' />   
    <input type='button' id='btnSave' value='Save' />
</body>
<script>
    (function () {
        'use strict';
        var aceInputXml, aceInputXslt, aceOutputXml, editors, saxon;

        setupAce();
        setupFileDragAndDrop();
        setupFileInput();
        setupFileDownload();
        setupSaxonce();

        // Initialize the ACE editors and save their object references.
        function setupAce() {
            var x;
            aceInputXml = ace.edit('aceInputXml');
            aceInputXslt = ace.edit('aceInputXslt');
            aceOutputXml = ace.edit('aceOutputXml');
            editors = [aceInputXml, aceInputXslt, aceOutputXml];
            for (x in editors) {
                editors[x].setTheme('ace/theme/monokai');
                editors[x].getSession().setMode('ace/mode/xml');
            }
        }

        // Rig up the Input XML and Input XSLT ACE editors so that the user can populate them
        // by dragging and dropping a file that contains XML.
        function setupFileDragAndDrop() {
            var inputXml, inputXslt;
            inputXml = document.getElementById('aceInputXml');
            inputXslt = document.getElementById('aceInputXslt');
            addFileDragAndDropEventListeners(inputXml, aceInputXml);
            addFileDragAndDropEventListeners(inputXslt, aceInputXslt);

            function addFileDragAndDropEventListeners(aceInputDiv, aceObject) {
                aceInputDiv.addEventListener('dragover', function (e) {
                    stopEvent(e);
                });

                aceInputDiv.addEventListener('drop', function (e) {
                    putFileContentsInAceEditor(e.dataTransfer.files[0], aceObject);
                    stopEvent(e);
                });

                function stopEvent(e) {
                    e.stopPropagation();
                    e.preventDefault();
                }
            } // end addFileDragAndDropEventListeners
        } // end setupFileDragAndDrop        

        // Set up the HTML5 file inputs so that the user can populate the ACE editors
        // by selecting a file.
        function setupFileInput() {
            (function () {
                var xmlFileInput;
                xmlFileInput = document.getElementById('xmlFileInput');
                xmlFileInput.addEventListener('change', function (e) {
                    var file;
                    file = e.srcElement.files[0];
                    putFileContentsInAceEditor(file, aceInputXml);
                });
            })();
            (function () {
                var xsltFileInput;
                xsltFileInput = document.getElementById('xsltFileInput');
                xsltFileInput.addEventListener('change', function (e) {
                    var file;
                    file = e.srcElement.files[0];
                    putFileContentsInAceEditor(file, aceInputXslt);
                });
            })();
        }

        // Setup the button that the user can click to download the output.
        function setupFileDownload() {
            var button;
            button = document.getElementById('btnSave');
            button.addEventListener('click', function (e) {
                var outputXmlStr, blob;
                outputXmlStr = aceOutputXml.getSession().getValue();
                // If the string is null or empty, do nothing.
                if (!outputXmlStr)
                    return;
                blob = new Blob([outputXmlStr], { type: 'text/plain' });
                // Use the FileSaver.js interface to download the file.
                saveAs(blob, 'Output.xml');
            });
        }

        // A small function that takes a file and an ACE editor object.
        // The function reads the file and copies its contents into the ACE editor.
        function putFileContentsInAceEditor(file, aceEditor) {
            var reader, text;
            reader = new FileReader();
            reader.onload = (function (file) {
                text = file.target.result;
                aceEditor.getSession().setValue(text);
            });
            reader.readAsText(file);
        }

        function setupSaxonce() {
            // This object is required by Saxon.
            // Saxon will automatically invoke this function when it loads.
            window.onSaxonLoad = function () {
                saxon = Saxon;
                setupTransformButton(Saxon);
            };
        }

        // Note that this gets called when setupSaxonce runs.
        // This ensures that the Saxon object is available when the user clicks the [Transform] button.
        function setupTransformButton(Saxon) {
            var button;
            button = document.getElementById('btnTransform');
            button.addEventListener('click', function (e) {
                var inputXmlStr, inputXsltStr, outputXmlStr,
                    inputXmlDoc, inputXsltDoc, outputXmlDoc, processor;
                // Get the input XML and XSLT strings from the ACE editors.
                inputXmlStr = aceInputXml.getSession().getValue();
                inputXsltStr = aceInputXslt.getSession().getValue();
                // Transform the inputs into Saxon XML documents.
                inputXmlDoc = Saxon.parseXML(inputXmlStr);
                inputXsltDoc = Saxon.parseXML(inputXsltStr);
                // Get an XSLT20Processor object that will apply the transformation.
                processor = Saxon.newXSLT20Processor(inputXsltDoc);
                // Apply the transformation.
                outputXmlDoc = processor.transformToDocument(inputXmlDoc);
                outputXmlStr = Saxon.serializeXML(outputXmlDoc);
                // Put the results of the transformation in the output ACE editor.
                aceOutputXml.getSession().setValue(outputXmlStr);
            });
        }
    })();    
</script>
</html>



